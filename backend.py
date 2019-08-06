import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import lyricsgenius
import numpy as np
import os
import textblob
import indicoio

# genius
GENIUS_KEY = "0AGGE0X9UYCDMkHxZWHojX0uBIaoHNZCQbfJO8hFx0g7nj9OJYEPJl2NzdBDdgtJ"
INDICO_KEY = "345e9dbbeafeed418903dac43945c766"

def playlist_title(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = str(soup.find_all(class_="media-bd")[0])
    return re.sub("<.*?>", "", title)

def scrape_titles(query):
    page = requests.get(query)
    soup = BeautifulSoup(page.content, 'html.parser')

    song_titles = pd.Series(soup.find_all(class_ = "track-name"))
    song_titles = song_titles.apply(str)
    html_cleaner = lambda title: re.sub("<.*?>", "", title)
    song_titles = song_titles.apply(html_cleaner)
    return song_titles

def scrape_artists(query):
    page = requests.get(query)
    soup = BeautifulSoup(page.content, 'html.parser')
    artists = pd.Series(soup.find_all(class_ = "artists-albums"))
    artists = artists.apply(lambda title: re.sub("<.*?>", "", str(title)))
    return artists

def clean_artists(artist_name):
    x = artist_name.split("•")[0]
    return re.sub('\s+', ' ', x).strip()

def query_song(title, artist):
    genius = lyricsgenius.Genius(GENIUS_KEY)
    song = genius.search_song(title, artist)
    if song:
        return song.lyrics
    elif artist == "":
        return "no lyrics found"
    else:
        return query_song(title, "")

def playlist_df(url):
    titles = scrape_titles(url)
    artists = scrape_artists(url).apply(clean_artists)
    df = pd.DataFrame({"song": titles, "artist": artists})
    df["lyrics"] = df.apply(lambda x: query_song(x.song, x.artist), axis=1)
    return df

def standardize(lyrics):
    clean1 = lambda lyric: re.sub(r"[^\w\d\'\s]+", '', lyric)
    clean2 = lambda lyric: re.sub(r'[0-9]+', '', lyric)
    lyrics = clean1(lyrics)
    lyrics = clean2(lyrics)
    lyrics = str.lower(lyrics)
    return lyrics

def remove_musical_words(lyrics):
    r = "(chorus|hook|intro|verse|bridge|outro|part|ft|feat)"
    lyrics = re.sub(r, "", lyrics)
    return lyrics


def stop_word_remover(lyric):
    words = lyric.split()
    result = ""
    for word in words:
        if not (word in STOP_WORDS):
            result += word + " "
    return result

def clean(lyric):
    lyric = standardize(lyric)
    lyric = remove_musical_words(lyric)
    return lyric

def english(lyric):
    blob = textblob.TextBlob(lyric)
    language = blob.detect_language()
    return language == 'en'

def translator(lyric):
    blob = textblob.TextBlob(lyric)
    if not english(lyric):
        result = blob.translate(to='en')
        return str(result)
    else:
        return lyric

def drop_records(df):
    df = df.loc[df["lyrics"] != "no lyrics found", :]
    df = df.loc[df["cleaned"].apply(english), :]
    return df

def driver(url):
    df = playlist_df(url)
    df["cleaned"] = df["lyrics"].apply(clean)
    df["no_stop"] = df["cleaned"].apply(stop_word_remover)
    df = drop_records(df)
    # still needs a lot more here

    # returns an array of urls of predictions
    return ["https://picsum.photos/id/502/200/200", "https://picsum.photos/id/268/200/200"]

