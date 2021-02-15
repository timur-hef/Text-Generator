from nltk.tokenize import WhitespaceTokenizer
from collections import Counter
import random
import re

#file_name = input()

my_file = open("corpus.txt", "r", encoding="utf-8")

tokens = WhitespaceTokenizer().tokenize(my_file.read())
just_a_list = [[f"{tokens[x]} {tokens[x + 1]}", tokens[x + 2]] for x in range(len(tokens) - 2)]

my_dict = {}
for elem in just_a_list:
    my_dict.setdefault(elem[0], []).append(elem[1])

for elem in my_dict:
    my_dict[elem] = dict(Counter(my_dict[elem]))


def first_word_generator(choices):
    while True:
        words = random.choice(choices)
        if re.match("[A-Z]\w+\Z", words.split(" ")[0]) is not None:
            return words


for i in range(10):
    sentence = ""
    begin = first_word_generator(list(my_dict.keys()))
    sentence += begin
    while True:
        temp_dict = my_dict[begin]
        new_word = random.choices(list(temp_dict.keys()), weights=list(temp_dict.values()))[0]
        begin = begin.split(" ")[1] + " " + new_word
        sentence = sentence + " " + new_word
        if (re.match("\w+[!.?]+\Z", new_word) is not None) and (len(sentence.split(" ")) >= 5):
            break
    print(sentence)