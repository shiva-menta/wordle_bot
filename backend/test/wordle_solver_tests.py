import unittest
from wordle_bot.src.wordle_solver import *

class TestWordFilter(unittest.TestCase):
    def setUp(self):
        self.my_first_guess = "crane"
        self.my_first_guess_duplicates = "reeks"

    def assertFilter(self):
        self.assertEquals(get_answer_template(self.my_first_guess, "recap"), "yyyxy")

if __name__ == '__main__':
    unittest.main()