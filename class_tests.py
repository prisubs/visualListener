from spotifyuser import SpotifyUser
from build_vizdata import *

# construct test user
genius_key = "0AGGE0X9UYCDMkHxZWHojX0uBIaoHNZCQbfJO8hFx0g7nj9OJYEPJl2NzdBDdgtJ"
user_url_short = "https://open.spotify.com/user/priankasubs?si=dIr00M7sQUuZ4fUdbkuBnw"
user_url_long = "https://open.spotify.com/user/31obw73wcndofulfje4bekzfyccy?si=gVDUwqejRByytdPWaWtS7A"

# represents @priankasubs test user
x = SpotifyUser(user_url_short, genius_key)
x.user_summary()

df = x.clean_and_merge_dfs()
print(languages_weighted(df))
print(artists_weighted(df))

# topic modeling
text_data = lda_composite(df)
print(text_data)
