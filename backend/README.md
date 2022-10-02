# wordle-bot
Automatic Wordle solver bot that chooses the optimal guess at every opportunity.

Problem Statement:
Every day, a random five-letter word is chosen and the user is given 6 guesses.
The program aims to choose the most optimal word possible at every guess,
maximizing letters used and avoiding reguesses of existing letters. Each
guess will need to take into account which letters have been guessed, which
letters have a confirmed position, which letters are in the word but in an
incorrect position.

We have a csv file with all five-letter words to be considered. Data must be 
loaded in a way such that each guess can quickly evaluate the word with the
most likely answer (most common letters based on available positions).

Steps To Take:
- Filtering array of words to exclude words with already guessed letters.

- Filtering array of words to include words with 'yellow' letters.

- Filtering array of words to include words with 'green' letters in specific positions.

- Collect words that have highest frequency in each position and choose the most 
- optimal word in a subset. (get_optimal_word(arr))

Potential Data Storage + SearchStrategies:
Ideas: 2D Arrays, HashMaps, Tries