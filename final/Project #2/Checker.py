from tkinter import Tk, scrolledtext, Menu, filedialog, END, messagebox
import os
import nltk

class Spell_Checker:

    def __init__(self, dictionary,bigrams):
        self.old_text_word_list = ([])

        self.dictionary = {}
        self.dictSum = 0
        self.bigrams = {}  
        #Fill dictionary from file 
        with open(dictionary, 'r', encoding='iso-8859-1') as f:
            for line in f:
                word = line.split()[0]
                self.dictionary[word] = int(line.split()[1])
        
        self.dictSum = sum(self.dictionary.values()) 

        #fill bigram for old dict 
        with open(bigrams, 'r', encoding='iso-8859-1') as f:
            for line in f: 
                word = line.split()[0]
                nextword = line.split()[1] 
                freq = int(line.split()[2]) 
                if word in bigram_frequency_dictionary: 
                    self.bigrams[word][nextword] = freq
                else:  
                    self.bigrams[word] = {nextword:freq}

    def new_words(self, current_text):
        current_text_word_list = ([])
        #creates lists of new words to spellcheck 
        for sentence in nltk.sent_tokenize(current_text):
            for word in nltk.word_tokenize(sentence):
                if word not in current_text_word_list:
                    current_text_word_list.append(word)

        new_words = [i for i in current_text_word_list if i not in self.old_text_word_list]
        self.old_text_word_list = current_text_word_list
        print(new_words)

        return new_words

    def spell_check(self, current_text):
        new_words = self.new_words(current_text) 
        misspelled=[] 
        for word in new_words:
            if word not in self.dictionary:
                misspelled.append(word) 
         
        #Corrections = 

        errors_and_suggestions = []

        return errors_and_suggestions 


    def known(self,words):
        return set(w for w in words if w in self.dictionary)


    def prob(self,word):
        return (self.dictionary(word))/(self.dictSum)

    def allCandidates(self,word):
        return (known([word]) or known(candidates1(word)) or known(candidates2(word)) or [word])
    def suggestCorrections(self, misspelled):
        return sorted(missspelled,reverse=True)[:3]
 

    def candidates1(self, word):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        
        #all possible splits
        split =  [(word[:i],word[i:]) for i in range(len(word+1))] 
        #all possible deletions  
        deletions = [] #its a set not a dict
        for l,r in split:
            if r:#if right exsists
                deletions.append(l+r[1:])#add right side to left but ignore the 0th letter
        #all possible insertions
        insertions = []
        for l,r in split:
            for sub in letters:#substitutions
                insertions.append(l+sub+r)
        #all possible letter replaces
        replace = []
        for l,r in split:
            if r:#dont overrun
                for sub in letters:#substitute letter
                    replace.append(l+sub+r[1:])#leave out a letter
          
        #all possible transpositions aka 2 adjacent letters swapped
        transpositions = []
        for l,r in split:
            if len(r)>1;
                transpositions.append(l+r[1]+r[0]+r[2:])
        return set(insertions+deletions+replace+transpositions)
        
    def candidates2(self, word):  
        return (c2 for c1 in self.candidates1(word) for c2 in self.candidates1(c1))

       



