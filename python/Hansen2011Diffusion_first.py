#!/usr/bin/env python
#
# $Id: Hansen2011Diffusion_first.py,v 1.2 2012/10/11 07:26:52 fn Exp $

from __future__ import division

import collections
import numpy as np
import re
import simplejson
import subprocess
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

filebase = "/home/fnielsen/"

pattern_split = re.compile(r"\W+", re.UNICODE)
pattern_word = re.compile(r"(?:http://\S+|\w+(?:-\w+)?)", re.UNICODE)
pattern_http = re.compile(r"http://\S+", re.UNICODE)

pattern_url = re.compile(r"http://", re.IGNORECASE | re.UNICODE)
pattern_url_capture = re.compile(r"(http://\S+)", re.IGNORECASE | re.UNICODE)
pattern_mention = re.compile(r"@\w", re.UNICODE)  # This pattern is not sufficient to exclude retweets.
pattern_mention1 = re.compile(r"((?:\b(?:RT|via):?\s*)?(?<!\w)@\w+)", re.UNICODE)
pattern_mention2 = re.compile(r"^(?:RT|via)", re.UNICODE)
pattern_hashtag = re.compile(r"#[^\W0-9]", re.UNICODE)
stringpatterns_retweet = [ r"^RT @", r"^RT\b", r"\bRT\b", r"\b(?:RT\b|via\s@)"]
patterns_retweet = [ re.compile(s, re.UNICODE) for s in stringpatterns_retweet ]


filename = '/home/fnielsen/fnielsen/data/Nielsen2010Responsible_english.csv'
englishwords = dict(map(lambda (k,v): (unicode(k, 'utf-8'), int(v)), 
                        [ line.split() for line in open(filename) ]))
def englishness(text):
    return sum(map(lambda word: englishwords.get(word.lower(),0), 
                   pattern_word.findall(text)))


filename_stopwords = filebase + '/matlab/brede/data/stop_english1.txt'
stopwords = [ line.strip() for line in open(filename_stopwords) ]
stopwords = dict(zip(stopwords, stopwords))

filename_afinn = filebase + '/Downloads/AFINN/AFINN-111.txt'
filename_afinn = filebase + '/fnielsen/data/Nielsen2009Responsible_emotion.csv'
afinn = dict(map(lambda (w, s): (unicode(w, 'utf-8'), int(s)), [ 
            ws.strip().split('\t') for ws in open(filename_afinn) ]))


def sentiment(text, norm='mean'):
    """
    (sentiment, arousal, ambivalence, positive, negative) = sentiment(test)
    """
    words_with_stopwords = pattern_word.findall(text.lower())
    # Exclude stopwords:
    words = filter(lambda w: not stopwords.has_key(w), words_with_stopwords)
    sentiments = map(lambda word: afinn.get(word, 0), words)
    keys = ['sentiment', 'arousal', 'ambivalence', 'positive', 'negative']
    if sentiments:
        sentiments = np.asarray(sentiments).astype(float)
        sentiment = np.sum(sentiments)
        arousal = np.sum(np.abs(sentiments))
        ambivalence = arousal - np.abs(sentiment)
        positive = np.sum(np.where(sentiments>0, sentiments, 0))
        negative = - np.sum(np.where(sentiments<0, sentiments, 0))
        result = np.asarray([sentiment, arousal, ambivalence, positive, negative])
        if norm == 'mean':
            result /= len(sentiments)
        elif norm == 'sum':
            pass
        elif norm == 'sqrt':
            result /= np.sqrt(len(sentiments))
        else:
            raise("Wrong ''norm'' argument")
    else:
        result = (0, 0, 0, 0, 0)
    return dict(zip(keys, result))


wordcount = collections.defaultdict(int)

f = open("Hansen2011Diffusion_first.csv", "w")
f.write("""id, retweet, url, mention, hashtag, length, lengthnourl, ambivalence, arousal, negative, positive, valence\n""")


cmdargs = ['gzip', '-cd', 'first300000.json.gz']
process = subprocess.Popen(cmdargs, shell=False, stdout=subprocess.PIPE)
for n in xrange(10000):
    tweet = simplejson.loads(process.stdout.readline())
    if not tweet.has_key('delete'):
        if tweet['user']['lang'] == 'en' and englishness(tweet['text']) > 0:
            text = tweet['text']
            retweet = int(bool(patterns_retweet[-1].search(text)))
            url = int(bool(re.search(pattern_url, text)))
            # tweet['entities']['user_mentions'] also has retweets
            mention = int(bool(filter(lambda t: not pattern_mention2.search(t), pattern_mention1.findall(text))))
            length = len(text)
            urltexts = pattern_url_capture.findall(text)
            if urltexts: 
                lengthnourl = len(text) - reduce(lambda x,y: x+len(y), urltexts, 0)
            else:
                lengthnourl = length
            hashtags = len(tweet['entities']['hashtags'])
            d = sentiment(tweet['text'], norm="sqrt")
            f.write(', '.join(map(str, [tweet['id'], retweet, url, mention, int(bool(hashtags)), 
                                        length, lengthnourl, d['ambivalence'],
                                        d['arousal'], d['negative'], d['positive'], d['sentiment']]
                                  )) + "\n")

f.close()

# fulldata = read.csv("Hansen2011Diffusion_first.csv")
# data_arousal = fulldata[fulldata$arousal>0,]
# summary(glm(retweet ~ arousal + hashtag + url + mention + length, data=data_arousal, family=binomial))
