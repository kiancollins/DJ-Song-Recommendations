import pandas as pd
import numpy as np
from clean_dataset import *
from mixability import *
from typing import Tuple
from utils import *


def get_song(track: str, artist: str, df: pd.DataFrame) -> Tuple[pd.Series, int]:
    """ Using the track and artist names, we can grab the exact series and index. 
        We can use this for better usability. The user can just input the track name and artist.
        
        The function runs character matching to find the most similar track/artist to the input
        Then scores the similarity of all of them and returns the top match."""
    
    track = normalize_track(track)
    artist = normalize_artist(artist)     # Normalize tracks using the functions from util.py

    
    song_search = df[["track", "artist"]].copy()
    song_search["track_norm"] = song_search["track"].map(normalize_track)
    song_search["artist_norm"] = song_search["artist"].map(normalize_artist)    # New dataframe with the normalized names

    song_search["track_similarity"] = song_search["track_norm"].map(
                                        lambda x: char_match(track, x))
    song_search["artist_similarity"] = song_search["artist_norm"].map(
                                        lambda x: char_match(artist, x)) # Run character match on all tracks & artists

    song_search["song_similarity"] = (song_search["track_similarity"] * 
                                      song_search["artist_similarity"]) # Add a column with total track & artist similarity
    
    sorted_similarity = song_search.sort_values("song_similarity", ascending=False)  # Sort by song similarity

    closest_match = sorted_similarity.iloc[0]
    idx = closest_match.name    # Grab index

    return closest_match, idx




def main():
    popular = pd.read_csv("data/popular_songs.csv")
    df = clean_data(popular)
    
    track = "disease"
    artist = "lady gaga"
    result, idx = get_song(track, artist, df)
    print(result, idx)

if __name__ == "__main__":
    main()




