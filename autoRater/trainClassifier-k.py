# -*- coding:utf8 -*- 
#!/usr/bin/python
# This script trains a classifier.

import csv
import sys
import re
import jieba
#import tfidf
import nltk
import pickle
import pandas as pd
# This function implements :
# clean the reply data, count line number and reply length, divide words
# And the store cleaned data into a text file.


# <codecell>
raw = pd.read_table('E:/my/Dropbox/BBS data analysis/classify-initiation/raw_replies-full.csv',sep=",")
  
dat = raw.ix[raw.authorid!=2]
#dat['word'] = raw.message.apply(lambda x: )    
  
# <codecell>
def clean(x):
    cleaned = re.sub('[\n|\r]', '@@@',x) # remove line end
            
    p=r'{:[0-9_]*:}' # smiley
    cleaned = re.sub(p, '', cleaned)

    # strip discuz code
    cleaned = re.sub(r'\[i=s\].*\[/i\]', '', cleaned)
    cleaned = re.sub(r'\[url=[^]]*]\d+#\[/url\]', '', cleaned)
    for t in ['quote','img','email']:
        tag = r'\[%s(=?)[^\]]*\].*\[/%s\]' % (t,t)
        cleaned = re.sub(tag, '', cleaned)    

    for t in ['u','i','b']:
        tag = r'\[%s\]' % t
        cleaned = re.sub(tag, '', cleaned)
        tag = r'\[/%s\]' % t
        cleaned = re.sub(tag, '', cleaned)    
        
    for t in ['color','url','size','align','font']:
        tag = r'\[%s=?[^\]]*\]' % t
        cleaned = re.sub(tag, '', cleaned)
        tag = r'\[/%s\]' % t
        cleaned = re.sub(tag, '', cleaned)    

    cleaned = re.sub(" ", '', cleaned) 

    cleaned = re.sub("  ", '', cleaned)
    cleaned = re.sub("  ", '', cleaned)
    cleaned = re.sub("  ", '', cleaned)
    cleaned = re.sub("  ", '', cleaned)
    for punc in [r',', r'，', r'\.', r'。', r'\)', r'\(', r'《', r'》',r'？', r':', r'：',r'…', r'-', r'~',r'！',r'）', r'（',r'、']:
        cleaned = re.sub(punc, '', cleaned)
    
    cleaned = cleaned.strip().lower()
    cleaned = re.sub(r'@@@', '\n', cleaned)
    cleaned = re.sub(r'\n\n', '\n', cleaned)
    cleaned = re.sub(r'\n\n', '\n', cleaned)
    cleaned = re.sub(r'\n\n', '\n', cleaned)
    cleaned = re.sub(r'\n\n', '\n', cleaned)
                    
    return cleaned
    #return ' '.join(jieba.cut(cleaned))

dat['clean_msg'] = dat.message.apply(clean)    
dat['words'] = dat.clean_msg.apply(jieba.cut) 
 
dat['line_cnt'] = dat.clean_msg.apply(lambda x: x.count('\n')+1)  
dat['msg_len'] = dat.clean_msg.apply(len)

#print words
# <codecell>
#dirty = dat.message.ix[ dat.message.map(lambda x: '[' in x)]
#for each in dirty.apply(clean):
#    print each
# <codecell>

dat['good'] = dat.rate > 0 
print dat.head()
dat.describe()

print dat.good.count()

print dat.line_cnt.groupby(dat.good).mean()
print dat.line_cnt.groupby(dat.good).std()

print dat.msg_len.groupby(dat.good).mean()
print dat.msg_len.groupby(dat.good).std()

# <codecell>

good_words=[]
for each in words.ix[good]:
    good_words+=each

spam_words=[]
for each in words.ix[~good]:
    spam_words+=each

# <codecell>
good_wordcount = nltk.FreqDist(good_words)
spam_wordcount = nltk.FreqDist(spam_words)

top_good_words = good_wordcount.keys()[:100]
top_spam_words = spam_wordcount.keys()[:100]

# <codecell>
for e in top_good_words:
    print e, good_wordcount[e]
    
print '---------------'
for e in top_spam_words:
    print e, spam_wordcount[e]
# <codecell>
len([e for e in top_good_words if e in top_spam_words])








# <codecell>

def cleanData():
  #reader = csv.reader(open('raw_replies2.csv'))
  #file = open('jieba_data2.txt','a')


  
  reader = csv.reader(open('E:/my/Dropbox/BBS data analysis/classify-initiation/raw_replies.csv'))
  file = open('jieba_data_full.txt','wb')  
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