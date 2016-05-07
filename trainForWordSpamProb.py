#!/usr/bin/env python
# Double all non-spam words
# Consider words that occur > 5
# Find prob that email is span if email has word 

import os, sys

MIN_WORD_COUNT = 5
RARE_WORD_PROB = 0.5
EXCLUSIVE_WORD_PROB = 0.9

def createWordDict(fp):
	wordDict = {}
	for line in fp:
		words = line.split()

		word = words[0]

		spamCount = int(words[1][1:-1])
		hamCount = int(words[2][:-1])
		wordDict[word] = [spamCount, hamCount]

	return wordDict

def probForWord(wordDict, word, tSpam, tHam):
	# print('WordDict: ', wordDict[word])
	total_word_count = wordDict[word][0] + wordDict[word][1]

	if total_word_count < MIN_WORD_COUNT:
		return RARE_WORD_PROB
	# spam count of word = 0
	elif wordDict[word][0] == 0:
		return 1-EXCLUSIVE_WORD_PROB
	# ham count = 0
	elif wordDict[word][1] == 0:
		return EXCLUSIVE_WORD_PROB

	else:
		# P(W n S) = P(S)*P(W|S)
		# P(S) = constant
		probS = 0.5
		# P(W|S) = num of spam occ / total num of occ for that word
		probWgnS = float(wordDict[word][0]) / tSpam
		# P(H)
		probH = 1 - probS
		# P(W|H)
		probWgnH = float(wordDict[word][1]) / tHam

		# P(S | W) = P(S)*P(W|S) / P(S)*(PW|S) + P(H)*P(W|H)
		num = probS * probWgnS
		den = num + (probH * probWgnH)
		return float(num)/den

		# P(H | W) = P(H)*P(W|H) / P(H)*P(W|H) + P(S)*P(W|S)


def totalSpamAndHamEmails(filename = 'total.txt'):
	total = [0, 0] # 0: spam, 1: ham
	fp = open(filename)
	for line in fp:
		words = line.split()
		if words[0]=='ham':
			total[1] = int(words[1])
		else:
			total[0] = int(words[1])
	return total

def getWordCountFromFile(filename):
	fp = open(filename, 'r')
	# create wordDict 
	wordDict = createWordDict(fp)

	# totals for spam and ham
	total = totalSpamAndHamEmails()
	tSpam = total[0]
	tHam = total[1]
	# probs for every word
	probDict = {}
	for word in wordDict.keys():
		p = probForWord(wordDict, word, tSpam, tHam)
		probDict[word] = p
	return probDict 

def getInterestingWords(filename):
	probDict = getWordCountFromFile(filename)
	interestingWords = {k:v for k,v in probDict.iteritems() if v>0.5}
	# interestingWords = sorted(probDict, key=probDict.get, reverse=True)
	return interestingWords


# getWordCountFromFile('testWordCount.txt')
# print getInterestingWords('testWordCount.txt')
