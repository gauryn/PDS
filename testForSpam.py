#!/usr/bin/env python

# 1. Token words
# 2. Get Spam Probabilities for words
# 3. Find Interesting words
# 4. Add probability of interesting words
# 5. If total prob > 0.9 ==> Spam, else ham


from ExtractContent import ExtractSubPayload
from trainForWordSpamProb import getWordCountFromFile
import os 
import chardet
import nltk
import math

# extract test file
def extractTestFile(filename):
	# extract test file
	msg = ExtractSubPayload(filename)
	# write to txt file
	dstpath = filename.replace('.eml', '.txt')
	dstfile = open(dstpath, 'w')
	dstfile.write(msg)
	dstfile.close()
	return dstpath

# tokenize file
def getWords(filename):
	wordList = []
	fp = open(filename, 'r')
	# iterate over each line
	# charset = line 0
	charset = fp.readline().strip()
	for line in fp:
		# words = line.split()
		words = nltk.word_tokenize(line.decode(charset, errors='replace'))
		
		wordList += words
	return wordList

# get prob for each word
def pForWord(trainedWords, word ):
	# if test word in trained set
	if word in trainedWords.keys():
		print('Old word: ', word)
		return trainedWords[word]
	# for w in trainedWords.keys():
	# 	if word.encode('UTF-8', errors='replace').lower() == w.lower():
	# 		print('Reached old: ', w)
	# 		return trainedWords[w]
	# if word not in train set: prob = constant = 0.4
	print("reached new: ", word)
	return 0.4

def getProbForWords(filename):
	trainedWords = getWordCountFromFile('testWordCount.txt')
	probDict = {}
	testWordList = getWords(filename)
	for word in testWordList:
		p = pForWord(trainedWords, word)
		probDict[word] = p
	# interesting words: prob > 0.5
	# interestingWords = {k:v for k,v in probDict.iteritems() if v>0.5}
	# interesting words: top 15 words
	interestingWordsList = sorted(probDict, key=probDict.get, reverse=True)[:15]
	print('Iw: ',interestingWordsList)
	interestingWords = {}
	for iw in interestingWordsList:
		interestingWords[iw] = probDict[iw]
	print('Iwd: ', interestingWords)
	return interestingWords
	# return probDict

def getTotalProb(filename):
	interestingWords = getProbForWords(filename)
	# calc total prob
	valueList = interestingWords.values()
	# probDict = getProbForWords(filename)
	# valueList = probDict.values()

	# num = 1
	# inv = 1
	# for v in valueList:
	# 	num = num*v 
	# 	inv = inv*(1-v)
	# print('Inv: ', inv)
	# print('Prob: ', float(num)/(num+inv))
	# print('Num: ', num)
	# print('Den: ', num+inv)
	# return float(num)/(num+inv)

	# prob using ln 
	nu = 0
	for v in valueList:
		nu += (math.log(1-v) + math.log(v))
	print('Nu: ', nu)
	p = 1/ (1+math.exp(nu))
	print('P: ', p)
	return p 
	
def isSpam(filename):
	totalProb = getTotalProb(filename)
	if totalProb > 0.9:
		return True
	else:
		return False


dstFile = extractTestFile('/Users/gaurynagaraju/Documents/Spring 2016/Practical Data Science/Project 2/CSDMC2010_SPAM/CSDMC2010_SPAM/TRAINING/TRAIN_00000.eml')
sp = isSpam(dstFile)
print('IsSpam?: ', sp)





