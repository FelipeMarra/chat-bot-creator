import random
import re
import numpy as np
from collections import Counter
import pandas as pd

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
print("100%")
ALPHA = 1
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ALPHABET_W_UPER = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

TEST_FILE_W_ERROR = f"./data/test.words.{ALPHA*100}_error"
TEST_FILE_W_CORRECTION = f"{TEST_FILE_W_ERROR}_correted"

def append_line(new_line):
    with open(TEST_FILE_W_CORRECTION, 'r') as file:
        content = file.readlines()
        content.append(new_line)

    with open(TEST_FILE_W_CORRECTION, 'w') as file:
        file = file.writelines(content)

#pegando o dataset de teste
testing_file = open(TEST_FILE_W_ERROR, 'r')
testing_file_lines = testing_file.readlines()

#Criando dataset com erros
arquivo = open(TEST_FILE_W_CORRECTION, 'w')
arquivo.close()

#Até chegar no final do arquivo faça:
for line in testing_file_lines:
    word = line.split()
    if(len(line.split()) != 0):
        corrected_word = run_autocorrect(word[0])
    else:
        corrected_word = ""
    #Escrever nova linha novo arquivo de testes
    append_line(f"{corrected_word}\n")