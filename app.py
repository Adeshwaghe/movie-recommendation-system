import streamlit as st
import pandas as pd
import numpy as np
import re
import base64

# -------------------------
# Modern Cinematic Styling
# -------------------------
def set_cinematic_style():
    cinematic_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Cinzel:wght@400;500;600&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Main header styling */
    .main-header {
        text-align: center;
        padding: 3rem 0 2rem 0;
        background: linear-gradient(135deg, 
            rgba(255, 215, 0, 0.1) 0%, 
            rgba(255, 165, 0, 0.1) 50%, 
            rgba(255, 69, 0, 0.1) 100%);
        border-radius: 0 0 30px 30px;
        margin-bottom: 2rem;
        border-bottom: 2px solid rgba(255, 215, 0, 0.3);
    }
    
    .main-header h1 {
        font-family: 'Cinzel', serif;
        font-size: 4rem !important;
        font-weight: 600;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF4500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 8px rgba(255, 215, 0, 0.3);
    }
    
    .main-header p {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    /* Modern card styling for expanders and containers */
    .modern-card {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        margin: 15px 0;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.36);
        transition: all 0.3s ease;
    }
    
    .modern-card:hover {
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        transform: translateY(-2px);
        box-shadow: 0 12px 40px 0 rgba(255, 215, 0, 0.15);
    }
    
    /* Enhanced widget styling */
    .stSelectbox > div > div, .stMultiselect > div > div {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 15px !important;
        color: white !important;
        font-weight: 400;
    }
    
    .stSlider > div > div {
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 15px !important;
    }
    
    .stNumberInput > div > div {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 15px !important;
        color: white !important;
    }
    
    /* Premium button styling */
    .stButton > button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF8C00 100%) !important;
        color: #000 !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 12px 30px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3) !important;
        font-size: 1rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.5) !important;
        background: linear-gradient(135deg, #FFA500 0%, #FF8C00 50%, #FF6347 100%) !important;
    }
    
    /* Modern table styling */
    .modern-table {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.36) !important;
    }
    
    .modern-table thead tr {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%) !important;
        color: #000 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    
    .modern-table tbody tr {
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.02) !important;
    }
    
    .modern-table tbody tr:nth-child(even) {
        background: rgba(255, 255, 255, 0.05) !important;
    }
    
    .modern-table tbody tr:hover {
        background: rgba(255, 215, 0, 0.1) !important;
        transform: scale(1.01);
    }
    
    .modern-table th, .modern-table td {
        padding: 15px 20px !important;
        text-align: center !important;
        border: none !important;
        color: white !important;
        font-weight: 400 !important;
    }
    
    /* Label styling */
    .stMarkdown p, .stText {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 500;
    }
    
    /* Expander header styling */
    .streamlit-expanderHeader {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #FFD700 !important;
        background: rgba(255, 215, 0, 0.1) !important;
        border-radius: 15px !important;
        padding: 15px 20px !important;
        margin: 10px 0 !important;
    }
    
    /* Custom progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF8C00 100%);
        border-radius: 10px;
    }
    
    /* Section headers */
    .section-header {
        font-family: 'Cinzel', serif;
        font-size: 2rem !important;
        color: #FFD700 !important;
        text-align: center;
        margin: 2rem 0 1rem 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    /* Movie card styling for recommendations */
    .movie-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .movie-card:hover {
        border: 1px solid rgba(255, 215, 0, 0.4);
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(255, 215, 0, 0.2);
    }
    </style>
    """
    st.markdown(cinematic_css, unsafe_allow_html=True)

# -------------------------
# Updated Header with Modern Design
# -------------------------
def show_modern_header():
    st.markdown("""
        <div class="main-header">
            <h1>🎬 Movie Buddy</h1>
            <p>Your Personal Cinematic Recommendation Engine</p>
        </div>
    """, unsafe_allow_html=True)

# -------------------------
# Load Data (unchanged)
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
# Bayesian Scoring (unchanged)
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
# Modern Styled Table Function
# -------------------------
def show_modern_table(df, show_bayes=False):
    if show_bayes:
        df = df[["title","genres","year","avg_rating","rating_count","bayes_score"]].copy()
    else:
        df = df[["title","genres","year","avg_rating","rating_count"]].copy()
    
    rename_dict = {
        "title":"🎬 Title",
        "genres":"🎭 Genres",
        "year":"📅 Year",
        "avg_rating":"⭐ Avg Rating",
        "rating_count":"📊 Rating Count",
    }
    if show_bayes:
        rename_dict["bayes_score"] = "🎯 Bayes Score"
    df.rename(columns=rename_dict, inplace=True)
    
    df = df.reset_index(drop=True)
    df["#"] = df.index + 1
    
    cols_order = ["#", "🎬 Title", "🎭 Genres", "📅 Year", "⭐ Avg Rating", "📊 Rating Count"]
    if show_bayes:
        cols_order.append("🎯 Bayes Score")
    df = df[cols_order]

    table_html = '<table class="modern-table">'
    table_html += '<thead><tr>'
    for col in df.columns:
        table_html += f'<th>{col}</th>'
    table_html += '</tr></thead>'
    
    table_html += '<tbody>'
    for i, row in df.iterrows():
        table_html += '<tr>'
        for col in df.columns:
            val = row[col]
            if isinstance(val, float):
                val = f"{val:.2f}"
            table_html += f'<td>{val}</td>'
        table_html += '</tr>'
    table_html += '</tbody></table>'

    st.markdown(table_html, unsafe_allow_html=True)

# -------------------------
# Modern Streamlit UI
# -------------------------

# Apply cinematic styling
set_cinematic_style()
show_modern_header()

# Main container with modern card styling
with st.container():
  
    
    st.markdown('<h2 class="section-header">🎭 Filter Movies</h2>', unsafe_allow_html=True)
    
    # Genre filter in expander
    with st.expander("🎭 **Select Genre(s)**", expanded=True):
        all_genres = sorted(set(genre for genres in movies["genres"].dropna() for genre in genres.split("|")))
        selected_genres = st.multiselect("Choose Genres:", options=all_genres, default=[],
                                       help="Select one or multiple genres to filter movies")

    # Year and Rating filters in columns
    col1, col2 = st.columns(2)
    with col1:
        year_min, year_max = int(movies["year"].min()), int(movies["year"].max())
        selected_year_range = st.slider("📅 Select Year Range:", 
                                      min_value=year_min, 
                                      max_value=year_max, 
                                      value=(1980, year_max))

    with col2:
        min_rating, max_rating = float(movies["avg_rating"].min()), float(movies["avg_rating"].max())
        selected_rating_range = st.slider("⭐ Select Rating Range:", 
                                        min_value=min_rating, 
                                        max_value=max_rating, 
                                        value=(3.0, max_rating),
                                        step=0.1)

    # Apply filters
    filtered_movies = movies[
        (movies["year"] >= selected_year_range[0]) & 
        (movies["year"] <= selected_year_range[1]) &
        (movies["avg_rating"] >= selected_rating_range[0]) & 
        (movies["avg_rating"] <= selected_rating_range[1])
    ]

    # Genre filter application
    if selected_genres:
        def has_genres(genres_str, selected):
            if pd.isna(genres_str):
                return False
            genres = genres_str.split("|")
            return all(g in genres for g in selected)
        filtered_movies = filtered_movies[filtered_movies["genres"].apply(lambda x: has_genres(x, selected_genres))]

    # Movie selection
    col3, col4 = st.columns(2)
    with col3:
        movie_titles = sorted(filtered_movies["title"].unique())
        selected_title = st.selectbox("🎬 Select a Movie:", ["All"] + movie_titles,
                                    help="Choose a specific movie or 'All' to see all filtered movies")
        
        if selected_title != "All":
            filtered_movies = filtered_movies[filtered_movies["title"] == selected_title]

    with col44:
        available_titles = sorted(filtered_movies["title"].unique())
        base_movie = st.selectbox("🚫 Exclude from recommendations:", ["None"] + available_titles,
                                help="Choose a movie to exclude from recommendations")
        if base_movie == "None":
            base_movie = None

    # Number of recommendations
    num_rec = st.slider("🔢 Number of recommendations:", 1, 20, 5, 
                       help="Adjust how many movie recommendations to display")

    st.markdown('</div>', unsafe_allow_html=True)


col5, col6 = st.columns(2)
with col5:
    if st.button("🎯 Get Smart Recommendations", use_container_width=True):
        if filtered_movies.empty:
            st.error("No movies match your filters. Please adjust your criteria.")
        else:
            recs = recommend_movies_bayesian(filtered_movies, merged_data, top_n=num_rec, exclude_title=base_movie)
            if recs.empty:
                st.error("No recommendations available. Try widening your filters.")
            else:
                st.markdown(f'<h2 class="section-header">🍿 Top {len(recs)} Recommendations</h2>', unsafe_allow_html=True)
                
                # Bayes score explanation
                with st.expander("ℹ️ How Recommendations Work", expanded=False):
                    C = merged_data["rating"].mean()
                    counts = merged_data.groupby("movieId")["rating"].count()
                    m = int(counts.quantile(0.75))
                    
                    st.markdown(f"""
                    <div style="color:white; font-size:14px; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                    <h4 style="color:#FFD700; margin-bottom: 10px;">🎯 Bayesian Scoring Algorithm</h4>
                    <b>Formula:</b> <code>Bayes Score = (v / (v + m)) × R + (m / (v + m)) × C</code><br><br>
                    
                    <b>Where:</b><br>
                    • <b>v</b> = Number of ratings for the movie<br>
                    • <b>R</b> = Average rating of the movie<br>
                    • <b>C</b> = Global mean rating = <b>{C:.2f}</b><br>
                    • <b>m</b> = Minimum ratings threshold = <b>{m}</b><br><br>
                    
                    This ensures fair ranking for movies with different numbers of ratings.
                    </div>
                    """, unsafe_allow_html=True)

                show_modern_table(recs, show_bayes=True)

with col6:
    if st.button("📋 Show Filtered Movies", use_container_width=True):
        st.markdown('<h2 class="section-header">🎞️ Filtered Movies</h2>', unsafe_allow_html=True)
        show_modern_table(filtered_movies.sort_values("avg_rating", ascending=False), show_bayes=False)

st.markdown('</div>', unsafe_allow_html=True)

# Stats section
if not filtered_movies.empty:
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">📊 Quick Stats</h3>', unsafe_allow_html=True)
    
    col7, col8, col9, col10 = st.columns(4)
    with col7:
        st.metric("Total Movies", len(filtered_movies))
    with col8:
        st.metric("Average Rating", f"{filtered_movies['avg_rating'].mean():.2f}")
    with col9:
        st.metric("Year Range", f"{filtered_movies['year'].min()}-{filtered_movies['year'].max()}")
    with col10:
        st.metric("Top Genre", filtered_movies['genres'].str.split('|').explode().mode().iloc[0] if not filtered_movies.empty else "N/A")
    
    st.markdown('</div>', unsafe_allow_html=True)
