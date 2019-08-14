import scraping
from pandas import DataFrame


class SpotiPyPlaylistClient:

    def __init__(self, genius_key):
        self.genius_authkey = genius_key
        self.lyrics_cached = DataFrame()

    def playlist_lyrics(self, url):
        lyrics_df = scraping.playlist_df(url, self.genius_authkey)
        self.lyrics_cached = lyrics_df
        return lyrics_df

    @staticmethod
    def user_playlists(url):
        return scraping.user_dict(url)

    def custom_lyrics(self, lyrics_list):
        num_songs = len(lyrics_list)

        try:
            lyrics_df = DataFrame({"lyrics": lyrics_list})
            self.lyrics_cached = lyrics_df
            print("Successfully cached {0} songs.".format(num_songs))

        except:
            return "Your lyrics data was not formatted properly."


