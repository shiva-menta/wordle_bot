import requests
import string
import csv
import os
import math
from itertools import product
from datetime import date
from collections import Counter

import heapq
from operator import itemgetter

URL = "https://www.nytimes.com/games-assets/v2/wordle.1b4655b170d30c964441b708a4e22b3e617499a1.js"
page = requests.get(URL)
start_date = date(2021, 6, 19)
total_word_list = []
endgame_threshold = 3

# helper function for quantifying most optimal guess
def expected_value(denom, numer):
    if numer:
        return (numer / denom) * -1 * math.log((numer / denom), 2)
    return 0

# returns all word template types
def get_all_template_types():
    return [''.join(temp) for temp in product('xyg', repeat=5)]

# returns all template types possible with locked green letters
def get_all_possible_template_types(template):
    green_indices = set()
    ret_strings = []

    for i in range(5):
        if template[i] == 'g':
            green_indices.add(i)

    
    non_green_len = len(set([0,1,2,3,4]).difference(green_indices))

    green_indices = list(green_indices)
    green_indices.sort()

    ret = [list(''.join(temp)) for temp in product('xyg', repeat=non_green_len)]

    for temp in ret:
        for ind in green_indices:
            temp.insert(ind, 'g')
    
    for temp in ret:
        ret_strings.append(''.join(temp))
    
    return ret_strings

# returns a list of words that matches a given template
def filter_words(word, template, word_arr):
    return list(filter(lambda guess: word_matches_template(guess, word, template), word_arr))

# checks if a word matches a given template
def word_matches_template(guess, word, template):
    green_indices = set()
    yel_stor = {}
    gray_stor = set()

    for count, letter in enumerate(template):
        if letter == 'g':
            green_indices.add(count)
        elif letter == 'y':
            yel_stor[word[count]] = yel_stor.get(word[count], []) + [count]
        else:
            gray_stor.add(word[count])

    pot_yel_ind = set([0,1,2,3,4]).difference(green_indices)

    if green_indices:
        for index in green_indices:
            if guess[index] != word[index]:
                return False

    if yel_stor:
        for key, val in yel_stor.items():
            act_ind = val

            check_ind = pot_yel_ind.copy()
            for ind in act_ind:
                check_ind.remove(ind)
            
            for ind in check_ind:
                if key == guess[ind] and act_ind:
                    act_ind.pop()

            if act_ind:
                return False
    
    if gray_stor:
        for ind in pot_yel_ind:
            if guess[ind] in gray_stor:
                return False

    return True

# returns the word template that represents a guess on the answer
def get_answer_template(guess, answer):
    return_list = ['x'] * 5
    stor = Counter(answer)
    green_indices = set()

    for i in range(5):
        if guess[i] == answer[i]:
            return_list[i] = 'g'
            green_indices.add(i)
            if stor[guess[i]] > 1:
                stor[guess[i]] -= 1
            else:
                stor[guess[i]] -= 1
                del stor[guess[i]]
    
    pot_yel_ind = set([0,1,2,3,4]).difference(green_indices)

    if pot_yel_ind:
        pot_yel_ind = list(pot_yel_ind)
        pot_yel_ind.sort()

        for i in pot_yel_ind:
            if guess[i] in stor.keys():
                return_list[i] = 'y'
                if stor[guess[i]] > 1:
                    stor[guess[i]] -= 1
                else:
                    stor[guess[i]] -= 1
                    del stor[guess[i]]

    return ''.join(return_list)

# get Wordle answer data from NYT site
def source_and_clean_wordle_text_dump():
    key = [',ft=[','],bt']
    start = end = 0

    file = open('wordle_dump.txt', 'w')
    file.close()
    with open('wordle_dump.txt', 'w') as f:
        f.write(page.text)
    file = open('wordle_dump.txt')
    first_line = file.readlines()[0]
    start = first_line.find(key[0]) + 5
    end = first_line.find(key[1])

    return(first_line[start:end])

# writes given list data into answers.csv
def read_answer_array_into_csv(lst):
    with open('./answers.csv', 'a', newline='') as csvfile:
        wordwriter = csv.writer(csvfile, delimiter=" ", quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if lst is None:
            return
        for word in lst.split(','):
            cln_word = word[1:-1]
            wordwriter.writerow([cln_word])

# returns today's Wordle answer (used internally)
def get_todays_word():
    curr_date = date.today()
    csv_row = abs(curr_date - start_date).days

    file = open('./src/answers.csv', 'r')
    todays_word = file.readlines()[csv_row].strip()
    file.close()

    return todays_word

# reads in all five-letter words
def read_in_word_list():
    file = open('./src/word-list.csv','r')
    for word in file.readlines():
        total_word_list.append(word.strip())
    
    file.close()

# calculates expected value for each word and writes to best-words.csv
def calc_best_guess_data():
    word_list = total_word_list
    denom = len(word_list)
    exp_val = [0] * denom
    template_dict = {}

    for temp in get_all_template_types():
        template_dict[temp] = 0
    exp = 0
    
    for ind, ans in enumerate(word_list):
        for guess in word_list:
            template_dict[get_answer_template(guess, ans)] += 1
        
        for key in template_dict:
            exp += expected_value(denom, template_dict[key])
        
        exp_val[ind] = exp
        template_dict = dict.fromkeys(template_dict, 0)
        exp = 0

        # print(ans)
    
    # read into file
    file = open('./src/best-words.csv', 'w')
    file.close()
    with open('./src/best-words.csv', 'a', newline='') as csvfile:
        wordwriter = csv.writer(csvfile, delimiter=" ", quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for ind, word in enumerate(word_list):
            wordwriter.writerow([word, exp_val[ind]])

# returns the best guess given a template and word list (for intermediate guesses)
def find_cond_best_guess(template, word_list):
    denom = len(word_list)
    exp_val = [0] * denom
    template_dict = {}

    for temp in get_all_possible_template_types(template):
        template_dict[temp] = 0
    exp = 0

    for ind, ans in enumerate(word_list):
        for guess in word_list:
            template_dict[get_answer_template(guess, ans)] += 1
        
        for key in template_dict:
            exp += expected_value(denom, template_dict[key])
        
        exp_val[ind] = exp
        template_dict = dict.fromkeys(template_dict, 0)
        exp = 0

    return word_list[exp_val.index(max(exp_val))]

# returns the best guess based on expected value data (TEST)
def get_best_first_guess():
    exp = float('-inf')
    word = None

    file = open('./src/best-words.csv')
    csvreader = csv.reader(file)
    for row in csvreader:
        arr = row[0].split(' ')
        if float(arr[1]) > exp:
            exp = float(arr[1])
            word = arr[0]
    file.close()

    return word

# returns the word with the highest word frequency
def return_highest_frequency_word(word_list):
    freq = float('-inf')
    word = None

    file = open('./src/word-frequency-data.csv')
    csvreader = csv.reader(file)
    for row in csvreader:
        arr = row[0].split(' ')
        if arr[0] in word_list and arr[1] != "Missing['NotAvailable']":
            if float(arr[1]) > freq:
                freq = float(arr[1])
                word = arr[0]
    file.close()
    return word

# full game playing function
def play_full_game(ans=get_todays_word()):
    guess_arr = []
    curr = None

    read_in_word_list()
    word_list = total_word_list
    temp = 'xxxxx'

    while curr != ans and len(guess_arr) <= 6:
        if len(guess_arr) == 0:
            curr = get_best_first_guess()
        elif len(word_list) <= endgame_threshold:
            curr = return_highest_frequency_word(word_list)
        else:
            curr = find_cond_best_guess(temp, word_list)
        
        guess_arr.append(curr)

        if curr == ans:
            break
        
        temp = get_answer_template(curr, ans)

        word_list = filter_words(curr, temp, word_list)

    return guess_arr

print(play_full_game())