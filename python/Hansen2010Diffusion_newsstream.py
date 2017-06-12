#!/usr/bin/env pythhon
#
# $Id: Hansen2010Diffusion_newsstream.py,v 1.3 2010/12/14 19:28:57 fn Exp $

from __future__ import division
import numpy as np
from nltk.corpus import brown
from nltk.classify import NaiveBayesClassifier
import nltk.classify.util
import pylab
from re import compile, findall, UNICODE

filebase = '/home/fn/'


def sents2words(sents):
    return [ set(map(lambda w: w.lower(), pattern_word.findall(j))) for j in sents ]


def word_feats(words):
    return dict([(word, True) for word in words])


pattern_word = compile('[^\W\d_]+', UNICODE)


news_sents = map(lambda words: " ".join(words), brown.sents(categories='news'))
other_sents = map(lambda words: " ".join(words),
                  brown.sents(categories=['reviews', 'religion', 
                                          'hobbies', 'lore',
                                          'belles_lettre', 'government',
                                          'learned', 'fiction', 'mystery',
                                          'science_fiction', 'adventure',
                                          'romance', 'humor']))
news_words = sents2words(news_sents)
other_words = sents2words(other_sents)
news_feats = [(word_feats(wordlist), 'news') for wordlist in news_words ]
other_feats = [(word_feats(wordlist), 'other') for wordlist in other_words ]

news_cutoff = len(news_feats)*3/4
other_cutoff = len(other_feats)*3/4

train_feats = news_feats[:news_cutoff] + other_feats[:other_cutoff]
test_feats = news_feats[news_cutoff:] + other_feats[other_cutoff:]
test_sents = news_sents[news_cutoff:] + other_sents[other_cutoff:] 
print 'train on %d instances, test on %d instances' % (len(train_feats), len(test_feats))
 
classifier = NaiveBayesClassifier.train(train_feats)
print 'accuracy:', nltk.classify.util.accuracy(classifier, test_feats)
classifier.show_most_informative_features(n=100)

P = [ classifier.prob_classify(test_feat[0]).prob('news') for test_feat in test_feats ]
I = np.argsort(-np.asarray(P)) 
for i in I[:20]:
    print(test_sents[i] + "\n")

filename = filebase + 'fnielsen/data/Hansen2010Diffusion_news.txt'
pattern_news = compile("(-?\d) (.+)")
statistics = {'nonenglish': 0, 'other': 0, 'news': 0, 'news1': 0, 'news2': 0}
n = 0
tweet_sents = []
tweet_feats = []
labels = []
for tweet in open(filename):
    if n == 1000:
        break
    m = pattern_news.findall(tweet.strip())
    if m:
        label, sentence = m[0]
        label = int(label)
        labels.append(label)
        tweet_sents.append(sentence)
        wordlist = sents2words([sentence])[0] 
        if label < 0:
            statistics['nonenglish'] += 1
            tweet_feats.append((word_feats(wordlist), 'nonenglish'))
        elif label == 0:
            statistics['other'] += 1
            tweet_feats.append((word_feats(wordlist), 'other'))
        elif label == 1:
            statistics['news'] += 1
            statistics['news1'] += 1
            tweet_feats.append((word_feats(wordlist), 'news'))
        elif label == 2:
            statistics['news'] += 1
            statistics['news2'] += 1
            tweet_feats.append((word_feats(wordlist), 'news'))
        else:
            print("ERROR: " + tweet)
    else:
        print("ERROR: " + tweet)
    n += 1

tweet_p = [ classifier.prob_classify(features).prob('news') for features, label in tweet_feats ]
tweet_i = np.argsort(-np.asarray(tweet_p)) 
n = 1
s1 = ''
for i in tweet_i[:50]:
    print("%3d %2d %.5f %s\n" % (n, labels[i], tweet_p[i], tweet_sents[i]))
    s1 += "%3d & %2d & %.5f & %s\n\\\\\n" % (n, labels[i], tweet_p[i], tweet_sents[i])
    n += 1


    
tweet_j = np.argsort(np.asarray(tweet_p)) 
s2 = ''
n = 1
for j in tweet_j[:50]:
    print("%3d %2d %.5f %s\n" % (n, labels[i], tweet_p[j], tweet_sents[j]))
    s2 += "%3d & %2d & %.5f & %s\n\\\\\n" % (n, labels[j], tweet_p[j], tweet_sents[j])
    n += 1



# Only English
i = list(np.where(np.asarray(labels) != -1)[0])
labels_english = np.asarray(labels).take(i)
tweet_p_english = np.asarray(tweet_p).take(i)

# ROC 
X = [(0, 0)]
for t in [0.0001, 0.001, 0.01, 0.1, 0.1, 0.2, 0.3, 0.5, 0.9, 0.99, 0.999, 0.9999, 0.99999, 0.999999, 0.999999]:
    positives = np.sum(tweet_p_english>t)
    negatives = np.sum(tweet_p_english<t)
    truepositives = np.sum((tweet_p_english>t).__and__(labels_english != 0))
    falsenegatives = np.sum((tweet_p_english<t).__and__(labels_english != 0))
    tpr = truepositives / positives
    fpr = falsenegatives / negatives
    X.append((fpr, tpr))


X.append((1,1))

X = np.asarray(X)
pylab.plot(X[:,0], X[:,1], linewidth=3)
pylab.axis((0, 1, 0, 1))
pylab.xlabel('False positive rate')
pylab.ylabel('True positive rate')
pylab.title('ROC curve for news classifier of English tweets')
pylab.show()


threshold = 0.963
ineg = (tweet_p_english < threshold).nonzero()[0]
ipos  = (tweet_p_english > threshold).nonzero()[0]
p = labels_english.take(ipos)
n = labels_english.take(ineg)

news_ratio = float(len(ipos))/(len(ineg)+len(ipos))
print news_ratio

s = """
         & News (strict) & News (broad) & Other & Total \\\\ \\hline
Positive &     %d        &     %d       & %d    &  %d \\\\
Negative &     %d        &     %d       & %d    &  %d \\\\

""" % (sum(p==2), sum(p>0), sum(p==0), len(p), sum(n==2), sum(n>0), sum(n==0), len(n))
print(s)
