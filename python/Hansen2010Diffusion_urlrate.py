#!/usr/bin/env python

from __future__ import division
import pymongo
from re import compile, search, IGNORECASE, UNICODE

connection = pymongo.Connection()
db = connection.twitter
tweets = db.tweets

pattern_url = compile(r"http://", IGNORECASE)
stringpatterns_retweet = [ r"^RT @", r"^RT\b", r"\bRT:?\s*@\w+", r"(?:\bRT|\bvia):?\s*@\w+", r"\bRT\b" ]
patterns_retweet = [ compile(s, UNICODE) for s in stringpatterns_retweet ]

total = 0
withurls = 0 
retweets = [ 0 ] * len(stringpatterns_retweet)
retweets_withurls = [ 0 ] * len(stringpatterns_retweet)
for tweet in tweets.find({"delete": {"$exists": False}}):
    total += 1
    if search(pattern_url, tweet.get('text', '')):
        withurls += 1
        urlpresent = True
    else:
        urlpresent = False
    for n in range(len(patterns_retweet)):
        if search(patterns_retweet[n], tweet.get('text', '')):
            retweets[n] += 1
            if urlpresent:
                retweets_withurls[n] += 1
    if not total % 10000:
        print("""
Total                       %23d    100.0%% 
With URLs                   %23d    %5.1f%%""" % (total, withurls, 100*withurls/total))
        for n in range(len(patterns_retweet)):
            print("""Retweet           %25s %7d    %5.1f%% of total
Retweet with URLs %25s %7d    %5.1f%% of total 
                                                       %5.1f%% of retweets 
                                                       %5.1f%% of tweets with URLs""" % (
                    stringpatterns_retweet[n], retweets[n], 
                    100*retweets[n]/total, 
                    stringpatterns_retweet[n], 
                    retweets_withurls[n], 100*retweets_withurls[n]/total,
                    100*retweets_withurls[n]/retweets[n],
                    100*retweets_withurls[n]/withurls))
