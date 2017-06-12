#!/usr/bin/env python
#
# $Id: Hansen2010Diffusion_news.py,v 1.3 2010/11/26 12:31:44 fn Exp $

import numpy as np
from nltk.corpus import brown
from nltk.classify import NaiveBayesClassifier
import nltk.classify.util
from re import compile, findall, UNICODE

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


tweet_sents = [ tweet.strip() for tweet in open('mat_rows_tweets.txt') ]
tweet_words = sents2words(tweet_sents) 
tweet_feats = [(word_feats(wordlist), 'unknown') for wordlist in tweet_words ]
tweet_p = [ classifier.prob_classify(feat[0]).prob('news') for feat in tweet_feats ]
tweet_i = np.argsort(-np.asarray(tweet_p)) 
for i in tweet_i[:20]:
    print(tweet_sents[i] + "\n")

tweet_j = np.argsort(np.asarray(tweet_p)) 
for j in tweet_j[:50]:
    print(tweet_sents[j] + "\n")

f = open('mat_rows_newsness.txt', 'w')
f.write('newsness\n')
f.write("\n".join(map(str, tweet_p)))
f.close()
