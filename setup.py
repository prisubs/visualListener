import setuptools

long_des =  '''
 Spotify-based lyrics analytics client for Python, written with the help of lyricsgenius. 
 This supports several functionalities for reading and analyzing playlist data, as well as 
 performing NLP functions on lyrics text.
'''

setuptools.setup(
    name="spotipy-playlist",
    version="1",
    author="Prianka Subrahmanyam",
    author_email="prianka.subrahmanyam@gmail.com",
    description="Spotify lyrics analytics client",
    long_description=long_des,
    long_description_content_type="text/markdown",
    url="https://github.com/prisubs/spotipy-playlist",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)