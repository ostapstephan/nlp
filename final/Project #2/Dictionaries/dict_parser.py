#Luka Lipovac and Ostap Voynarovskiy
#Natural Language Processing - Project #2: Auto-Correct
#April 9th, 2018

#Run with: python dict_parser.py path_to_dict_folder old_dictionary.txt new_dictionary.txt

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
for file in os.listdir(args.texts_path):
    path = os.path.abspath(args.texts_path)
    with open(os.path.join(path, file), 'r', encoding='iso-8859-1') as f:
        for line in f:
            word = line.split()[0]
            if word not in frequency_dictionary:
                frequency_dictionary[word] = 1


#Sort and write new dictionary
sorted = sorted(frequency_dictionary.items(), key=operator.itemgetter(1), reverse=True)
with open(args.new_dictionary, 'w') as f:
    f.write('\n'.join('%s %s' % x for x in sorted))

print("Total words in dictionary: ", len(frequency_dictionary))
print("Total occurences of words in dictionary: ", sum(frequency_dictionary.values()))
