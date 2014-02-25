# -*- coding:utf8 -*- 
#!/usr/bin/python
# This script trains a classifier.

import csv
import sys
import re
import jieba
import tfidf
import nltk
import pickle

# This function implements :
# clean the reply data, count line number and reply length, divide words
# And the store cleaned data into a text file.
def cleanData():
  #reader = csv.reader(open('raw_replies2.csv'))
  #file = open('jieba_data2.txt','a')
  reader = csv.reader(open('raw_replies_full2.csv'))
  file = open('jieba_data_full.txt','a')  
  counter = 0
  for iter in reader:
    reply_rate = iter[4]
    reply_length = len(iter[3])
    #reply_lineNum = iter[3].count('\r\n')
    reply_lineNum = len( re.compile('\r\n|\n').findall(iter[3]) ) + 1
    reply_text = re.sub(u'\r\n|\n', ' ', iter[3])
    #reply_text = reply_text.replace('\r',' ')
    jieba_str = ' '.join(jieba.cut(reply_text))
    rate_flag = '0'
    #if int(reply_rate) > 0:
    if reply_rate > '0':
      rate_flag = '1'
    line = '(#SEP#)'.join( [rate_flag,str(reply_length),str(reply_lineNum),jieba_str,'\n'] )
    # This step is quite important. Python interpretor change the string from ASCII to utf-8 and then finally to unicode. Method file.write() may encounter decoding problems without this step.
    file.write(line.encode('utf-8'))
    #print line
    counter += 1
    print counter
  file.close()

# This function initialize feature set.
def getFeatureSet(table):
  # Initialize word list of real reply and spam respectively.
  wordList_0 = []
  wordList_1 = []
  for iter in table.documents:
    if iter[1] <= '0' and 'quote' not in iter[-1].keys():
      wordList_0 += iter[-1].keys()
    if iter[1] > '0' and 'quote' not in iter[-1].keys():
      wordList_1 += iter[-1].keys()
  
  freqWordList_0 = list(nltk.FreqDist(wordList_0).iterkeys())
  freqWordList_1 = list(nltk.FreqDist(wordList_1).iterkeys())
  feature_0 = set(freqWordList_0[:100]) - set(freqWordList_1[:100])
  feature_1 = set(freqWordList_1[:100]) - set(freqWordList_0[:100])
  

  counter = 0
  file = open('feature_set_2000.txt','a')
  for iter in freqWordList_0[:2000]:
    file.write( iter + '\n' )
    counter += 1
  file.close()
  print counter 
  
# This function describe features of a text.
# In this case, features are whether the word in feature set.
def getTextFeatures(word_list,reply_length,lines_num,feature_set):
  text_features = {}
  text_features['reply_length'] = reply_length
  text_features['lines_num'] = lines_num
  for feature in feature_set:
    if feature in word_list:
      text_features[feature.lower()] = 1
    else:
      text_features[feature.lower()] = 0
  return text_features
  
def main():
  #cleanData()
  #sys.exit()
  
  # Initialize feature set.
  file = open('feature_set.txt','r')
  #file = open('feature_set_2000.txt','r')
  feature_set = file.read().split('\n')
  file.close()
  
  # Initialize the table that contains all information of replies.
  #file = open('jieba_data2.txt','r')
  file = open('jieba_data_full.txt','r')
  lines = file.readlines()
  file.close()
  table = tfidf.tfidf()
  for iter in range(len(lines)):
    reply_info = lines[iter].split('(#SEP#)')
    rate_flag = reply_info[0]
    reply_length = reply_info[1]
    lines_num = reply_info[2]
    dividedWords_list = reply_info[-2].lower().split()
    # eliminate replies of replies.
    if 'quote' not in dividedWords_list:
      table.addDocument(str(iter), rate_flag, reply_length, lines_num, dividedWords_list)
      # print 'lines_num:',lines_num,'reply_length:',reply_length

  #getFeatureSet(table)
  #sys.exit()
      
  # Get feature set of every sample.
  sample_list = table.documents
  infoPairs_list = []
  for sample_info in sample_list:
    rate_flag = sample_info[1]
    word_list = sample_info[-1].keys()
    reply_length = sample_info[2]
    lines_num = sample_info[3]
    text_features = getTextFeatures(word_list,reply_length,lines_num,feature_set)
    infoPairs_list.append( (text_features, rate_flag) )
  
  # Train a decision tree (or naive bayes) classifier and test it.
  size = int(len(infoPairs_list) * 0.1)
  train_set, test_set = infoPairs_list[size:], infoPairs_list[:size]
  print 'Training classifier ...'
  classifier = nltk.NaiveBayesClassifier.train(train_set)
  #classifier = nltk.DecisionTreeClassifier.train(train_set)
  print 'Classfier has been trained!'
  
  #print classifier.pseudocode(depth=3)
  print nltk.classify.accuracy(classifier, test_set)
  
  # Save the classifier above.
  file = open('myNaiveBayesClassifier.pickle', 'wb')
  #file = open('myDecisionTreeClassifier.pickle', 'wb')
  pickle.dump(classifier, file)
  file.close()
  print 'my classifier has been saved.'
  
if __name__ == '__main__':
  main()