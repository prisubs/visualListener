import pandas as pd
import musical_stop_words

from sklearn.feature_extraction.text import CountVectorizer

STOPWORDS = musical_stop_words.stop


def keywords(corpus, n):
    cv = CountVectorizer(max_df=0.7,
                         ngram_range=(1, 3),
                         stop_words=STOPWORDS)

    count_vector = cv.fit_transform(corpus)
    most_common = list(cv.vocabulary_.keys())[:n]

    return most_common

