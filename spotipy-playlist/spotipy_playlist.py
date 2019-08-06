import scraping


class SpotiPyPlaylistClient:

    def __init__(self, genius_key):
        self.genius_authkey = genius_key

    def playlist_lyrics(self, url):
        return scraping.playlist_df(url, self.genius_authkey)

    @staticmethod
    def user_playlists(url):
        return scraping.user_dict(url)