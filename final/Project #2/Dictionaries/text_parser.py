#Luka Lipovac and Ostap Voynarovsky
#Natural Language Processing - Project #2: Auto-Correct
#April 9th, 2018

#Run with: python text_parser.py path_to_texts_folder old_dictionary.txt new_dictionary.txt

import argparse
import os
import nltk
import operator

#Parse input
parser = argparse.ArgumentParser()
parser.add_argument("texts_path")
parser.add_argument("old_dictionary")
parser.add_argument("new_dictionary")
args = parser.parse_args()


frequency_dictionary = {}

#Fill dict with old dictionary
with open(args.old_dictionary, 'r') as f:
    for line in f:
        word = line.split()[0]
        frequency_dictionary[word] = int(line.split()[1])

#Read all files in folder
i = 0
for file in os.listdir(args.texts_path):
    print(i)
    i+=1
    path = os.path.abspath(args.texts_path)
    with open(os.path.join(path, file), 'r', encoding='iso-8859-1') as f:
        for line in f:
            for sentence in nltk.sent_tokenize(f.read().lower()):
                for word in nltk.word_tokenize(sentence):
                    if word.isalpha():
                        if word in frequency_dictionary:
                            frequency_dictionary[word] += 1
                        else:
                            frequency_dictionary[word] = 1

#Strip values under 50 and divde by 50
strip_value = 50
frequency_dictionary_stripped = {k: v for k, v in frequency_dictionary.items() if v > strip_value}
frequency_dictionary_normalized = {k: int(round(v/strip_value)) for k, v in frequency_dictionary_stripped.items()}

#Sort and write new dictionary
sorted = sorted(frequency_dictionary_normalized.items(), key=operator.itemgetter(1), reverse=True)
with open(args.new_dictionary, 'w') as f:
    f.write('\n'.join('%s %s' % x for x in sorted))

print("Total words in dictionary: ", len(sorted))
print("Total occurences of words in dictionary: ", sum(frequency_dictionary_stripped.values()))
