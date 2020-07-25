# dictionaries of data ready for visualization
# all in dictionaries of key: FDG weight
# takes in original cleaned df from SpotifyUser
import pandas as pd
import spacy
spacy.load('en_core_web_sm')
from spacy.lang.en import English
parser = English()
import nltk

from nltk.corpus import wordnet as wn
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# get list of languages and their weights
def languages_weighted(df):
    result = df["lang"].value_counts()
    return result.to_dict()
nltk.download('wordnet')
# gets list of artists and their weights
def artists_weighted(df):
    # artists separated by commas in SpotifyUser df
    artists = df["artist"].tolist()
    artists = [txt.split(", ") for txt in artists]
    flattened_artists = [y for x in artists for y in x]
    flattened_artists = pd.Series(flattened_artists)
    return flattened_artists.value_counts().to_dict()

def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

from nltk.stem.wordnet import WordNetLemmatizer
def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))

def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

def lda_composite(df):
    text_data = []
    f = df["lyrics"].tolist()
    for line in f:
        tokens = prepare_text_for_lda(line)
        text_data.append(tokens)
