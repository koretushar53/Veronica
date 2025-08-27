import pandas as pd
import streamlit as st
import pickle
import requests
import urllib.parse

# 🔑 OMDb API Key
OMDB_API_KEY = "c9b16384"   # replace with your own key if needed

# -------------------------------
# Poster Fetch Functions
# -------------------------------
def fetch_from_omdb(movie_title):
    try:
        # Encode title for URL safety
        encoded_title = urllib.parse.quote(movie_title)
        url = f"http://www.omdbapi.com/?t={encoded_title}&apikey={OMDB_API_KEY}"
        data = requests.get(url).json()

        # Debugging (optional - uncomment if needed)
        # st.write(f"OMDb query for {movie_title} → {url}")
        # st.write("OMDb response:", data)

        if data.get("Response") == "True":
            return data.get("Poster") if data.get("Poster") != "N/A" else None
        else:
            return None
    except:
        return None


def fetch_poster(movie_title):
    # Only OMDb is used here
    poster = fetch_from_omdb(movie_title)
    return poster


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
st.title("🎬 Movie Recommender System (OMDb Posters)")

# Select movie
selected_movie_name = st.selectbox(
    "Select a movie:",
    movies["title"].values
)

# Show recommendations
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    st.subheader("Top 5 Recommendations:")
    cols = st.columns(5)  # 5 posters side by side
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            if posters[idx]:
                st.image(posters[idx])
            else:
                st.warning("Poster not available")
