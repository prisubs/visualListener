from scraping import *
from language import *

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

    # combine all playlist songs into one df
    def clean_and_merge_dfs(self):
        df_dict = self.playlist_data
        dfs = []
        for df in df_dict:
            dfs.append(df_dict[df])

        df = pd.concat(dfs)
        df = df.drop_duplicates(subset = "title", keep = False, inplace = False)

        return transform(df)

