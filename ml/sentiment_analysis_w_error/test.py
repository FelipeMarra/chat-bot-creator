import numpy as np
from predict import predict as naive_bayes_predict
import nltk
from nltk.corpus import twitter_samples
from apply_error import apply_error
import re  
from collections import Counter
import pandas as pd
import string

############ AUTORCORRECT #####################
w = []
with open('shakespeare.txt','r',encoding="utf8") as f:
    file_name_data = f.read()
    file_name_data = file_name_data.lower()
    w = re.findall('\w+', file_name_data)

v = set(w)

def get_count(words):
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

def get_probs(word_count_dict):
    probs = {}
    m = sum(word_count_dict.values())
    for key in word_count_dict.keys():
        probs[key] = word_count_dict[key] / m
    return probs

def DeleteLetter(word):
    delete_list = []
    split_list = []
    for i in range(len(word)):
        split_list.append((word[0:i], word[i:]))
    for a, b in split_list:
        delete_list.append(a + b[1:])
    return delete_list

def SwitchLetter(word):
    split_l = []
    switch_l = []
    for i in range(len(word)):
        split_l.append((word[0:i], word[i:]))
    switch_l = [a + b[1] + b[0] + b[2:] for a, b in split_l if len(b) >= 2]
    return switch_l

def replace_letter(word):
    split_l = []
    replace_list = []
    for i in range(len(word)):
        split_l.append((word[0:i], word[i:]))
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    replace_list = [a + l + (b[1:] if len(b) > 1 else '') for a, b in split_l if b for l in alphabets]
    return replace_list

def insert_letter(word):
    split_l = []
    insert_list = []
    for i in range(len(word) + 1):
        split_l.append((word[0:i], word[i:]))
    letters = 'abcdefghijklmnopqrstuvwxyz'
    insert_list = [a + l + b for a, b in split_l for l in letters]
    return insert_list

def edit_one_letter(word, allow_switches=True):
    edit_set1 = set()
    edit_set1.update(DeleteLetter(word))
    if allow_switches:
        edit_set1.update(SwitchLetter(word))
    edit_set1.update(replace_letter(word))
    edit_set1.update(insert_letter(word))
    return edit_set1

def edit_two_letters(word, allow_switches=True):
    edit_set2 = set()
    edit_one = edit_one_letter(word, allow_switches=allow_switches)
    for w in edit_one:
        if w:
            edit_two = edit_one_letter(w, allow_switches=allow_switches)
            edit_set2.update(edit_two)
    return edit_set2

def get_corrections(word, probs, vocab, n=2):
    suggested_word = []
    best_suggestion = []
    suggested_word = list(
        (word in vocab and word) or edit_one_letter(word).intersection(vocab) or edit_two_letters(word).intersection(
            vocab))
    best_suggestion = [[s, probs[s]] for s in list(reversed(suggested_word))]
    return best_suggestion

def run_autocorrect(my_word):
    try:
        ndx = w.index(my_word)
    except:
        ndx = -1

    if(ndx != -1):
        return my_word
    else:
        word_count = get_count(w)
        probs = get_probs(word_count)
        tmp_corrections = get_corrections(my_word, probs, v, 2)
        max_prob = 0
        index = 0
        for j, word_prob in enumerate(tmp_corrections):
            if word_prob[1] > max_prob:
                index = j
                max_prob = word_prob[1]
        if len(tmp_corrections) != 0:
            return str(tmp_corrections[index][0])
        else:
            return my_word
###########################################################################

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
        tweet = apply_error(tweet)
        new_tweet = ""

        for word in tweet.split():
            skip = False
            for letter in word:
                if letter in string.punctuation:
                    skip = True
                    break
            if skip:
                new_tweet = f"{new_tweet} {word}"
            else:
                new_tweet = f"{new_tweet} {run_autocorrect(word)}"

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