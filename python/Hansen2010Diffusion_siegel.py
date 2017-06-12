#!/usr/bin/env python
#
# $Id: Hansen2010Diffusion_siegel.py,v 1.1 2010/12/21 16:47:07 fn Exp $

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
afinn = dict(map(lambda (k,v): (k,int(v)), 
                 [ line.split('\t') for line in open(filename) ]))

filename = filebase + 'data/words.prn'
asiegel = dict(map(lambda l: (l[1], float(l[2])) , [ re.split('\s+', line) for line in open(filename).readlines()[1:] ]))

asiegel_positive = [ word for word, valence in asiegel.items() if valence == 1 ]
asiegel_negative = [ word for word, valence in asiegel.items() if valence == 2 or valence == 3 ]

# These should all be positive:
[ afinn[word] for word in asiegel_positive ]

# These should all be negative:
[ word for word in asiegel_negative if not afinn.has_key(word) ]


set(asiegel).difference(afinn)

