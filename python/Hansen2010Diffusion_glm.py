#!/usr/bin/env python
#
# $Id: Hansen2010Diffusion_glm.py,v 1.6 2010/11/08 08:52:21 fn Exp $

# oauth
# Download retweeted tweets
# Investigate COP15 tweet for sentimental retweet
# Most retweeted tweets from COP15.

# There is an issue with 'user' not existing 
# for tweet in tweets.find({"delete": {"$exists": False}, "user": {"$exists": False}}): print(tweet)
# {u'scrub_geo': {u'user_id': 92035237, u'up_to_status_id': 21814937600L}, u'_id': ObjectId('4c8f70b8f95118b062b71b87')}
# Apparently only one. (Is that an interrupted download)



from __future__ import division
import pymongo
from re import compile, findall, search, IGNORECASE, UNICODE

connection = pymongo.Connection()
db = connection.twitter
tweets = db.tweets

pattern_url = compile(r"http://", IGNORECASE)

pattern_mention = compile(r"@\w")  # This pattern is not sufficient to exclude retweets.
pattern_mention1 = compile(r"((?:\b(?:RT|via):?\s*)?@\w+)")
pattern_mention2 = compile(r"^(?:RT|via)")

pattern_hashtag = compile(r"#\w")
stringpatterns_retweet = [ r"^RT @", r"^RT\b", r"\bRT\b", r"\b(?:RT\b|via\s@)"]
patterns_retweet = [ compile(s, UNICODE) for s in stringpatterns_retweet ]

f = open("Hansen2010Diffusion_glm.csv", "w")
f.write("""id, retweet, url, mention, hashtag, followers, followees, length, englishness, enlang, valence, arousal, normvalence, normarousal\n""")

n = 0
for tweet in tweets.find({"delete": {"$exists": False}, "user": {"$exists": True}}):
    text = tweet.get('text', '')
    id = tweet.get('id', '')
    retweet = int(bool(search(patterns_retweet[-1], text)))
    url = int(bool(search(pattern_url, text)))
    mention = int(bool(filter(lambda t: not search(pattern_mention2, t), findall(pattern_mention1, text))))
    hashtag = int(bool(search(pattern_hashtag, text)))
    followers = tweet['user']['followers_count']
    followees = tweet['user']['friends_count']
    length = len(text)
    englishness = tweet.get('englishness', 0)
    enlang = int(tweet.get('user', {}).get('lang') == 'en')
    valence = tweet.get('sentiment', 0)
    arousal = tweet.get('arousal', 0)
    f.write(', '.join(map(str, [id, retweet, url, mention, hashtag, 
                                followers, followees,
                                length, 
                                englishness, enlang, valence, arousal, 
                                valence/(length+0.0001),
                                abs(valence)/(length+0.0001) ])) + "\n")
    n += 1
    if not n % 10000:
        print(n)

f.close()
