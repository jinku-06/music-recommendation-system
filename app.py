# Download spotify songs dataset from https://www.kaggle.com/datasets/notshrirang/spotify-million-song-dataset and name it spotify_millsongdata.csv

import pickle
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import os


CLIENT_ID = "YOUR_SPOTIFY_CLIENT_ID"
CLIENT_SECRET = "YOUR_SPOTIFY_CLIENT_SECRET"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="https://example.com",
        cache_path="token.txt",
        show_dialog=True,
    )
)


def get_song_cover_url(song_name, artist_name):
    search = f"track: {song_name}, artist: {artist_name}"
    results = sp.search(q=search, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        img_url = track["album"]["images"][0]["url"]
        print(img_url)
        return img_url
    else:
        return "https://www.shutterstock.com/image-illustration/no-picture-available-placeholder-thumbnail-icon-2226533863"


def recommend(song):
    index = music[music["song"] == song].index[0]
    distance = sorted(list(enumerate(similer[index])), reverse=True, key=lambda x: x[1])
    names = []
    posters = []

    for i in distance[1:6]:
        artist = music.iloc[i[0]].artist
        song_name = music.iloc[i[0]].song
        print(artist, song_name)
        names.append(song_name)
        posters.append(get_song_cover_url(song_name, artist))

    return names, posters


st.header("Music Recommender System")
music = pickle.load(open("df.pkl", "rb"))
similer = pickle.load(open("similarity.pkl", "rb"))

music_list = music["song"].values
select_song = st.selectbox("Type or select a song from the dropdown", music_list)

if st.button("Show Recommendation"):
    names, posters = recommend(select_song)

    cols = st.columns(5)

    for i in range(len(names)):
        with cols[i % 5]:
            st.text(names[i])
            st.image(posters[i], width=120)
