import sys
from preprocess import preprocess_tweet
from freqs_table import FreqsTable

def predict(tweet):
    db = FreqsTable()
    
    words = preprocess_tweet(tweet)

    probability = 0

    probability += db.get_utils()[0]
    

    for word in words:
        loglikelihood = db.get_loglikelihood(word)

        probability += loglikelihood
        
    if probability >= 1:
        sentiment = 'positive'
    
    else:
        sentiment = 'negative'
        
    return probability, sentiment