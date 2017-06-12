# $Id: Hansen2010Diffusion.py,v 1.4 2011/05/05 09:43:06 fn Exp $
#
# export LD_LIBRARY_PATH=/usr/lib/xulrunner-`xulrunner --gre-version`


from __future__ import division
import getpass, numpy, pymongo, re, simplejson, sys, urllib


reload(sys)
sys.setdefaultencoding('utf-8')

connection = pymongo.Connection()
db = connection.twitter
tweets = db.tweets

pattern_split = re.compile(r"\W")

def download_tweets():
    password = getpass.getpass()       # get password for "fnielsen2" user
    url = "http://fnielsen2:" + password + \
        "@stream.twitter.com/1/statuses/sample.json"
    for tweet in urllib.urlopen(url):
        oid = tweets.insert(simplejson.loads(tweet))   # !!!
        print(tweets.count())

def set_englishness():
    filename = '/home/fnielsen/fnielsen/data/Nielsen2010Responsible_english.csv'
    englishwords = dict(map(lambda (k,v): (k,int(v)), 
                            [ line.split() for line in open(filename) ]))

    for tweet in tweets.find({"delete": {"$exists": False}}):
        englishness = sum(map(lambda word: englishwords.get(word.lower(),0), 
                              tweet['text'].split()))
        tweet['englishness'] = englishness         # Add a new field
        oid = tweets.save(tweet)                   # Overwrite the element 


def set_sentiments():
    filename = '/home/fnielsen/fnielsen/data/Nielsen2009Responsible_emotion.csv'
    try: 
        swords = dict(map(lambda (k,v): (k,int(v)), 
                          [ line.split('\t') for line in open(filename) ]))
    except: 
        for line in open(filename):
            if len(line.split('\t')) != 2:
                print(line)
    # Label with sentiment
    for tweet in tweets.find({"englishness": {"$gt": 0}}):
        sentiments = map(lambda word: swords.get(word.lower(),0), pattern_split.split(tweet['text']))
        tweet['sentiment'] = sum(sentiments)
        tweet['arousal'] = sum(map(abs, sentiments))
        tweet['ambivalence'] = tweet['arousal'] - abs(tweet['sentiment'])
        oid = tweets.save(tweet)  


# Matching expression for Retweeting
prog = re.compile(r"\bRT\b", re.UNICODE)


total = 0
retweet = 0
nonretweet = 0 
retweet_aroused = 0
retweet_negative = 0
retweet_positive = 0
retweet_neutral = 0
nonretweet_aroused = 0
nonretweet_negative = 0
nonretweet_positive = 0
nonretweet_neutral = 0
aroused = 0
negative = 0
positive = 0
neutral = 0
for tweet in tweets.find({"englishness": {"$gt": 0}}):
  total += 1
  if re.search(prog, tweet['text']):
    retweet += 1 
    if abs(tweet.get('sentiment', 0)) > 2:
      retweet_aroused += 1
      if tweet.get('sentiment', 0) > 2:
        retweet_positive += 1
      elif tweet.get('sentiment', 0) < 2:
        retweet_negative += 1
    elif tweet.get('sentiment', 0) == 0:
      retweet_neutral += 1
  else:
    nonretweet += 1
    if abs(tweet.get('sentiment', 0)) > 2:
      nonretweet_aroused += 1
      if tweet.get('sentiment', 0) > 2:
        nonretweet_positive += 1
      elif tweet.get('sentiment', 0) < 2:
        nonretweet_negative += 1
    elif tweet.get('sentiment', 0) == 0:
      nonretweet_neutral += 1
  if abs(tweet.get('sentiment', 0)) > 2:
    aroused += 1
    if tweet.get('sentiment', 0) > 2:
      positive += 1
    elif tweet.get('sentiment', 0) < 2:
      negative += 1
  elif tweet.get('sentiment', 0) == 0:
    neutral += 1


tweets.count()
tweets.find({"englishness": {"$gt": 0}}).count()

retweet_aroused/aroused
retweet_neutral/neutral
retweet_positive/positive
retweet_negative/negative






for tweet in tweets.find({"englishness": {"$gt": 0}}):
  total += 1
  if len(tweet['text']) > 100:
      if re.search(prog, tweet['text']):
        retweet += 1 
        if abs(tweet.get('sentiment', 0)) > 2:
          retweet_aroused += 1
          if tweet.get('sentiment', 0) > 2:
            retweet_positive += 1
          elif tweet.get('sentiment', 0) < 2:
            retweet_negative += 1
        elif tweet.get('sentiment', 0) == 0:
          retweet_neutral += 1
      else:
        nonretweet += 1
        if abs(tweet.get('sentiment', 0)) > 2:
          nonretweet_aroused += 1
          if tweet.get('sentiment', 0) > 2:
            nonretweet_positive += 1
          elif tweet.get('sentiment', 0) < 2:
            nonretweet_negative += 1
        elif tweet.get('sentiment', 0) == 0:
          nonretweet_neutral += 1
      if abs(tweet.get('sentiment', 0)) > 2:
        aroused += 1
        if tweet.get('sentiment', 0) > 2:
          positive += 1
        elif tweet.get('sentiment', 0) < 2:
          negative += 1
      elif tweet.get('sentiment', 0) == 0:
        neutral += 1
