# wordle-bot
Automatic Wordle solver bot that guesses a mystery 5-letter word in optimal 
time.

Problem Statement:
Wordle is an online game in which users try to guess a five letter word. A new 
word is uploaded daily.

A user is given six guesses per round. After each guess, a user is told how
much information they have correct. A yellow character indicates that the
letter is in the word but in the wrong position. A green character indicates
that the letter is in the word AND is in the correct position. A gray character
indicates that the letter is not in the word.

A user's goal is to guess the correct word in the fewest number of attempts.
Wordle also has two modes: normal and hard mode. In Hard Mode, all information
sourced previously has to be used in subsequent guesses (e.g. yellow and
green letters). We will be 'playing' in Wordle Hard Mode.

Algorithm Logic:
Taking inspiration from 3Blue1Brown, our algorithm will depend on information
theory.

In brief terms, given a pool of existing words, the optimal guess is the one
that contains the highest expected value of information. The expected value
is calculated by multiplying two terms: the probability of getting a certain
word template multiplied by the amount of information that we can source from
it. We'll dive a bit deeper into each term below.

1: Word Template – There are a total of 3^5 different word templates we can
have in Wordle, each composed of different combinations of gray, yellow, and
green letters. If we calculate the expected value for each of these word
template possibilities, we'll be able to assess the strength of each word
guess.

2: Amount of Information (bits) – We'll quantify the amount of information
we're getting using bits. A bit of information corresponds to the power of 2
associated with the number of words we're cutting down to for future guesses.
For example, if my original word pool has 4 words, and we cut it down to 2
words with our guess, we can say that our guess had 1 bit of information (cut
down by a factor of 2^1). Another way of quantifying a bit is considering how
many times our available word pool is cut down by half.

Now that we've explained both terms, we'll simply use our Python scripts
to calculate the optimal guess at each round until a guess is made. 

To make the bot perform even better, I added an endgame solution parameter of
N = 3. Essentially, once the word pool is N = 2,3, the Wordle bot will choose
the word that has the highest frequency according to word usage data. The pool
of Wordle answers is relatively small (~2000), and they're generally the most
frequently used / common five-letter words. For this reason, once we reach a
small enough word pool, we'll select our next guess using this method.

With this, our logic is complete. Hope you enjoy the project :)

Data Sources:
I sourced the list of all possible words using WordsAPI. Word frequency
data was collected using Wolfram's WordFrequency Data function.
