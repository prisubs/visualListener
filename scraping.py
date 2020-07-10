import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import lyricsgenius
from lxml import html


# constructs dataframe for a user playlist
def playlist_df(url, genius_key):
    titles = scrape_titles(url)
    artists = scrape_artists(url)

    df = pd.DataFrame({
        "title": titles,
        "artist": artists,
    })

    df["lyrics"] = df.apply(lambda x: grab_song(x.title, x.artist, genius_key), axis=1)

    return df


# lyrics for a song and artist pair
def grab_song(title, artist, key):
    genius = lyricsgenius.Genius(key)
    song = genius.search_song(title, artist)

    if song:
        return str(song.lyrics)
    elif artist == "":
        return "no lyrics found"
    else:
        return grab_song(title, "", key)


# Base scraping function
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


# Titles for a single playlist
def scrape_titles(query):
    song_titles = scrape_something(query, "track-name")
    return song_titles


# Artists for a single playlist
def scrape_artists(query):
    artists = scrape_something(query, "artists-albums")
    artists = artists.apply(clean_artists)
    return artists


# Cleaning the dot and extra space around artist name
def clean_artists(artist_name):
    x = artist_name.split("•")[0]
    return re.sub('\s+', ' ', x).strip()


# Name for a single user
def scrape_name(query):
    name = scrape_something(query, "view-header", single_val=True)
    return name


# List of playlist titles and URLs (for further analysis) for a single user
def scrape_user_playlists(query):
    playlists = scrape_something(query, "cover playlist")
    return playlists


# use a regex to clean out extraneous urls + construct full url list
def process_playlist_urls(urls):
    spotify_base = "https://open.spotify.com"
    cleaned = []
    for url in urls:
        if re.findall(r"\/playlist\/.*", url):
            cleaned.append(url)
    cleaned = [spotify_base + url for url in cleaned]
    return cleaned


# dynamically construct playlist URLs by finding them on user's profile
def pull_user_playlists(url):
    playlist_names = scrape_user_playlists(url)

    # get playlist urls
    page = requests.get(url)
    webpage = html.fromstring(page.content)
    urls = webpage.xpath('//a/@href')

    spotify_base = "https://open.spotify.com"
    cleaned = []
    for url in urls:
        if re.findall(r"\/playlist\/.*", url):
            cleaned.append(url)
    cleaned = [spotify_base + url for url in cleaned]
    df = pd.DataFrame(list(zip(playlist_names, cleaned)), columns =['playlist_name', 'playlist_url'])
    return df


# get lyrics and data for playlists given df of names and urls
def playlist_datagrab(df, token):
    urls = df["playlist_url"].tolist()
    result = {}
    for url in urls:
        p_df = playlist_df(url, token)
        result[url] = p_df
    return result
