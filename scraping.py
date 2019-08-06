import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import lyricsgenius

'''
Constructs a dataframe for a playlist
'''
def playlist_df(url, genius_key):

    titles = scrape_titles(url)
    artists = scrape_artists(url)

    df = pd.DataFrame({
        "title": titles,
        "artist": artists,
    })

    df["lyrics"] = df.apply(lambda x: grab_song(x.title, x.artist, genius_key), axis=1)

    return df

'''
Constructs a dictionary for a user
'''
def user_dict(url):
    name = scrape_name(url)
    playlists = scrape_user_playlists(url).tolist()

    return {
        "name": name,
        "playlists": playlists
    }

'''
Grabs lyrics for a single song and artist pair
'''
def grab_song(title, artist, key):

    genius = lyricsgenius.Genius(key)
    song = genius.search_song(title, artist)

    if song:
        return str(song.lyrics)
    elif artist == "":
        return "no lyrics found"
    else:
        return grab_song(title, "")


'''
Base scraping function, no-frills
'''
def scrape_something(url, classname, single_val=False):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    result = soup.find_all(class_ = classname)
    result = pd.Series(result).apply(str)

    html_cleaner = lambda text: re.sub("<.*?>", "", text)
    result = result.apply(html_cleaner)

    if single_val:
        return result[0]
    else:
        return result


'''
Titles for a single playlist
'''
def scrape_titles(query):

    song_titles = scrape_something(query, "track-name")
    return song_titles


'''
Artists for a single playlist
'''
def scrape_artists(query):

    artists = scrape_something(query, "artists-albums")
    artists = artists.apply(clean_artists)
    return artists


'''
Cleaning the dot and extra space around artist name
'''
def clean_artists(artist_name):

    x = artist_name.split("•")[0]
    return re.sub('\s+', ' ', x).strip()


'''
Name for a single user
'''
def scrape_name(query):

    name = scrape_something(query, "view-header", single_val=True)
    return name


'''
List of playlist titles for a single user
'''
def scrape_user_playlists(query):

    playlists = scrape_something(query, "cover playlist")
    return playlists

