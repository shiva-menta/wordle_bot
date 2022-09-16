import string
import csv
import requests

url = "https://wordsapiv1.p.rapidapi.com/words/"

headers = {
	"X-RapidAPI-Key": "cf5f9da48fmshbf6b132f0b1a3e0p1226e7jsn27b9f98304d7",
	"X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
}

alphabet_list = list(string.ascii_lowercase)

def get_wordlist_from_api(letter_pattern) :
    query_len = 5 - len(letter_pattern)
    querystring = {"letterPattern": f"^{letter_pattern}.{{{query_len}}}$",
                   "letters": "5"}

    response = requests.request("GET", url, headers=headers, params=querystring)
    word_array = response.json()["results"]["data"]
    return(word_array)

def add_array_to_csv(arr) :
    with open("./word-list.csv", 'a', newline='') as csvfile:
        wordwriter = csv.writer(csvfile, delimiter=" ", quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for word in arr :
            if word.isalpha() :
                wordwriter.writerow([word])

def collect_all_words() :
    for first in alphabet_list :
        for second in alphabet_list :
            word_arr = get_wordlist_from_api(str(first + second))
            if word_arr is not None :
                add_array_to_csv(word_arr)
                

f = open('./word-list.csv', 'w+')
f.close()
collect_all_words()



