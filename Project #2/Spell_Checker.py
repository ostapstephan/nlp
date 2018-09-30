from tkinter import Tk, scrolledtext, Menu, filedialog, END, messagebox
import os
import nltk
import heapq
import math

class Spell_Checker:

    def __init__(self, dictionary, bigrams):#added third arg 
        self.old_text_word_list = ([])
        self.old_bi_word_list = ([])
        self.returnedSuggestions = 3

        self.dictionary = {}
        self.bigrams = {}
        self.revBigrams= {}
        with open(bigrams, 'r', encoding='UTF-8') as fd:
            for line in fd: 
                word = line.split()[0]
                nextword = line.split()[1] 
                freq = int(line.split()[2]) 
                if word in bigrams: 
                    bigrams[word][nextword] = freq
                else:  
                    bigrams[word] = {nextword:freq}

                if word in revBigrams: #may be unnessesary 
                    revBigrams[nextword][word] = freq
                else:
                    revBigrams[nextword] = {word:freq}

        #Fill dictionary from file
        with open(dictionary, 'r', encoding='UTF-8') as f:
            for line in f:
                word = line.split()[0]
                self.dictionary[word] = int(line.split()[1])

        
        self.dictSum = sum(self.dictionary.values()) #to calc probabilities
        self.misspelled = {}
        self.misspelledbg = {}



    def new_words(self, current_text):
        current_text_word_list = ([])
        #creates lists of new words to spellcheck
        for sentence in nltk.sent_tokenize(current_text):
            for word in nltk.word_tokenize(sentence):
                if word not in current_text_word_list:
                    if word.isalpha():
                        current_text_word_list.append(word)
         
        new_words = [i for i in current_text_word_list if i not in self.old_text_word_list]
        self.old_text_word_list = current_text_word_list

        return new_words

    def spell_check(self, current_text):
        new_words = self.new_words(current_text)

        for word in new_words:
            if word not in self.dictionary:
                if word.capitalize() in self.dictionary:
                    self.misspelled[word] = [word.capitalize()]  
                elif word.lower() in self.dictionary:
                    continue
                else:
                    self.misspelled[word] = []

                self.misspelled[word] = self.misspelled[word] + self.suggestCorrections(word)
                #gives it one word
        
        return self.misspelled

    def known(self,words):
        return set(w for w in words if w in self.dictionary)

    def prob(self,word):
        return math.log((self.dictionary[word]))-math.log((self.dictSum))

    def allCandidates(self,word):
        return (self.known([word]) + self.known(self.candidates1(word)) + self.known(self.candidates2(word)))

    def suggestCorrections(self, misspelled):
        suggestions = self.allCandidates(misspelled)

        probabilitySuggestions = {}

        for word in suggestions:
            probabilitySuggestions[word] = self.prob(word);

        return heapq.nlargest(self.returnedSuggestions, (key for key, value in probabilitySuggestions.items()))

    def candidates1(self, word):
        letters = 'abcdefghijklmnopqrstuvwxyz'

        #all possible splits
        split =  [(word[:i],word[i:]) for i in range(len(word)+1)]
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
            if len(r)>1:
                transpositions.append(l+r[1]+r[0]+r[2:])
        return set(insertions+deletions+replace+transpositions)

    def candidates2(self, word):
        return (c2 for c1 in self.candidates1(word) for c2 in self.candidates1(c1))
    
    
    ######################BIGRAMS############################

    def bWords(self, current_text):
        cont_text = ([]) 
        #creates lists of new words to spellcheck
        for sentence in nltk.sent_tokenize(current_text):
            for word in nltk.word_tokenize(sentence):
                cont_text.append(word) 
        new_words = [] 
        if len(self.old_bi_word_list)>1:
            new_words += self.old_bi_word_list[-1]
            #add last word
        new_words += [i for i in cont_text if i not in self.old_bi_word_list]
        #add most recent words
        self.old_bi_word_list = cont_text
        return new_words #gives me a list of the most recently added words 

    def probBigram(self,prev,word,nxt):
        return ((self.bigrams[prev][word])/(self.dictionary[prev])+(self.revBigrams[nxt][word])/(self.dictionary[nxt]))
        
    def suggestCorrectionsbg(self,prev,mis,nxt):
        suggestions = self.known(self.candidates1(mis))
        #generated a bunch of 1 edit distance words
        probabilitySuggestions = {}  

        for word in suggestions:
            probabilitySuggestions[word] = self.probBigram(prev,word,nxt);
         
        return heapq.nlargest(self.returnedSuggestions, (key for key, value in probabilitySuggestions.items()))


    def suggestRealWorld(self,prev,word,nxt):
         
        suggestions = [w for w in bigrams[prev].keys() if w in revBigrams[nxt].keys()]
 
        pthreshold = 5*(probBigram(prev,word,nxt) )


        realsuggestions=[]
        for wd in suggestions:
            if probBigram(prev,wd,nxt)>pthreshold:
                realsuggestions += wd;
        
        return realsuggestions

    def bigramCheck(self,current_text):
        new_words = self.bWords(current_text)  
        if len(new_words)>1:
            for i in range(len(new_words)):
                if new_words[i] not in self.dictionary:
                    if new_words[i].capitalize() in self.dictionary:
                        self.misspelledbg[new_words[i]] = [new_words[i].capitalize()] 
                        #the capital lettered word will be suggested
                    elif new_words[i].lower() in self.dictionary:
                        continue     
                    else:
                        self.misspelledbg[new_words[i]] = []
                    
                    if (i+1<len(new_words)) and (i-1>0):
                        self.misspelledbg[new_words[i]] = self.misspelledbg[new_words[i]]+self.suggestCorrectionsbg(new_words[i-1],new_words[i],new_words[i+1])
                else:
                    if (i+1<len(new_words)) and (i-1>0):
                        self.realWorld[new_words[i]] = self.suggestRealWorld(new_words[i-1],new_words[i],new_words[i+1])

        return self.misspelledbg, self.realWorld
