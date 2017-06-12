#!/usr/bin/env python
#
# $Id: Hansen2010Diffusion_derose.py,v 1.3 2011/03/03 23:54:36 fn Exp $

from nltk.stem.wordnet import WordNetLemmatizer
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


filebase = '/home/fn/'
filename = filebase + 'fnielsen/data/Nielsen2009Responsible_emotion.csv'
[elements for elements in [ line.split('\t') for line in open(filename) ] if len(elements) != 2 or re.match(r'\w*\s+$', elements[0])]

afinn = dict(map(lambda (k,v): (k,int(v)), 
                 [ line.split('\t') for line in open(filename) ]))

filename = filebase + 'data/derose.txt'
derose = dict(map(lambda w: (w.lower(), 1), re.split('\W+', open(filename).read())))


print(sorted(list(set(derose).difference(afinn))))
