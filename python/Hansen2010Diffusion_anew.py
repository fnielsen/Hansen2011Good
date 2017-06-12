#!/usr/bin/env python
#
# $Id: Hansen2010Diffusion_anew.py,v 1.3 2010/12/15 15:50:39 fn Exp $

from nltk.stem.wordnet import WordNetLemmatizer
import nltk
import numpy as np
import pylab
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


filebase = '/home/fn/'
filename = filebase + 'fnielsen/data/Nielsen2009Responsible_emotion.csv'
swords = dict(map(lambda (k,v): (k,int(v)), 
                  [ line.split('\t') for line in open(filename) ]))

filename = filebase + 'data/ANEW.TXT'
anew = dict(map(lambda l: (l[0], float(l[2])) , [ re.split('\s+', line) for line in open(filename).readlines()[41:1075] ]))

lemmatizer = WordNetLemmatizer()
stemmer = nltk.PorterStemmer()

anew_stem = dict([ (stemmer.stem(word), valence) for word, valence in anew.items() ])

def word2anewsentiment(word):
    sentiment = None
    if word in anew:
        sentiment = anew[word]
    else:
        lword = lemmatizer.lemmatize(word)
        if lword in anew:
            sentiment = anew[lword]
        else:
            lword = lemmatizer.lemmatize(word, pos='v')
            if lword in anew:
                sentiment = anew[lword]
    return sentiment


def word2anewsentiment_stem(word):
    return anew_stem.get(stemmer.stem(word), None)



sentiments = []
for word in swords.keys():
    sentiment_anew = word2anewsentiment(word)
    if sentiment_anew:
        sentiments.append((swords[word], sentiment_anew))
        if (swords[word] > 0 and sentiment_anew < 5) or \
                (swords[word] < 0 and sentiment_anew > 5):
            print(word)
        

sentiments_stem = []
for word in swords.keys():
    sentiment_stem_anew = word2anewsentiment_stem(word)
    if sentiment_stem_anew:
        sentiments_stem.append((swords[word], sentiment_stem_anew))
        if (swords[word] > 0 and sentiment_stem_anew < 5) or \
                (swords[word] < 0 and sentiment_stem_anew > 5):
            print(word)
        

sentiments = np.asarray(sentiments)
pylab.plot(sentiments[:,0], sentiments[:,1], '.')
pylab.xlabel('Our list')
pylab.ylabel('ANEW')
pylab.title('Correlation between sentiment word lists')
pylab.text(1, 4, "Correlation = %.2f" % np.corrcoef(sentiments.T)[1,0])
pylab.show()


sentiments_stem = np.asarray(sentiments_stem)
pylab.plot(sentiments_stem[:,0], sentiments_stem[:,1], '.')
pylab.xlabel('My list')
pylab.ylabel('ANEW')
pylab.title('Correlation between sentiment word lists')
pylab.text(1, 4, "Correlation = %.2f" % np.corrcoef(sentiments_stem.T)[1,0])
pylab.show()





