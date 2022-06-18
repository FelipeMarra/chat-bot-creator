import numpy as np
from predict import predict as naive_bayes_predict
import nltk
from nltk.corpus import twitter_samples

#get tweets
nltk.download('twitter_samples')

corpora_root = 'C:/Users/felip/AppData/Roaming/nltk_data/corpora/twitter_samples/'

all_positive_tweets = twitter_samples.strings(corpora_root + 'positive_tweets.json')
all_negative_tweets = twitter_samples.strings(corpora_root + 'negative_tweets.json')

#put them togheter
tweets = all_negative_tweets + all_negative_tweets

#get ys
pos_size = len(all_positive_tweets)
neg_size = len(all_negative_tweets)
ys = np.append(np.ones(pos_size), np.zeros(neg_size))

#get train and test
test_pos = all_positive_tweets[4000:]
test_neg = all_negative_tweets[4000:]

test_x = test_pos + test_neg

# avoid assumptions about the length of all_positive_tweets
test_y = np.append(np.ones(len(test_pos)), np.zeros(len(test_neg)))

def test_naive_bayes(test_x, test_y):
    accuracy = 0  # return this properly

    y_hats = []
    for tweet in test_x:
        # if the prediction is > 0
        if naive_bayes_predict(tweet)[0] > 0:
            # the predicted class is 1
            y_hat_i = 1
        else:
            # otherwise the predicted class is 0
            y_hat_i = 0

        # append the predicted class to the list y_hats
        y_hats.append(y_hat_i)

    # error is the average of the absolute values of the differences between y_hats and test_y
    error = np.mean(np.absolute(y_hats-test_y))

    # Accuracy is 1 minus the error
    accuracy = 1-error

    ### END CODE HERE ###
    print(accuracy)

    return accuracy

print("Naive Bayes accuracy = %0.4f" %
(test_naive_bayes(test_x, test_y)))