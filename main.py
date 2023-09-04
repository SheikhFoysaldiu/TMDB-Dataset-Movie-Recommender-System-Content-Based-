import streamlit as st
import pandas as pd
import pickle
import requests

df = pd.read_pickle("movie.pkl")
similarity = pickle.load(open("similarity.pkl",'rb'))

def fetchPoster(movieID):
    res = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=e2cf243a0a49c983df69a350ba2ab0af".format(movieID))
    data = res.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
    

def recommend(movie):
  movie_index = df[df['title'] == movie].index[0]
  distance = similarity[movie_index]
  movies_list = sorted(list(enumerate(distance)),reverse=True,key=lambda x: x[1])[1:6]
  
  recommendedMovie = []
  recommendedMoviePoster = []
  for i in movies_list:
    movieID = df.iloc[i[0]].movie_id                                                
    recommendedMovie.append(df.iloc[i[0]].title)

    recommendedMoviePoster.append(fetchPoster(movieID))
    #st.title(fetchPoster(movieID))
    
  return recommendedMovie,recommendedMoviePoster

    

    

st.title("Movie Recommender System")

option = st.selectbox("Select",df['title'])

if st.button('Recommend'):
    recommendedMovie,recommendedMoviePoster = recommend(option)

    for id,name in enumerate(recommendedMovie):
        st.title(name)
        st.image(recommendedMoviePoster[id],width=300)
