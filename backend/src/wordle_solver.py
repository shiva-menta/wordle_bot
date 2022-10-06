import requests
import string
import csv
import os
import math
from datetime import date
from collections import Counter

URL = "https://www.nytimes.com/games-assets/v2/wordle.1b4655b170d30c964441b708a4e22b3e617499a1.js"
page = requests.get(URL)
start_date = date(2021, 6, 19)
endgame_threshold = 3



def expected_value(denom, numer):
    return (numer / denom) * -1 * math.log((numer / denom), 2)

def get_all_template_types():
    template_type = ['x', 'y', 'g']
    ret = []

    for first in template_type:
        for second in template_type:
            for third in template_type:
                for fourth in template_type:
                    for fifth in template_type:
                        ret.append(first+second+third+fourth+fifth)
    
    return ret

def filter_words(word, template, word_arr):
    return list(filter(lambda guess: word_matches_template(guess, word, template), word_arr))

# checks that a given guess would be valid given a word template
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
    
    if len(gray_stor) == 5:
        return False

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
            
def get_answer_template(guess, answer):
    return_list = ['x'] * 5
    stor = Counter(answer)

    for i in range(5):
        if guess[i] == answer[i]:
            return_list[i] = 'g'
            del stor[answer[i]]

    for i in range(5):
        if guess[i] in stor.keys():
            return_list[i] = 'y'
            del stor[guess[i]]

    return ''.join(return_list)

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

def read_answer_array_into_csv(lst):
    with open('./answers.csv', 'a', newline='') as csvfile:
        wordwriter = csv.writer(csvfile, delimiter=" ", quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if lst is None:
            return
        for word in lst.split(','):
            cln_word = word[1:-1]
            wordwriter.writerow([cln_word])

def get_todays_word():
    curr_date = date.today()
    csv_row = abs(curr_date - start_date).days

    file = open('./answers.csv', 'r')
    todays_word = file.readlines()[csv_row].strip()

    print(todays_word)

def play_full_game(ans):
    guess_arr = []
    curr = None

    # Read CSV Data into Array
    word_list = None

    while curr != ans and len(guess_arr) <= 6:
        curr = get_best_guess(word_list)
        guess_arr.append(curr)

        word_list = filter_words(curr, get_answer_template(curr, ans), word_list)

    return guess_arr

def find_best_guess(arr):
    denom = len(arr)
    best_arr = [0] * len(arr)
    exp = 0

    for index, word in range(len(arr)):
        for temp in get_all_template_types():
            exp += expected_value(denom, len(filter_words(word, temp, arr)))
        
        best_arr[index] = exp
        exp = 0

    return max(best_arr)

    # for every word, use filter_words on every word template and calculate expected 


# filter_words("crane", "xxyxg", ['alike','ranch','strre','saute','alive'])
# print(get_answer_template("shiee", "icert"))
# read_answer_array_into_csv(source_and_clean_wordle_text_dump())
# get_todays_word()
# print(word_matches_template('smart','stara','gyggx'))
print(filter_words('eeeee','xxxxx',['shiva', 'hello', 'smart', 'group']))