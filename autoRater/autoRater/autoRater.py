# -*- coding:gbk -*- 
#!/usr/bin/python

import httplib
import urllib,urllib2
import BeautifulSoup
import re
import sys
import time
import MySQLdb
import random
import cookielib
import pickle
import jieba

# Log in.
def login(username, password):
  print 'Logging in ...'
  postURL = 'http://www.1point3acres.com/bbs/member.php' 
  cookieJar = cookielib.LWPCookieJar()  
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar), urllib2.HTTPHandler)      
  urllib2.install_opener(opener)
  postData = {'username' : username,
  'password' : password,
  'quickforward' : 'yes',
  'handlekey' : 'ls',
  'mod' : 'logging',
  'action' : 'login',
  'loginsubmit' : 'yes',
  'infloat' : 'yes',
  'lssubmit' : 'yes',
  'inajax' : '1'}
  postData = urllib.urlencode(postData)
  request = urllib2.Request(postURL, postData)
  response = urllib2.urlopen(request)
  #urllib2.urlopen(request)
  print response.read()
  print 'Log in successfully!'

def getLatestRepliesList(tid, page):
  ''' TEST CODE
  file = open('test.htm','r')
  doc = file.read()
  file.close()
  '''
  # Initialize replies list.
  repliesInfo_list = []
  
  # get raw html text.
  url = 'http://www.1point3acres.com/bbs/thread-%s-%s-1.html' % (tid, page)
  doc = urllib2.urlopen(url).read()
  
  # extract reply info from raw html file and then insert them into a list, repliesInfo_list
  soup = BeautifulSoup.BeautifulSoup(doc)
  postlist_obj = soup.html.body.find('div', {'id' : 'postlist'})
  repliesList_obj = postlist_obj.findAll('div', id = re.compile('post_\d+') )
  for reply_obj in repliesList_obj:
    reply_pid = reply_obj.attrs[0][1].split('_')[1]
    reply_text = reply_obj.find('td', id = re.compile('postmessage_\d+') ).text
    reply_authorid = reply_obj.find('dl', {'class' : 'pil cl'}).text.split('UID')[1]
    #print reply_pid,reply_authorid
    #print reply_text
    #print reply_authorid
    # Figure out no rated replies and tag them.
    rate_obj = reply_obj.find('p', {'class' : 'ratc'})
    rate_flag = False
    if rate_obj is not None:
      rate_flag = True
    # Insert information of replies into a list, repliesInfo_list.
    repliesInfo_list.append( [reply_authorid, reply_pid, reply_text, rate_flag] )

  return repliesInfo_list

def getReplyTimes(tid, authorid):
  print 'Counting reply times ...'
  
  # get raw html text.
  URL = 'http://www.1point3acres.com/bbs/forum.php'
  #http://www.1point3acres.com/bbs/forum.php?mod=viewthread&tid=84602&page=1&authorid=88416
  page = '1' # only scrap first page in this case.
  countData = {'mod' : 'viewthread',
  'tid' : tid,
  'page' : page,
  'authorid' : authorid}
  countData = urllib.urlencode(countData)
  request = urllib2.Request(URL, countData)
  response = urllib2.urlopen(request)
  doc = response.read()
  
  # count reply times
  soup = BeautifulSoup.BeautifulSoup(doc)
  postlist_obj = soup.html.body.find('div', {'id' : 'postlist'})
  repliesList_obj = postlist_obj.findAll('div', id = re.compile('post_\d+') )  
  replyTimes = len(repliesList_obj)
  
  print 'Get reply times!'
  print replyTimes
  return replyTimes
  
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
  
def classifier(myClassifier, feature_set, raw_text):
  # Chinese character encodings are really troublesome!!
  word_list = [iter.encode('gbk') for iter in list(jieba.cut(raw_text))]
  reply_length = len(raw_text)
  lines_num = raw_text.count('\n')
  text_features = getTextFeatures(word_list,reply_length,lines_num,feature_set)
  #print text_features
  #for iter in text_features:
  #  print iter, text_features[iter]
  result = myClassifier.classify(text_features)
  return result == '1'
  
# This function rate a reply with reason and score.
def rate(tid, page, pid, score, reason):
  print 'Reply Info:', tid, pid, score, reason
  print 'Rating ......' 
  rateURL = 'http://www.1point3acres.com/bbs/forum.php'
  referer = 'http%3A%2F%2Fwww.1point3acres.com%2Fbbs%2Fforum.php%3Fmod%3Dviewthread%26tid%3D' + tid + '%26page%3D' + page + '%23pid' + pid
  rateData = {'mod' : 'misc',
  'action' : 'rate',
  'ratesubmit' : 'yes',
  'infloat' : 'yes',
  'inajax' : '1',
  'formhash' : '782ed14a', # I don't know what the use of 'formhash' is.
  'tid' : tid,
  'pid' : pid,
  'referer' : referer,
  'handlekey' : 'rate',
  'score1' : score,
  'reason' : reason}
  rateData = urllib.urlencode(rateData)
  request = urllib2.Request(rateURL, rateData)
  urllib2.urlopen(request)  
  print 'Rate successfully!' 
 
# This function doesn't work  
def post(fid, tid, message):
  postURL = 'http://www.1point3acres.com/bbs/forum.php'
  postData = {'mod' : 'post',
  'action' : 'reply',
  'fid' : fid,
  'tid' : tid,
  'extra' : 'page=1',
  'replysubmit' : 'yes',
  'infloat' : 'yes',
  'handlekey' : 'fastpost',
  'inajax' : '1',
  'message' : message,
  'posttime' : '1393293780',
  'formhash' : 'e987babc', #'782ed14a',# 
  'subject' : ''
  }
  postData = urllib.urlencode(postData)
  print 'Post Info:', fid, tid, message
  print postData
  print 'Posting ......'   
  request = urllib2.Request(postURL, postData)
  urllib2.urlopen(request)  
  print 'Post successfully!' 
 
def main():
  # Step 1 : enter username and password to log in.
  username = raw_input('username:')
  password = raw_input('password:')
  login(username, password)
  #sys.exit()
  
  # Step 2 : initialize topic id and page number.
  tid = '84602' # 这个是版主区测试帖的编号
  page = '2'
  fid = '97' # 这个是版主区的编号，这些编号怎么来的请看 url 和 Discuz!的data schema 
  
  # TEST CODE FOR POST FUNCTION
  #message = 'AUTOPOSTTEST'
  #post(fid, tid, message)
  #sys.exit()
  
  # Step 3 : initialize decision tree classifier and feature set.
  file = open('myNaiveBayesClassifier.pickle')
  #file = open('myDecisionTreeClassifier.pickle')
  myClassifier = pickle.load(file)
  file.close()
  file2 = open('feature_set.txt','r')
  feature_set = file2.read().split('\n')
  file2.close()
  
  # TEST CODE!
  #file = open('test_reply.txt','r')
  #raw_text = file.read()
  #file.close()
  #print classifier(myClassifier, feature_set, raw_text)
  #sys.exit()
  
  # Step 4 : get latest replies list.
  # each element of the list orderly contains: reply_authorid, reply_pid, reply_text, rate_flag
  repliesInfo_list = getLatestRepliesList(tid, page)
  
  # Step 5 : traverse replies list and rate suitable replies.
  for reply_info in repliesInfo_list:
    reply_authorid = reply_info[0]
    reply_pid = reply_info[1]
    raw_text = reply_info[2]
    rate_flag = reply_info[3]
    classification_result = classifier(myClassifier, feature_set, raw_text)
    
    if not rate_flag:
      # You can raise the threshold as 50 for tests.
      if getReplyTimes(tid, reply_authorid) > 1:
        score = '1'
        reason = '重复报道扣分！'
        rate(tid, page, reply_pid, score, reason)
      elif not classification_result:
        score = '1'
        reason = '报道不合格！'
        rate(tid, page, reply_pid, score, reason)      
      elif classification_result:
        score = '1'
        reason = '欢迎来到一亩三分地论坛！'
        rate(tid, page, reply_pid, score, reason) 
    
    
if __name__ == '__main__':
  main()