import pandas as pd
import numpy as np
from clean_dataset import *

SUB_WEIGHTS = {"tempo": 0.45,
           "energy": 0.1,
           "key": 0.35,
           "popularity": 0.6,
           "danceability": 0.35,
           "liveness": 0.05
            }

WEIGHTS = {"closeness": 0.6,
           "ranking": 0.4}


def tempo_score(current: int, candidate: int) -> float:
    """ Grades the similarity in tempo between 2 songs.
        
        Since tempo is a very important feature that shouldn't have a linear rating, 
        I created a system for grading tempo. Songs close enougha and within a specific zone
        are treated the same, while songs far away are not scored. """
    perfect = 3
    good = 5
    okay = 7
    maximum = 10
    weights = {"perfect": 1.0, 
               "good": 0.7,
               "okay": 0.5,
               "maximum": 0.2,
               }
    diff = abs(current-candidate)
    
    if diff <= perfect:
        return weights["perfect"]
    elif diff <= good:
        return weights["good"]
    elif diff <= okay:
        return weights["okay"]
    elif diff <= maximum:
        return weights["maximum"]
    return 0.0


def energy_score(current: float, candidate: float) -> float:
    """ Grades the similarity in energy between 2 songs."""
    diff = abs(current - candidate)
    score = float(1 - diff)
    return score


def key_score(current: int, candidate: int) -> float:
    """ Grades the similarity in key between 2 songs.
        Key ranges from 0 - 11, so we should think of it a wheel split into 2, with 6 sections on each side.
            ie. 0 and 1 are the same distance as 0 and 11, 
                and the furthest possible difference is 6.
        And if the furthest distance is 6, then we can calculate our score on a scale of 0-6.
        """
    
    raw_diff = abs(current - candidate)
    circular_diff = min(raw_diff, 12-raw_diff)
    score = float(1 - (circular_diff/6))
    return score


def closeness_score(tempo: float, energy: float, key: float) -> float:
    """Calculates the final score of the closeness categories (tempo, energy, key)"""
    weighted_tempo = tempo * SUB_WEIGHTS["tempo"]
    weighted_energy = energy * SUB_WEIGHTS["energy"]
    weighted_key_score = key * SUB_WEIGHTS["key"]
    final_score = weighted_tempo + weighted_energy + weighted_key_score
    # print(final_score)
    return final_score


def ranking_score(popularity: float, danceability: float, liveness: float) -> float:
    """ Calculates the final score of the ranking categories (popularity, danceability, liveness)"""
    weighted_popularity = popularity * SUB_WEIGHTS["popularity"]
    weighted_danceability = danceability * SUB_WEIGHTS["danceability"]
    weighted_liveness = liveness * SUB_WEIGHTS["liveness"]
    final_score = weighted_popularity + weighted_danceability + weighted_liveness
    # print(final_score)
    return final_score

def mixability_score(closeness: float, ranking: float) -> float:
    """ Combines the closeness and ranking scores to return our final mixability score"""
    mixability = (closeness * WEIGHTS["closeness"]) + (ranking * WEIGHTS["ranking"])
    return mixability


def run_mixability(current: pd.Series, candidate: pd.Series) -> float:
    """ Implementation of each of the previous tests to output a final mixability score for each song"""
    tempo = tempo_score(current["tempo"], candidate["tempo"])
    energy = energy_score(current["energy"], candidate["energy"])
    key = key_score(current["key"], candidate["key"])
    
    closeness = closeness_score(tempo, energy, key)
    ranking = ranking_score(candidate["popularity"], candidate["danceability"], candidate["liveness"])
    mixability = round(mixability_score(closeness, ranking), 2)
    # print(mixability)
    # return f"{current["track"]} -> {candidate["track"]} has score of {mixability}"
    return mixability




def main():
    popular = pd.read_csv("data/popular_songs.csv")
    df = clean_data(popular)
    
    song_1 = df.loc[1]
    for idx, candidate in df.iloc[:20].iterrows():
        print(run_mixability(song_1, candidate))


if __name__ == "__main__":
    main()






