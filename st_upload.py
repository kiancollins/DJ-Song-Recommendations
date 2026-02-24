import streamlit as st
import pandas as pd
import numpy as np
from clean_dataset import *
from mixability import *


st.set_page_config(layout="wide")
st.title("DJ Song Recommendation")

if "df" not in st.session_state:        # Initialize a df variable for session state, 
    st.session_state.df = None          # we will rewrite later with the cleaned dataframe  

music_csv = st.file_uploader(f"Upload Music", type=["csv"])     # Upload music CSV

df = None       # Initialize a "df" variable
if music_csv:                               
    raw_df = pd.read_csv(music_csv) 
    df = clean_data(raw_df)

    if isinstance(df, pd.DataFrame):
        st.success("Music data uploaded and cleaned")
    else:
        st.error(df)         # Check output of df because an error will return a string

if isinstance(df, pd.DataFrame):
    print(df.head(5))
    st.dataframe(df)                        # Display dataframe
    st.session_state.df = df                # Set df in the session state (use for the next page)


    if st.button("Next →"):
        st.switch_page("pages/st_main.py")      # "Next" button to move to the main part of program






