# dictionaries of data ready for visualization
# all in dictionaries of key: FDG weight
# takes in original cleaned df from SpotifyUser
import pandas as pd


# get list of languages and their weights
def languages_weighted(df):
    result = df["lang"].value_counts()
    return result.to_dict()


# gets list of artists and their weights
def artists_weighted(df):
    # artists separated by commas in SpotifyUser df
    artists = df["artist"].tolist()
    artists = [txt.split(", ") for txt in artists]
    flattened_artists = [y for x in artists for y in x]
    flattened_artists = pd.Series(flattened_artists)
    return flattened_artists.value_counts().to_dict()




