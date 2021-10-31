from nltk.tokenize import WhitespaceTokenizer
from collections import Counter
import random
import re
import json

def create_template(file_name):
    with open(fr'sources\{file_name}.txt', "r", encoding="utf-8") as f:
        tokens = WhitespaceTokenizer().tokenize(f.read())

    just_a_list = [[f"{tokens[x]} {tokens[x + 1]}", tokens[x + 2]] for x in range(len(tokens) - 2)] # [['The Dead.', "You've"], ...]

    my_dict = {}
    for elem in just_a_list:
        my_dict.setdefault(elem[0], []).append(elem[1]) # {'The Dead.': ["You've", 'The', 'None', 'We']}

    for elem in my_dict:
        my_dict[elem] = dict(Counter(my_dict[elem]))  # {'The Dead.': {"You've": 1, 'The': 1, 'None': 1, 'We': 2}}

    with open(fr'sources\{file_name}_template.txt', "w", encoding="utf-8") as f:
        f.write(json.dumps(my_dict))

    return my_dict

# Выбор первых слов. Первое слово должно начинаться с заглавной буквы и не заканчиваться знаком препинания.
def first_word_generator(choices: list):
    while True:
        words = random.choice(choices)
        if re.match("[A-Z]\w+\Z", words.split(" ")[0]) is not None:
            return words

def run(name, num):
    try:
        print('Открываю файл...')
        with open(fr'sources\{file_name}_template.txt', "r", encoding="utf-8") as f:
            temp = json.loads(f.read())
        print('Файл найден и прочитан')
    except FileNotFoundError:
        print('Такой файл не обнаружен. Создаю новый...')
        temp = create_template(name)
        print('Файл создан')
    finally:
        print()
        for _ in range(int(num)):
            sentence = ""
            begin = first_word_generator(list(temp.keys())) # The Dead.
            sentence += begin 
            while True:
                choice = temp[begin] # {"You've": 1, 'The': 1, 'None': 1, 'We': 2}}
                new_word = random.choices(list(choice.keys()), weights=list(choice.values()))[0] # We
                begin = begin.split(" ")[1] + " " + new_word  # Dead. We
                sentence = sentence + " " + new_word  # The Dead. We
                if (re.match("\w+[!.?]+\Z", new_word) is not None) and (len(sentence.split(" ")) >= 5):
                    break
            print(sentence)


if __name__ == '__main__':
    file_name = input('Enter filename:\n')
    number = input('Enter number of sentences:\n')
    run(file_name, number)