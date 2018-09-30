#python 3.5
import nltk
from nltk.stem import *
import numpy 
from nltk.tokenize import word_tokenize
import operator
import math
import string
import pprint
from collections import Counter

def TrainandTest(trainingData,testData,outFile):
    filetag = []
    i=0
    pp = pprint.PrettyPrinter(indent = 4) #setup pprint

    with open(trainingData) as fp:
        line = fp.readline()#open training Data File
        filetag.append(line.split(" ")) 
        while line:
            line =fp.readline()
            filetag.append(line.split(" ")) #create list with data file and tags
            i+=1
    fp.close()
   
    numFiles = i  #for use in calculating prior 
    vocab,cl,text,catVoc = extractvocab(filetag)  
    prior = calcPrior(cl, numFiles)
    cond =  condProb(catVoc,vocab)
    
    testList = []
    with open(testData) as tf:
        for line in tf:
            testList.append(line.strip()) #create list with data file and tags
    tf.close()
    
    score =  Test( prior, cond, testList,vocab)
    o = open(outFile,'w')
    i=0 

    for i in range( 0,len(testList)-1):
        o.write(testList[i]+ ' '+ str(max(score[i], key=score[i].get)))#str(score[i])  
    o.close()
      
    final = []
    for i in range( 0,len(testList)-1):
        t=[]
        t=[testList[i], str(max(score[i], key=score[i].get))]
        final.append(t)
          
    return final, testList, score, filetag


def calcPrior(prior, numFiles):
    for key in prior: #calc prior 
        prior[key] /= numFiles
    return prior 

def extractvocab(filetag):
    vocab={}#create vocab dict
    cl = {}# create class dict for #files in class   
    text = {}
    catVoc= {} 
    i=0
    
    for f in filetag: #loop all docs
        if (f[0] != ''):#create categorized text repo
            with open(f[0]) as fp:
                t = fp.read()
                text = sortText(text, t, f[1],cl) 
        i+=1
        fp.close() 

    for cat in text:
        tokens = ToK(text[cat])#split up all docs in category 
        vocTemp=Counter()
        for token in tokens: #create vocab by checking if it's there
            vocTemp[token]+=1

        catVoc[cat] = vocTemp  
        for w in vocTemp:#generate complete vocab 
            if w in vocab:
                vocab[w]+=vocTemp[w] 
            else:
                vocab[w]=vocTemp[w]
      
    return vocab, cl, text, catVoc

def sortText(textCat, s, cat, cl):
    if cat in textCat:
        textCat[cat] += ' '+s
    else:
        textCat[cat] =s 

    if cat in cl: 
        cl[cat] +=1
    else: 
        cl[cat] =1 
    return textCat


def condProb(voc,vt):
    cond = {}
    laplace =.1
    
    for cat in voc:  
        cond[cat] = {}

    for cat in cond: #calculate individual Conditional probabilities
        for t in vt:  
            cond[cat][t] = (voc[cat][t]+laplace)/((sum(voc[cat].values()))+laplace*len(vt))
     
    return cond 


def Test(prior, cond, fl,vt):
    score = {}
    scoreFinal= []
    
    for doc in fl: 
        if (doc != ''):
            with open(doc) as fp:
                wd = ToK(fp.read())
                words = [] 
                score = {} 
                for w in wd:
                    if w in vt:
                        words.append(w)
                 
                for c in prior:
                    score[c]=math.log(prior[c])
                    for t in words:
                        if t in cond[c]:
                            score[c] +=math.log(cond[c][t])

            scoreFinal.append(score) 
            fp.close() 
    return scoreFinal

def ToK(s):
    w = nltk.word_tokenize(s) 
    w = [tok.lower() for tok in w]    
    w = [tok.strip() for tok in w]      
    # wo=[]
    # stemmer = PorterStemmer() 
    
    # inv = set(string.punctuation)
    # for t in w:
        # if any(c in inv for c in t):   
            # pass
        # else:
            # wo.append(t) 
    # wo = [stemmer.stem(al) for al in w] 
    return w

if __name__ == '__main__':
    print('''Please print training Data list File''')
    trainingData = input()
    print('''Please print test Data list File''')
    testData = input()
    print( '''Please print output File''')
    outFile = input()
    TrainandTest(trainingData,testData,outFile)
