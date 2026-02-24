import pandas as pd
import numpy as np
from clean_dataset import *


REMOVE_WORDS = ["remix", "edit", "version", "mix", "remaster", "live", "feat", "ft"]


def normalize_track(track):
    """ Remove any extra words in track name that could cause confusion during search. """
    lower = str(track).lower()                  # 1. Make it a str and all lowercase

    for w in REMOVE_WORDS:
        lower = lower.replace(w, "")    # 2. Replace any extra words
    
    shortened = str(lower).split("-")[0]        # 3. Cut off anything after "-" if it exists
    shortened = str(shortened).split("(")[0]        # 4. Cut off anything after "(" if it exists

    clean = str(shortened).strip().replace(" ", "").replace("_", "").replace("-", "").replace(".", "")  
    return clean                                # 5. ^ Remove any other extra puncuation


def normalize_artist(artist):
    """ Normalize artist name. Strip, make all lower case, and remove any extra puncuation"""
    clean = str(artist).strip().lower().replace(" ", "").replace("_", "").replace("-", "").replace(".", "")
    shortened = str(clean).split(",")[0]        # Cut off anything after "," if it exists

    return shortened


def char_match(target: str, possible: str):
    """ Returns a score of how close two words are based on matching characters. 
        The inputted words should be normalized beforehand based on the type (track, artist)"""   

    target_list = list(target)
    possible_list = list(possible)      # Turn words into lists
    unmatched_list = []

    for char in possible_list:
        if char in target_list:
            target_list.remove(char)
        else:
            unmatched_list.append(char)
        
    total_possible = len(target) + len(possible)
    total = len(unmatched_list) + len(target_list)
    score = 1 - (total / total_possible)
    return score




def main():
    popular = pd.read_csv("data/popular_songs.csv")
    df = clean_data(popular)
    
    song = df.loc[1]
    print(song)
    song_track = song["track"]
    song_artist = song["artist"]
    print(song_track, song_artist)

    track = "BIRDS OF A FEATHER - Lady Gaga remix"
    artist = "Bille eilish"

    test1 = char_match(track, song_track)
    test2 = char_match(artist, song_artist)

    print(test1, test2)


if __name__ == "__main__":
    main()
