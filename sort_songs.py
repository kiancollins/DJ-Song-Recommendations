import pandas as pd
import numpy as np
from clean_dataset import *
from mixability import *
from typing import Tuple



def run_mixability_scores(current: pd.Series, df: pd.DataFrame, played: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """ This function inputs the current song, and the full dataframe of songs it is in,
        and outputs a new dataframe with all the songs sorted by mixability score. 
        
        We also remove the current song, and add it to the "played" dataframe, so we 
        can keep track of what songs we already played. This avoids repeats, but also 
        avoids fully removing the song from our list
        """
    new = df.copy()
    new["mixability"] = 0.0 # Create copy of DataFrame, and insert a new column

    
    mask = ((new["track"] == current["track"]) &
            (new["artist"] == current["artist"]))       # Grab the current song (and any copies of it)
    result = new.loc[~mask]                             # Our dataframe exclues the current song (and any copies of it)




    for idx, candidate in result.iterrows():                    # Set mixability score of each song
        mixability = run_mixability(current, candidate)
        result.loc[idx, "mixability"] = mixability
    
    result = result.sort_values("mixability", ascending=False)  # Sort by mixability

    current = current.drop("mixability", errors="ignore")                   # Remove mixability score if it has one
    played = pd.concat([played, current.to_frame().T], ignore_index=True)   # Add to our df of played songs

    
    return result, played






def main():
    popular_songs = pd.read_csv("popular_songs.csv")
    cleaned = clean_data(popular_songs).iloc[:10]
    played = pd.DataFrame(columns=cleaned.columns)

    current = cleaned.loc[1]
    sorted, played = run_mixability_scores(current, cleaned, played)

    sorted = sorted.drop(columns=["artist"])

    print(current)
    print(sorted.head(10))
    print(played.head(1))



if __name__ == "__main__":
    main()




