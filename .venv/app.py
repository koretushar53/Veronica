import pandas as pd
import streamlit as st
import pickle
import requests
import urllib.parse

# 🔑 OMDb API Key
OMDB_API_KEY = "c9b16384"  # replace with your own key if needed

# -------------------------------
# Custom CSS Styling
# -------------------------------
st.markdown("""
    <style>
        /* Background */
        .stApp {
            background: linear-gradient(135deg, #1f1c2c, #928dab);
            color: white;
        }

        /* Title */
        .title {
            font-size: 40px;
            font-weight: 700;
            text-align: center;
            color: #FFD700;
            margin-bottom: 30px;
        }

        /* Dropdown */
        .stSelectbox label {
            font-size: 18px;
            font-weight: 600;
            color: #f5f5f5;
        }

        /* Recommend Button */
        div.stButton > button {
            background-color: #FF5733;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 18px;
            font-weight: bold;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background-color: #C70039;
            transform: scale(1.05);
        }

        /* Recommendation Title */
        .recommend-title {
            font-size: 26px;
            font-weight: bold;
            margin-top: 20px;
            text-align: center;
            color: #00FFAB;
        }

        /* Movie Cards */
        .movie-card {
            padding: 10px;
            border-radius: 15px;
            background-color: rgba(255, 255, 255, 0.1);
            text-align: center;
            transition: 0.3s;
        }
        .movie-card:hover {
            background-color: rgba(255, 255, 255, 0.2);
            transform: scale(1.05);
        }
        .movie-title {
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
            color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)


# -------------------------------
# Poster Fetch Functions
# -------------------------------
def fetch_from_omdb(movie_title):
    try:
        encoded_title = urllib.parse.quote(movie_title)
        url = f"http://www.omdbapi.com/?t={encoded_title}&apikey={OMDB_API_KEY}"
        data = requests.get(url).json()
        if data.get("Response") == "True":
            return data.get("Poster") if data.get("Poster") != "N/A" else None
        else:
            return None
    except:
        return None


def fetch_poster(movie_title):
    return fetch_from_omdb(movie_title)


# -------------------------------
# Recommendation Function
# -------------------------------
def recommend(movie):
    movie_index = int(movies[movies['title'] == movie].index[0])
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))
    return recommended_movies, recommended_posters


# -------------------------------
# Load similarity and movie data
# -------------------------------
similarity = pickle.load(open("similarity.pkl", "rb"))
movie_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movie_dict)

# -------------------------------
# Streamlit UI
# -------------------------------
st.markdown("<h1 class='title'>🎬 VERONICA - Movie Recommender</h1>", unsafe_allow_html=True)

# Select movie
selected_movie_name = st.selectbox(
    "Select a movie:",
    movies["title"].values
)

# Show recommendations
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    st.markdown("<h2 class='recommend-title'>✨ Top 5 Recommendations ✨</h2>", unsafe_allow_html=True)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"<div class='movie-card'>", unsafe_allow_html=True)
            if posters[idx]:
                st.image(posters[idx], use_container_width=True)
            st.markdown(f"<div class='movie-title'>{names[idx]}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
