# functions to build input for visualizations
from textblob import TextBlob
import re
import pycountry


# translate identified non-english text
def to_english(lyr, lang):
    if lang == 'en':
        return lyr
    else:
        blob = TextBlob(lyr)
        translation = blob.translate(to='en')
        return str(translation)


# identify non-english text, return detected language
def detect_lang(lyr):
    blob = TextBlob(lyr)
    lang = blob.detect_language()
    return lang


# fix languages on each row of df
def lang_transform(df):
    df['lang'] = df["lyrics"].apply(detect_lang)
    df["english_lyrics"] = df.apply(lambda x: to_english(x['lyrics'], x['lang']), axis=1)
    return df


# regex to remove anything in brackets
def clean_musical_indicators(lyrics):
    lyric_capture = r"\[.*?\]"
    result = re.sub(lyric_capture,'', lyrics)
    return result


# fix all the newlining
def fix_newlines(lyrics):
    newline_capture = r"\s+"
    result = re.sub(newline_capture, ' ', lyrics)
    return result


# change language codes to full language name
def full_lang(iso_code):
    lang = pycountry.languages.get(alpha_2=iso_code)
    return str(lang.name)


# apply all cleaning functions
def clean_lyrics(df):
    df["lyrics"] = df["english_lyrics"].apply(clean_musical_indicators)
    df["lyrics"] = df["lyrics"].apply(fix_newlines)
    df["lyrics"] = df["lyrics"].apply(str.lower)
    df = df.drop(["english_lyrics"], axis=1)
    df["lang"] = df["lang"].apply(full_lang).apply(str.lower)
    return df


# apply basic (non-NLP) transformations
def transform(df):
    df = lang_transform(df)
    df = clean_lyrics(df)
    return df
