from http.client import responses

import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/' + str(movie_id) +'?api_key=' + os.getenv("TMDB_API_KEY").format(movie_id))
    data = response.json()
    path = ""
    for key, value in data.items():
        if key == "poster_path":
            path = value

    return "https://image.tmdb.org/t/p/w500/" + path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = i[0]
        recommended_movies.append(movies.iloc[movie_id].title)
        recommended_movies_posters.append(fetch_poster(movies.iloc[movie_id].movie_id))

    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('model/movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('model/similarity.pkl', 'rb'))
st.title('Movie Recommender')

selected_movie_name = st.selectbox(
    'How would you like to predict?',
    (movies['title'].values)
)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)


    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
