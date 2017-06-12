#!/usr/bin/env python
#
# $Id: Hansen2010Diffusion_cop15csv.py,v 1.5 2012/08/23 15:01:01 fn Exp $

from __future__ import division
from pysqlite2 import dbapi2 as sqlite
from re import compile, search, findall, sub, IGNORECASE, UNICODE
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

filenameDatabase = '/var/local/www/rbb.sqlite'


pattern_words = compile(r"""(?:\w+(?:-\w+)?|http://\S+)""")
pattern_http = compile(r"""http://\S+""")

pattern_url = compile(r"http://", IGNORECASE)
pattern_url_capture = compile(r"(http://\S+)", IGNORECASE)
pattern_mention = compile(r"@\w")  # This pattern is not sufficient to exclude retweets.
pattern_mention1 = compile(r"((?:\b(?:RT|via):?\s*)?@\w+)")
pattern_mention2 = compile(r"^(?:RT|via)")
pattern_hashtag = compile(r"#\w")
stringpatterns_retweet = [ r"^RT @", r"^RT\b", r"\bRT\b", r"\b(?:RT\b|via\s@)"]
patterns_retweet = [ compile(s, UNICODE) for s in stringpatterns_retweet ]

f = open("Hansen2010Diffusion_cop15csv.csv", "w")
f.write("""retweet, url, mention, hashtag, length, lengthnourl, ambivalence, valence, arousal, normvalence, normarousal\n""")

frows_user = open('mat_rows_user.txt', 'w')


connection = sqlite.connect(filenameDatabase)
cursor = connection.cursor()


# 147041 December tweets with sentiment and no language code filter.
sql = """SELECT 
             iso_language_code, 
             text, 
             created_at, 
             to_user,
             source, 
             from_user, 
             from_user_id,
             to_user_id, 
             tweets.id,
             query,
             valence,
             ambivalence
           FROM tweets, tweets_sentiment
           WHERE tweets.id = tweets_sentiment.id
             AND iso_language_code = 'en' 
             AND query = 'cop15'
             AND created_at > "2009-12-00" 
             AND created_at < "2009-12-32"
           ORDER BY created_at
           ;"""

cursor.execute(sql)


n = 1
for (language, text, date, to_user, source, user, user_id, to_user_id, id, query, valence, ambivalence) in cursor: 
    retweet = int(bool(search(patterns_retweet[-1], text)))
    url = int(bool(search(pattern_url, text)))
    mention = int(bool(filter(lambda t: not search(pattern_mention2, t), findall(pattern_mention1, text))))
    hashtag = int(bool(search(pattern_hashtag, text)))
    length = len(text)
    lengthnourl = len(text) - reduce(lambda x,y: len(x)+len(y), pattern_url_capture.findall(text))

    f.write(', '.join(map(str, [retweet, url, mention, hashtag, 
                                length, lengthnourl, ambivalence,
                                valence, abs(valence), 
                                valence/(length+0.0001),
                                abs(valence)/(length+0.0001) ])) + "\n")
    frows.write(re.sub('\n', ' ', user), 
    n += 1



f.close()
frows_user.close()




