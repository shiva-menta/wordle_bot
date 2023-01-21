# imports
import os
import sys
import string
import csv
import requests
from typing import List

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..' )
sys.path.append( mymodule_dir )
import config

# constants
alphabet_list = list(string.ascii_lowercase)

# api related info
url = "https://wordsapiv1.p.rapidapi.com/words/"
headers = {
	"X-RapidAPI-Key": config.wordle_api_key,
	"X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
}


# Words API Data Sourcing (no longer being used)
def get_wordlist_from_api(letter_pattern: int) -> List[int]: # make letter pattern request to api
    query_len = 5 - len(letter_pattern)
    querystring = {"letterPattern": f"^{letter_pattern}.{{{query_len}}}$",
                   "letters": "5"}

    response = requests.request("GET", url, headers=headers, params=querystring)
    word_array = response.json()["results"]["data"]
    return(word_array)

def add_array_to_csv(arr: List[int]) -> None: # add array of words to csv
    with open("./word-list.csv", 'a', newline='') as csvfile:
        wordwriter = csv.writer(csvfile, delimiter=" ", quotechar='|', 
            quoting=csv.QUOTE_MINIMAL)
        for word in arr :
            if word.isalpha() :
                wordwriter.writerow([word])

def collect_all_words() -> None: # add all words to csv
    for first in alphabet_list :
        for second in alphabet_list :
            word_arr = get_wordlist_from_api(str(first + second))
            if word_arr is not None :
                add_array_to_csv(word_arr)


# Word Frequency Data Sourcing
def get_word_frequency_data() -> None: # reads in word frequency data to csv
    word_list = []

    file = open('./src/word-list.csv','r')
    for word in file.readlines():
        word_list.append(word.strip())
    file.close()
    
    file = open('./src/word-frequency-data.csv', 'w')
    file.close()

    session = WolframLanguageSession('''/Applications/Wolfram Engine.app/Contents/Resources/Wolfram Player.app/Contents/MacOS/WolframKernel''')

    with open('./src/word-frequency-data.csv', 'a', newline='') as csvfile:
        wordwriter = csv.writer(csvfile, delimiter=" ", quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for word in word_list:
            print(word)
            obj = session.evaluate(wl.WordFrequencyData([word]))

            csv_line = []
            for key in obj.keys(): csv_line.append(key)
            for value in obj.values(): csv_line.append(value)

            wordwriter.writerow(csv_line)

    session.terminate()


# Executed Code
get_word_frequency_data()



