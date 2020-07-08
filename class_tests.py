from spotifyuser import SpotifyUser

# construct test user
genius_key = "0AGGE0X9UYCDMkHxZWHojX0uBIaoHNZCQbfJO8hFx0g7nj9OJYEPJl2NzdBDdgtJ"
user_url = "https://open.spotify.com/user/priankasubs?si=dIr00M7sQUuZ4fUdbkuBnw"

# represents @priankasubs test user
x = SpotifyUser(user_url, genius_key)
x.user_summary()
