import streamlit as st
import pandas as pd
import numpy as np
import re
import base64

# -------------------------
# Set Background Image & Styling
# -------------------------
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode()
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: #ffffff;  
        font-family: Arial, sans-serif;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
    }}
    
    .stMarkdown, .stText {{
        color: #ffffff !important;
    }}

    .stSelectbox, .stMultiselect, .stSlider, .stNumberInput, .stMultiSelect, .stExpander {{
        color: black !important;
        background-color: rgba(255, 255, 255, 0.9) !important; 
        border-radius: 10px;
        padding: 5px;
    }}

    .stButton>button {{
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background("background.jpg")

# -------------------------
# Data Loading
# -------------------------
@st.cache_data
def load_data():
    movies = pd.read_csv("movies.csv")  # Expected: movieId, title, genres
    ratings = pd.read_csv("ratings.csv", usecols=["userId", "movieId", "rating"])
    
    avg_ratings = ratings.groupby("movieId")["rating"].mean().reset_index().rename(columns={"rating": "avg_rating"})
    movies = movies.merge(avg_ratings, on="movieId", how="left")

    def extract_year(title):
        match = re.search(r'\((\d{4})\)', title)
        return int(match.group(1)) if match else None
    movies["year"] = movies["title"].apply(extract_year)
    
    merged_data = pd.merge(ratings, movies, on="movieId")
    return movies, ratings, merged_data

movies, ratings, merged_data = load_data()

# -------------------------
# Sidebar Filters
# -------------------------
st.title("🎬 Movie Recommendation System")
st.write("Use the filters below and click 'Recommend' to see movie suggestions.")

# **Genre Selection**
with st.expander("🎭 **Select Genre(s)**", expanded=True):
    all_genres = sorted(set(genre for genres in movies["genres"].dropna() for genre in genres.split("|")))
    selected_genres = st.multiselect("Choose Genres:", options=all_genres, default=[])

# **Year Range Filters**
st.write("📅 **Filter by Release Year**")
col1, col2 = st.columns(2)

with col1:
    year_min = int(movies["year"].min())
    year_max = int(movies["year"].max())
    year_min_input = st.number_input("Enter Min Year:", min_value=year_min, max_value=year_max, value=year_min, step=1)

with col2:
    year_max_input = st.number_input("Enter Max Year:", min_value=year_min, max_value=year_max, value=year_max, step=1)

selected_year_range = st.slider("Select Year Range:", min_value=year_min, max_value=year_max, value=(year_min_input, year_max_input))

# Apply year filters
filtered_movies = movies[
    (movies["year"] >= selected_year_range[0]) & 
    (movies["year"] <= selected_year_range[1])
]

# **Rating Range Filters**
st.write("⭐ **Filter by Ratings**")
col3, col4 = st.columns(2)

with col3:
    min_rating = float(movies["avg_rating"].min())
    max_rating = float(movies["avg_rating"].max())
    rating_min_input = st.number_input("Enter Min Rating:", min_value=min_rating, max_value=max_rating, value=min_rating, step=0.1)

with col4:
    rating_max_input = st.number_input("Enter Max Rating:", min_value=min_rating, max_value=max_rating, value=max_rating, step=0.1)

selected_rating_range = st.slider("Select Rating Range:", min_value=min_rating, max_value=max_rating, value=(rating_min_input, rating_max_input))

# Apply rating filters
filtered_movies = filtered_movies[
    (filtered_movies["avg_rating"] >= selected_rating_range[0]) & 
    (filtered_movies["avg_rating"] <= selected_rating_range[1])
]

# **Movie Title Filter**
movie_titles = sorted(filtered_movies["title"].unique())
movie_titles.insert(0, "All")
selected_title = st.selectbox("🎬 Select a Movie Title:", options=movie_titles)

if selected_title != "All":
    filtered_movies = filtered_movies[filtered_movies["title"] == selected_title]

# -------------------------
# Movie Recommendations
# -------------------------
if st.button("📌 Recommend Movies"):
    st.write("### 🎞️ Filtered Movies")
    st.write(filtered_movies[["movieId", "title", "genres", "year", "avg_rating"]].sort_values("title").reset_index(drop=True))

    def compute_correlations(filtered_movies, merged_data):
        filtered_ids = filtered_movies["movieId"].unique()
        filtered_ratings = merged_data[merged_data["movieId"].isin(filtered_ids)]
        
        if filtered_ratings.empty:
            return None
        
        user_movie_matrix = filtered_ratings.pivot_table(index="userId", columns="title", values="rating")
        correlation = user_movie_matrix.corr(method="pearson", min_periods=5)
        return correlation

    correlation = compute_correlations(filtered_movies, merged_data)
    if correlation is None or correlation.empty:
        st.error("Not enough data for recommendations. Try changing the filters.")
    else:
        available_titles = sorted(filtered_movies["title"].unique())
        selected_movie = st.selectbox("🎬 Choose a movie for recommendations:", available_titles)

        def recommend_movies(selected_movie, correlation, num_recommendations=5):
            if selected_movie not in correlation:
                return [f"Movie '{selected_movie}' not found in the dataset."]
            similar = correlation[selected_movie].dropna().sort_values(ascending=False)
            similar = similar.drop(selected_movie, errors="ignore")
            return similar.head(num_recommendations).index.tolist()

        if st.button("🎥 Get Recommendations"):
            recommendations = recommend_movies(selected_movie, correlation)
            st.subheader(f"🍿 Movies similar to '{selected_movie}':")
            for rec in recommendations:
                st.write(f"- {rec}")
