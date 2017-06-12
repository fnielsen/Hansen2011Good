#!/usr/bin/env python
#
# $Id: Hansen2010Diffusion_preparenews.py,v 1.1 2010/12/10 13:34:16 fn Exp $

s = open('mat_rows_tweets.txt').read().split('\n')
random.shuffle(s, random=lambda: 0.42)


f = open('mat_rows_tweets_newslabel.txt', 'w')
f.write("\n".join(s[:2000]))
f.close()
