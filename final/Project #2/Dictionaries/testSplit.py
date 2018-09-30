import nltk 
import os
import argparse 
import operator


frequency_dictionary = {}
bigram_frequency_dictionary = {}

path = os.path.abspath('./Texts/')
print(path)



i=0
with open('./Frequency_Dictionary.txt', 'r', encoding='iso-8859-1') as fd:
    for line in fd:
        word = line.split()[0]
        frequency_dictionary[word] = int(line.split()[1])


with open(os.path.join(path, "Pride and Prejudice.txt" ), 'r', encoding='iso-8859-1') as f:
    for line in f: 
        i += 1 
        print(i)
        prevWord = ""
        for sentence in nltk.sent_tokenize(f.read().lower()): 
            for word in nltk.word_tokenize(sentence):
                if word.isalpha():
                    if word in frequency_dictionary:  
                        if prevWord != "": 
                            if prevWord in bigram_frequency_dictionary:
                                if word in bigram_frequency_dictionary[prevWord]:
                                    bigram_frequency_dictionary[prevWord][word]+= 1
                                    prevWord = word
                                else:
                                    bigram_frequency_dictionary[prevWord][word] = 1
                                    prevWord = word
                            else:  
                                bigram_frequency_dictionary[prevWord] = {word:1}
                                prevWord = word
                        else:
                            prevWord = word
                    else:
                        prevWord = ""
                else:
                    prevWord = ""

print(bigram_frequency_dictionary['then'])
