from scraping import *

class SpotifyUser:
    def __init__(self, url, genius_key):
        self.name = scrape_name(url)
        self.playlist_metadata = pull_user_playlists(url)
        self.num_playlists = len(self.playlist_metadata.index)
        self.playlist_data = playlist_datagrab(self.playlist_metadata, genius_key)

    # print summary
    def user_summary(self):
        print("User: {}".format(self.name))
        print("Number of playlists: {}".format(self.num_playlists))
        playlists = self.playlist_metadata["playlist_name"].tolist()

        print("Playlists")
        print("**************")
        for i in range(1, self.num_playlists + 1):
            print("{0}. {1}".format(i, playlists[i-1]))
