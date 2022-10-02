import requests
import string
import csv
import os
from datetime import date

URL = "https://www.nytimes.com/games-assets/v2/wordle.1b4655b170d30c964441b708a4e22b3e617499a1.js"
page = requests.get(URL)
start_date = date(2021, 6, 19)

def filter_words(guess, template, word_list):
    template_array = list(template)
    guess_array = list(guess)
    green_indices = []
    contains_list = []
    cleaned_words_list = []

    # Reading through template.
    for i in range(5):
        if template_array[i] == "y":
            contains_list.append(str(guess_array[i]))
        if template_array[i] == "g":
            green_indices.append(i)

    for word in word_list:
        word_bool = True

        # Filters out words that don't match green letters.
        if green_indices :
            for index in green_indices:
                if guess[int(index)] == word[int(index)] :
                    word_bool = word_bool and True
                else :
                    word_bool = False
                    break
        
        # Filters out words that don't contain yellow letters.
        if word_bool and contains_list :
            for char in contains_list:
                if char in word:
                    word_bool = word_bool and True
                else :
                    word_bool = word_bool and False
        
        # Adds word to return list.
        if word_bool:
            cleaned_words_list.append(word)

    print(cleaned_words_list)
            
def get_answer_template(guess, answer):
    guess_array = list(guess)
    answer_array = list(answer)
    return_list = []

    for i in range(5):
        if guess_array[i] == answer_array[i]:
            return_list.append("g")
        elif guess_array[i] in answer_array:
            return_list.append("y")
        else :
            return_list.append("x")

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




def source_todays_word():
    
    return


# filter_words("crane", "xxyxg", ['alike','ranch','strre','saute','alive'])
# print(get_answer_template("racea", "raesh"))
# read_answer_array_into_csv(source_and_clean_wordle_text_dump())
get_todays_word()
