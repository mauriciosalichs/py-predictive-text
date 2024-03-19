import os
import pickle

file_path = "dictionary.pkl"
punctuations = [',', '.', '-', '_', ';', ':', '?', '!', '¡', '¿', ' ', '(', ')']

class CharDict:
    def __init__(self, char):
        self.char = char
        self.next_favorite = ''
        self.next_favorite_count = 0
        self.maps = {'': [0, None]} # Char -> ( Int, CharDict() )

    def construct_mapping(self, word):
        for letter in word:
            if not letter in self.maps:
                self.maps[letter] = [0, CharDict(letter)]
            self.maps[letter][0] += 1
            if self.maps[letter][0] > self.next_favorite_count:
                self.next_favorite_count = self.maps[letter][0]
                self.next_favorite = letter
            self = self.maps[letter][1]
        self.next_favorite = ''
        self.next_favorite_count = 20
        self.maps[''] = [20, None]
        
    def process_word(self, word):
        for letter in word:
            if letter in punctuations:
                continue
            [count, next_chars]  = self.maps[letter]
            count += 1
            if count > self.next_favorite_count:
                self.next_favorite = letter
                self.next_favorite_count = count
            self.maps[letter][0] = count
            self = self.maps[letter][1]
        if '' not in self.maps:
            return
        [count, next_chars]  = self.maps['']
        count += 5
        if count > self.next_favorite_count:
            self.next_favorite = ''
            self.next_favorite_count = count
        self.maps[''][0] = count
        
        

def process_words_from_file(file_path):
    dictionary = CharDict('')
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()  # Remove leading/trailing whitespaces
            dictionary.construct_mapping(word)
    return dictionary
    
def process_word(dict, word):
    dict.process_word(word)
    return dict
    
def calculate_predictive_word(dict, word):
    if word == '':
        return (dict,'',False)
    for letter in word[:-1]:
        dict = dict.maps[letter][1]
    return calculate_predictive_letter(dict, word[-1])
    
def calculate_predictive_letter(dict, letter):
    predicted_text = ''
    if letter not in dict.maps:
        dict.maps[letter] = [1, CharDict(letter)]
    else:
        iter_char = dict.maps[letter][1]
        while iter_char and iter_char.maps:
            next_letter = iter_char.next_favorite
            if next_letter == '': break
            predicted_text += next_letter
            iter_char = iter_char.maps[next_letter][1]
    return (dict.maps[letter][1],predicted_text,True)

def get_dictionary():
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    else:
        return process_words_from_file('words.txt')
        
def get_punctuations():
    return punctuations