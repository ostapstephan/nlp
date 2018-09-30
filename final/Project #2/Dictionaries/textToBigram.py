#Ostap Voynarovskiy and Luka Lipovac
#Natural Langage Processing - Project #2: Auto Correct
#April 9th, 2018

#Run with: python textToBigram.py path_to_texts_folder dictionary.txt oldBigrams.txt newBigrams.txt

import nltk
import os 
import argparse
import operator

#Parse input
parser = argparse.ArgumentParser()
parser.add_argument("texts_path")
parser.add_argument("dictionary")
parser.add_argument("old_Bigram")
parser.add_argument("new_Bigram")
args = parser.parse_args()

bigram_frequency_dictionary = {} #key is word, value is {next_word:freq}
frequency_dictionary = {}

#load valid words dictionary

with open(args.dictionary, 'r', encoding='iso-8859-1') as fd:
    for line in fd:
        word = line.split()[0]
        frequency_dictionary[word] = int(line.split()[1])


#Fill bigram dictionary with old dictionary
with open(args.old_Bigram, 'r', encoding='iso-8859-1') as fd:
    for line in fd: 
        word = line.split()[0]
        nextword = line.split()[1] 
        freq = int(line.split()[2]) 
        if word in bigram_frequency_dictionary: 
            bigram_frequency_dictionary[word][nextword] = freq
        else:  
            bigram_frequency_dictionary[word] = {nextword:freq}


#Read all files in folder
i =0;
for file in os.listdir(args.texts_path):#reads all file names in directory
    print(i)
    i+=1
    path = os.path.abspath(args.texts_path) #generates path so you can easliy append file nams

    with open(os.path.join(path, file ), 'r', encoding='iso-8859-1') as f:
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





#Strip values under 50 and divde by 50
# strip_value = 50 
# frequency_dictionary_stripped = {k: v for k, v in frequency_dictionary.items() if v > strip_value}
# frequency_dictionary_normalized = {k: int(round(v/strip_value)) for k, v in frequency_dictionary_stripped.items()}

#Sort and write new dictionary
for key in bigram_frequency_dictionary.keys():
    bigram_frequency_dictionary[key] = sorted(bigram_frequency_dictionary[key].items(), key=operator.itemgetter(1), reverse=True)

totalBigrams= 0
with open(args.new_Bigram, 'w') as f: 
    for w1 in bigram_frequency_dictionary.keys():  
        for i in range(0, len(bigram_frequency_dictionary[w1])):
            f.write('\n'+str(w1)+' '+
                    str(bigram_frequency_dictionary[w1][i][0])+' '+str(bigram_frequency_dictionary[w1][i][1]))
        totalBigrams += len(bigram_frequency_dictionary[w1])

print("Total bigrams in corpora: ", totalBigrams)
# print("Total occurences of words in dictionary: ", sum(frequency_dictionary_stripped.values()))
