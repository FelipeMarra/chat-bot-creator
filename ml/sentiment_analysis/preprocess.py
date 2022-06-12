from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer

import re
import string
import numpy as np

# removing undesired substrigns
def preprocess_tweet(tweet):
    stemmer = PorterStemmer()
    stopwords_en = stopwords.words('english')

    #print('\033[92m' + tweet)

    # remove stock market tickers, old rt, hyperlinks, hash sign
    tweet = re.sub(r'\$\w*', '', tweet)
    tweet = re.sub(r'^RT[\s]+', '', tweet)
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
    tweet = re.sub(r'#', '', tweet)

    # tokenize
    # preserve_case => downcase everything
    # strip_handles => removes @s (user handles)
    # reduce_len => removes repetitive letters
    tokenizer = TweetTokenizer(
        preserve_case=False, strip_handles=True, reduce_len=True)
    tweet_tokens = tokenizer.tokenize(tweet)

    # remove stopwords, ponctuation and perform steamming
    tweet_clean = []

    for word in tweet_tokens:
        if (word not in stopwords_en and word not in string.punctuation):
            stem_word = stemmer.stem(word)
            tweet_clean.append(stem_word)

    return tweet_clean
