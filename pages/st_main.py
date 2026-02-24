import streamlit as st
import pandas as pd
import numpy as np
from clean_dataset import *
from mixability import *
from get_song import *
from utils import *
from sort_songs import *

print("Session state keys:", list(st.session_state.keys()))
st.set_page_config(layout="wide")
st.title("DJ Song Recommendation")
  

df = st.session_state.get("df")             # Grab the all songs dataframe from last page/run
if df is None:
    st.error("Upload music first")
    st.stop()

if "played" not in st.session_state:
    st.session_state.played = pd.DataFrame(columns=df.columns)

played = st.session_state.played


st.text("All Songs")
st.dataframe(df)
st.text("Played Songs")
st.dataframe(played)


def enter_song():
    df = st.session_state.df
    played = st.session_state.played
    track = st.session_state.track_in
    artist = st.session_state.artist_in

    match, idx = get_song(track, artist, df)
    song = df.loc[idx]

    df, played = run_mixability_scores(song, df, played)

    st.session_state.df = df
    st.session_state.played = played

    #Reset inputs (allowed inside callback)
    st.session_state.track_in = ""
    st.session_state.artist_in = ""


track = st.text_input("Track Name", "", key="track_in")
# artist = st.text_input("Artist Name", "", key="artist_in")
artist = st.text_input(
    "Artist Name",
    "",
    key="artist_in",
    on_change=enter_song
)



st.button("Enter", on_click=enter_song)


