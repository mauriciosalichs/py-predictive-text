import os
import pickle

file_path = "dictionary.pkl"

class CharDict:
    def __init__(self, char):
        self.char = char
        self.next_favorite = ''
        self.next_favorite_count = 0
        self.maps = {'': None} # Char -> ( Int, CharDict() )

    def construct_mapping(self, word):
        for letter in word:
            if not letter in self.maps:
                new_char = [0, CharDict(letter)]
                self.maps[letter] = new_char
            self = self.maps[letter][1]
            
    def process_word(self, word):
        for letter in word+'':
            if letter == ' ' or letter == ',' or letter == '.':
                continue
            [count, next_chars]  = self.maps[letter]
            count += 1
            if count > self.next_favorite_count:
                self.next_favorite = letter
                self.next_favorite_count = count
            self.maps[letter][0] = count
            self = self.maps[letter][1]
        

def process_words_from_file(file_path):
    dictionary = CharDict('')
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()  # Remove leading/trailing whitespaces
            dictionary.construct_mapping(word)
    return dictionary
    
def process_word(dictionary, word):
    dictionary.process_word(word)
    return dictionary

def get_dictionary():
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    else:
        return process_words_from_file('words.txt')