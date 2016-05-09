#!/usr/bin/env python

import os, sys
import shutil
import spacy

en_nlp = spacy.load('en')

exclusive_words = ['content-type', 'tontent-transfer-tncoding', '<', '>', 'mon', 'tues', 'wed', 'thurs', 'fri', 'sat', 'sun', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'jan', 'feb', 'mar', 'apr', 'nay', 'june', 'july', 'aug', 'sept', 'oct', 'nov', 'dec', 're', 'ascii', '7bit', 'content', 'text/html', 'plain', 'ascii', 'body', 'head', 'u', 'div', '/p', 'p', '8bit', '5C4033']

def getLabel(filename = 'SPAMTrain.label'):
	labelDict={}
	fp = open(filename, 'r')
	for line in fp:
		words = line.split()
		f = words[1][:-4] # get filename without extension
		labelDict[f] = words[0] # words[1] = 0/ 1 based on spam/ ham
	return labelDict

def createWordDict():
	d = {}
	return d

def addToDict(wordDict, word, fname, labelDict):
	print('Word: ', word)
	# ignore some words
	if word.is_digit or word.is_punct or word.is_space or word.is_oov or word.is_stop:
		return
	# check if in blacklisted words
	elif word.is_alpha :
		word = word.orth_[:].encode('ascii')
		for ew in exclusive_words:
			if (word.lower() in ew.lower()) or (ew.lower() in word.lower()):
				return 
		# else add to dict
		if word.lower() in wordDict:
			# index 0: spam
			if labelDict[fname] == '0':
				wordDict[word.lower()][0] += 1
			# index 1: ham
			else:
				wordDict[word.lower()][1] += 1
		else:
			# index 0: spam
			if labelDict[fname] == '0':
				wordDict[word.lower()] = [1,0]
			# index 1: ham
			else:
				wordDict[word.lower()] = [0,1]



def getWordCount (wordDict, filename, labelDict):
	if not os.path.exists(filename): # dest path doesnot exist
		print("ERROR: input file does not exist:", filename)
		os.exit(1)

	# get filename from file path
	head, tail = os.path.split(filename)
	fname = tail[:-4]

	fp = open(filename, 'r')
	# iterate over each line
	# charset = line 0
	charset = fp.readline().strip()
	for line in fp:
		# words = line.split()
		# words = nltk.word_tokenize(line.decode(charset, errors='replace'))
		u = unicode(line, "utf-8")
		words = en_nlp(u)
		for word in words:
			addToDict(wordDict, word, fname, labelDict)


def getWordCountForDir ( srcdir, dstFile ):
	'''Get count for each token in all extracted email data'''
	if not os.path.exists(dstFile): # dest path doesnot exist
		os.mknod(dstFile)  
	files = os.listdir(srcdir)
	# create word dictionary
	wordDict = createWordDict()
	# get labelDict
	labelDict = getLabel()
	for file in files:
		if not file.startswith('.'):		
			srcpath = os.path.join(srcdir, file)
			getWordCount(wordDict, srcpath, labelDict)
	df = open(dstFile, 'w')
	for key in wordDict.keys():
		msg = key.encode('UTF-8', errors='replace') + ' ' + str(wordDict[key]) + '\n'
		df.write(msg)
	df.close()

def getTotalSpamAndNonSpamEmails(srcFile, dstFile):
	'''Get total number of spam and non-spam email'''
	# create count dictionary
	countDict = {'spam': 0, 'ham': 0}
	fp = open(srcFile, 'r')
	for line in fp:
		words = line.split()
		if words[0]== '1':
			countDict['ham'] += 1
		else:
			countDict['spam'] += 1
	# write to File
	df = open(dstFile, 'w')
	for key in countDict.keys():
		msg = str(key) + ' ' + str(countDict[key]) + '\n'
		df.write(msg)
	df.close()


###################################################################
# main function start here
# srcdir is the directory where the .eml are stored
print('Input source directory: ') #ask for source and dest dirs
srcdir = raw_input()
if not os.path.exists(srcdir):
	print('The source directory %s does not exist, exit...' % (srcdir))
	sys.exit()
# dstdir is the directory where the content .eml are stored
print('Input destination File: ') #ask for source and dest dirs
dstFile = raw_input()
if not os.path.exists(dstFile):
	print('The destination directory is newly created.')
	os.mknod(dstFile)

# ###################################################################
getWordCountForDir(srcdir, dstFile ) 
# getTotalSpamAndNonSpamEmails ('SPAMTrain.label', 'total.txt')

