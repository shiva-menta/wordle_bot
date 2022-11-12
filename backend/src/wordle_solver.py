# imports
import requests
import string
import csv
import os
import math
import pathlib
from itertools import product
from datetime import date, datetime
from collections import Counter
from typing import List
from lxml import html

import firebase_admin
from firebase_admin import credentials, firestore

# global variables
total_word_list = []

# constants
start_date = date(2019, 6, 12)
endgame_threshold = 3
URL = """https://www.nytimes.com/games-assets/v2/wordle.1b4655b170d30c964441b7
08a4e22b3e617499a1.js"""



# Timestamp Printing Functions
def write_file(filename,data):
    if os.path.isfile(filename):
        with open(filename, 'a') as f:          
            f.write('\n' + data)   
    else:
        with open(filename, 'w') as f:                   
            f.write(data)
 
def print_time():   
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    data = "Current Time = " + current_time
    return data




# Word Sourcing Functions
def read_in_word_list() -> None: # reads in all five-letter words
    file = open(pathlib.Path(__file__).parent / 'word-list.csv','r')
    for word in file.readlines():
        total_word_list.append(word.strip())
    
    file.close()

def return_highest_frequency_word(word_list: List[str]) -> str: # returns the word with the highest word frequency
    freq = float('-inf')
    word = None

    file = open(pathlib.Path(__file__).parent / 'word-frequency-data.csv')
    csvreader = csv.reader(file)
    for row in csvreader:
        arr = row[0].split(' ')
        if arr[0] in word_list and arr[1] != "Missing['NotAvailable']":
            if float(arr[1]) > freq:
                freq = float(arr[1])
                word = arr[0]
    file.close()
    return word




# NYT Wordle Data Functions
def source_and_clean_wordle_text_dump() -> str: # get Wordle answer data from NYT site
    page = requests.get(URL)
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

def read_answer_array_into_csv(lst: List[str]) -> None: # writes given list data into answers.csv
    with open('./answers.csv', 'a', newline='') as csvfile:
        wordwriter = csv.writer(csvfile, delimiter=" ", quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if lst is None:
            return
        for word in lst.split(','):
            cln_word = word[1:-1]
            wordwriter.writerow([cln_word])


# old
def get_todays_word_sitesource() -> str: # returns today's Wordle answer
    curr_date = date.today()
    csv_row = abs(curr_date - start_date).days

    file = open(pathlib.Path(__file__).parent / 'answers.csv', 'r')
    todays_word = file.readlines()[csv_row].strip()
    file.close()

    return todays_word

# updated
def get_todays_word_unofficial() -> str: # returns today's Wordle answer
    page = requests.get('https://tryhardguides.com/wordle-answers/')
    tree = html.fromstring(page.content)
    hidden_word = tree.xpath('//span[@class="hidden-text d-none"]//strong/text()')
    return hidden_word[0].lower()




# Template Generation / Filtering Functions
def get_all_template_types() -> List[str]: # returns all word template types
    return [''.join(temp) for temp in product('xyg', repeat=5)]

def get_all_possible_template_types(template: str) -> List[str]: # returns all template types possible with locked green letters
    green_indices = set()
    ret_strings = []

    for i in range(5):
        if template[i] == 'g':
            green_indices.add(i)

    
    non_green_len = len(set([0,1,2,3,4]).difference(green_indices))

    green_indices = list(green_indices)
    green_indices.sort()

    ret = [list(''.join(temp)) for temp in 
        product('xyg', repeat=non_green_len)]

    for temp in ret:
        for ind in green_indices:
            temp.insert(ind, 'g')
    
    for temp in ret:
        ret_strings.append(''.join(temp))
    
    return ret_strings

def get_answer_template(guess: str, answer: str) -> str: # returns the word template that represents a guess on the answer
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

def word_matches_template(guess: str, word: str, template: str) -> bool: # checks if a word matches a given template
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
                if key == guess[ind]:
                    return False
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

def filter_words(word: str, template: str, word_arr: List[str]) -> List[str]: # returns a list of words that matches a given template
    return list(filter(lambda guess: word_matches_template(guess, 
        word, template), word_arr))




# Best Guess Functions
def expected_value(denom: int, numer: int) -> float: # helper function for quantifying most optimal guess
    if numer:
        return (numer / denom) * -1 * math.log((numer / denom), 2)
    return 0

def calc_best_guess_data() -> None: # calculates expected value for each word and writes to best-words.csv
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
        print(ans)

    file = open('./best-words.csv', 'w')
    file.close()
    with open('./best-words.csv', 'a', newline='') as csvfile:
        wordwriter = csv.writer(csvfile, delimiter=" ", quotechar='|', 
            quoting=csv.QUOTE_MINIMAL)
        for ind, word in enumerate(word_list):
            wordwriter.writerow([word, exp_val[ind]])

def get_best_first_guess() -> str: # returns the best guess based on expected value data
    exp = float('-inf')
    word = None

    file = open(pathlib.Path(__file__).parent / 'best-words.csv')
    csvreader = csv.reader(file)
    for row in csvreader:
        arr = row[0].split(' ')
        if float(arr[1]) > exp:
            exp = float(arr[1])
            word = arr[0]
    file.close()

    return word

def find_cond_best_guess(template: str, word_list: List[str]) -> str: # returns the best guess given a template and word list (for intermediate guesses)
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




# Full Game Code
def play_full_game(ans=get_todays_word_unofficial()):
    guess_arr = []
    temp_arr = []
    curr = None

    read_in_word_list()
    word_list = total_word_list
    temp = 'xxxxx'

    while curr != ans and len(guess_arr) <= 6:
        print(curr)

        if len(guess_arr) == 0:
            curr = get_best_first_guess()
        elif len(word_list) <= endgame_threshold:
            curr = return_highest_frequency_word(word_list)
        else:
            curr = find_cond_best_guess(temp, word_list)
        
        guess_arr.append(curr)
        
        temp = get_answer_template(curr, ans)

        temp_arr.append(temp)

        if curr == ans:
            break

        word_list = filter_words(curr, temp, word_list)

    return guess_arr, temp_arr

def get_num_guesses(templates: List[str]) -> int:
    if templates[-1] == 'ggggg':
        return len(templates)
    else:
        return 7


# Executed Code
cred = credentials.Certificate(pathlib.Path(__file__).parent.parent / 'serviceAccountKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
words, templates = play_full_game()
db.collection('daily-game').add({'date': firestore.SERVER_TIMESTAMP, 'guesses': 
    words, 'guess_templates': templates, 'attempts': get_num_guesses(templates)})

write_file(pathlib.Path(__file__).parent / 'timestamp.txt', print_time())


# Crontab previous command
# 0 12  * * * cd /Users/shivamenta/repos/wordle_bot/src && /Users/shivamenta/opt/anaconda3/bin/python wordle_solver.py