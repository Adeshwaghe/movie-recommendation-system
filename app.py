import streamlit as st
import pandas as pd
import numpy as np
import re
import base64

# -------------------------
# Set Background Image & Styling
# -------------------------
# Update the set_background function and add new styling

def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode()
    page_bg_img = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        font-family: 'Poppins', sans-serif;
    }}
    
    .stMarkdown, .stText {{
        color: #ffffff !important;
    }}

    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Poppins', sans-serif;
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        letter-spacing: 0.5px;
    }}

    /* Glass morphism effect for widgets */
    .stSelectbox, .stMultiselect, .stSlider, .stNumberInput {{
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 10px !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }}

    /* Button styling */
    .stButton>button {{
        background: linear-gradient(135deg, #FF6B6B 0%, #FF4B4B 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
    }}

    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.4);
    }}

    /* Expander styling */
    .streamlit-expander {{
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }}

    /* Slider styling */
    .stSlider div[data-baseweb="slider"] {{
        background: rgba(255, 255, 255, 0.2) !important;
    }}

    /* Table styling update */
    .styled-table {{
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 16px !important;
        overflow: hidden;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }}

    .styled-table thead tr {{
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%) !important;
        color: black !important;
        font-weight: 600;
    }}

    .styled-table tbody tr {{
        transition: all 0.3s ease;
    }}

    .styled-table tbody tr:hover {{
        background-color: rgba(255, 255, 255, 0.2) !important;
        transform: scale(1.01);
    }}

    /* Custom progress bar */
    .stProgress > div > div > div > div {{
        background: linear-gradient(135deg, #FF6B6B 0%, #FF4B4B 100%);
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Update the title display with emoji and subtitle
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3rem; margin-bottom: 0.5rem;'>🎬 Movie Buddy</h1>
        <p style='font-size: 1.2rem; opacity: 0.9;'>Your Personal Movie Recommendation System</p>
    </div>
""", unsafe_allow_html=True)

# Rest of your existing code remains the same...

# -------------------------
# Load Data
# -------------------------
@st.cache_data
def load_data():
    movies = pd.read_csv("movies.csv")
    ratings = pd.read_csv("ratings.csv", usecols=["userId", "movieId", "rating"])
    
    avg_ratings = ratings.groupby("movieId")["rating"].mean().reset_index().rename(columns={"rating":"avg_rating"})
    count_ratings = ratings.groupby("movieId")["rating"].count().reset_index().rename(columns={"rating":"rating_count"})
    
    movies = movies.merge(avg_ratings, on="movieId", how="left")
    movies = movies.merge(count_ratings, on="movieId", how="left").fillna({"avg_rating":0, "rating_count":0})
    
    def extract_year(title):
        match = re.search(r'\((\d{4})\)', title)
        return int(match.group(1)) if match else None
    movies["year"] = movies["title"].apply(extract_year)
    
    if "genres" not in movies.columns:
        movies["genres"] = ""
    
    merged_data = pd.merge(ratings, movies, on="movieId")
    return movies, ratings, merged_data

movies, ratings, merged_data = load_data()

# -------------------------
# Bayesian Scoring
# -------------------------
def compute_bayesian_scores(df, all_ratings_df, m_value=None):
    global_mean = all_ratings_df["rating"].mean()
    counts = all_ratings_df.groupby("movieId")["rating"].count()
    m = int(counts.quantile(0.75)) if m_value is None and not counts.empty else (5 if m_value is None else m_value)
    v = df["rating_count"].fillna(0)
    R = df["avg_rating"].fillna(0)
    C = global_mean
    return (v/(v+m))*R + (m/(v+m))*C

def recommend_movies_bayesian(filtered_movies_df, all_ratings_df, top_n=5, exclude_title=None):
    candidates = filtered_movies_df.copy()
    candidates["bayes_score"] = compute_bayesian_scores(candidates, all_ratings_df)
    if exclude_title:
        candidates = candidates[candidates["title"] != exclude_title]
    candidates_sorted = candidates.sort_values("bayes_score", ascending=False)
    return candidates_sorted.head(top_n)[["title","genres","year","avg_rating","rating_count","bayes_score"]]

# -------------------------
# Styled HTML Table Function
# -------------------------
def show_styled_table(df, show_bayes=False):
    if show_bayes:
        df = df[["title","genres","year","avg_rating","rating_count","bayes_score"]].copy()
    else:
        df = df[["title","genres","year","avg_rating","rating_count"]].copy()
    
    rename_dict = {
        "title":"Title",
        "genres":"Genres",
        "year":"Year",
        "avg_rating":"Avg Rating",
        "rating_count":"No. of Ratings",
    }
    if show_bayes:
        rename_dict["bayes_score"] = "Bayes Score"
    df.rename(columns=rename_dict, inplace=True)
    
    df = df.reset_index(drop=True)
    df["Sr No"] = df.index + 1
    
    cols_order = ["Sr No", "Title", "Genres", "Year", "Avg Rating", "No. of Ratings"]
    if show_bayes:
        cols_order.append("Bayes Score")
    df = df[cols_order]

    table_html = '<table class="styled-table">'
    table_html += '<thead><tr>'
    for col in df.columns:
        table_html += f'<th>{col}</th>'
    table_html += '</tr></thead>'
    
    table_html += '<tbody>'
    for i, row in df.iterrows():
        bg_color = '#f5f5f5' if i % 2 == 0 else 'rgba(245,245,245,0.95)'
        table_html += f'<tr style="background-color:{bg_color}">'
        for col in df.columns:
            val = row[col]
            if isinstance(val, float):
                val = f"{val:.2f}"
            table_html += f'<td>{val}</td>'
        table_html += '</tr>'
    table_html += '</tbody></table>'

    st.markdown("""
        <style>
        .styled-table {
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 14px;
            font-family: sans-serif;
            min-width: 500px;
            width: 100%;
            border-radius: 8px 8px 0 0;
            overflow: hidden;
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
        }
        .styled-table thead tr {
            background-color: #FFD700;
            color: black;
            font-weight: bold;
            text-align: center;
        }
        .styled-table th, .styled-table td {
            padding: 10px 15px;
            color:black;
            text-align: center;
        }
        .styled-table tbody tr:last-of-type {
            border-bottom: 2px solid #FFD700;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown(table_html, unsafe_allow_html=True)

# -------------------------
# Streamlit UI
# -------------------------
st.title("🎬 Movie Recommendation System")

# Genre filter
with st.expander("🎭 **Select Genre(s)**", expanded=True):
    all_genres = sorted(set(genre for genres in movies["genres"].dropna() for genre in genres.split("|")))
    selected_genres = st.multiselect("Choose Genres:", options=all_genres, default=[])

# Year filter
col1, col2 = st.columns(2)
with col1:
    year_min, year_max = int(movies["year"].min()), int(movies["year"].max())
    year_min_input = st.number_input("Min Year:", min_value=year_min, max_value=year_max, value=year_min)
with col2:
    year_max_input = st.number_input("Max Year:", min_value=year_min, max_value=year_max, value=year_max)
selected_year_range = st.slider("Select Year Range:", min_value=year_min, max_value=year_max, value=(year_min_input, year_max_input))
filtered_movies = movies[(movies["year"] >= selected_year_range[0]) & (movies["year"] <= selected_year_range[1])]

# Rating filter
col3, col4 = st.columns(2)
with col3:
    min_rating, max_rating = float(movies["avg_rating"].min()), float(movies["avg_rating"].max())
    rating_min_input = st.number_input("Min Rating:", min_value=min_rating, max_value=max_rating, value=min_rating, step=0.1)
with col4:
    rating_max_input = st.number_input("Max Rating:", min_value=min_rating, max_value=max_rating, value=max_rating, step=0.1)
selected_rating_range = st.slider("Select Rating Range:", min_value=min_rating, max_value=max_rating, value=(rating_min_input, rating_max_input))
filtered_movies = filtered_movies[(filtered_movies["avg_rating"] >= selected_rating_range[0]) & (filtered_movies["avg_rating"] <= selected_rating_range[1])]

# Apply genre filter
if selected_genres:
    def has_genres(genres_str, selected):
        if pd.isna(genres_str):
            return False
        genres = genres_str.split("|")
        return all(g in genres for g in selected)
    filtered_movies = filtered_movies[filtered_movies["genres"].apply(lambda x: has_genres(x, selected_genres))]

# Movie title filter
movie_titles = sorted(filtered_movies["title"].unique())
movie_titles.insert(0, "All")
selected_title = st.selectbox("🎬 Select a Movie Title:", movie_titles)
if selected_title != "All":
    filtered_movies = filtered_movies[filtered_movies["title"] == selected_title]

# Show recommendations
available_titles = sorted(filtered_movies["title"].unique())
base_movie = st.selectbox("🎬 Exclude a movie from recommendations:", ["None"] + available_titles)
if base_movie == "None":
    base_movie = None
num_rec = st.slider("Number of recommendations to show:", 1, 20, 5)

# Pre-calculate global C and m
C = merged_data["rating"].mean()
counts = merged_data.groupby("movieId")["rating"].count()
m = int(counts.quantile(0.75))

if st.button("🎯 Show Recommendations"):
    recs = recommend_movies_bayesian(filtered_movies, merged_data, top_n=num_rec, exclude_title=base_movie)
    if recs.empty:
        st.error("No recommendations available. Try widening the filters.")
    else:
        st.subheader(f"🍿 Top {len(recs)} recommendations:")

        # Info expander for Bayes Score with actual C and m
        with st.expander("ℹ️ How Bayes Score is calculated"):
            st.markdown(f"""
            <div style="color:black; font-size:14px;">
            <b>Bayesian Average Formula:</b><br>
            <code>Bayes Score = (v / (v + m)) * R + (m / (v + m)) * C</code><br><br>
            
            Where:<br>
            - <b>v</b> = Number of ratings for the movie (<i>rating_count</i>)<br>
            - <b>R</b> = Average rating of the movie (<i>avg_rating</i>)<br>
            - <b>C</b> = Global mean rating of all movies = <b>{C:.2f}</b><br>
            - <b>m</b> = Minimum number of ratings to be considered = <b>{m}</b> (75th percentile of all movie rating counts)<br><br>
            
            This ensures movies with very few ratings are not unfairly ranked too high or too low.
            </div>
            """, unsafe_allow_html=True)

        show_styled_table(recs, show_bayes=True)
        st.markdown("**Recommended Titles:**")
        for _, row in recs.iterrows():
            st.write(f"- {row['title']} — Bayes score: {row['bayes_score']:.3f} — Avg Rating: {row['avg_rating']:.2f} ({int(row['rating_count'])} ratings)")

if st.button("📌 Show Filtered Movies Only"):
    st.subheader("🎞️ All Filtered Movies")
    show_styled_table(filtered_movies.sort_values("title"), show_bayes=False)
