import numpy as np
import pandas as pd

REQUIRED_COLS = ["track_name", "track_artist", "playlist_genre", "tempo", "key", 
                    "energy", "track_popularity", "danceability", "liveness"]


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """ Input a Spotify API dataframe and output a cleaned version that we can 
        easily use for our program."""
    
    missing = []
    for col in REQUIRED_COLS:
        if col not in df.columns:
            missing.append(col)
    if len(missing) > 0:
        return f"Missing Columns: {missing}"

    df = df[["track_name", "track_artist", "playlist_genre", "tempo", "key", 
                               "energy", "track_popularity", "danceability", "liveness"]]
    df = df.rename(columns={"track_name": "track", "track_artist": "artist",
                                              "playlist_genre": "genre", "track_popularity": "popularity"})

    df["popularity"] *= 0.01
    df["danceability"] = df["danceability"].round(2)
    df["liveness"] = df["liveness"].round(2)
    df["energy"] = df["energy"].round(2)
    df["tempo"] = df["tempo"].round()
    # print(df)
    return df


def main():
    popular_songs = pd.read_csv("popular_songs.csv")
    cleaned = clean_data(popular_songs)
    print(cleaned.head(5))

if __name__ == "__main__":
    main()
