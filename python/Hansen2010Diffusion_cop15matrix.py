#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# $Id: Hansen2010Diffusion_cop15matrix.py,v 1.4 2010/11/16 19:05:53 fn Exp $



from cgi  import escape
import datetime
import getopt
import numpy 
import math
from matplotlib.font_manager import FontProperties
from os        import rename
import pylab
from pysqlite2 import dbapi2 as sqlite
from random    import choice
from re        import compile, findall, search, sub, split, IGNORECASE, UNICODE
from scipy import sparse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from time             import sleep, time
from urllib           import FancyURLopener, urlencode, urlretrieve, urlopen
from xml.sax.saxutils import unescape as unescape_saxutils

# filenameDatabase = '/var/local/www/rbb.sqlite'
filename_database = '../rbb.sqlite-2010-02-18'

filename_valence = '../../../fnielsen/data/Nielsen2009Responsible_emotion.csv'
filename_stopwords = '../../../matlab/brede/data/stop_english1.txt'
filename_englishness = '../../../fnielsen/data/Nielsen2010Responsible_english.csv'
filename_users = '../cop_15_info.txt'

englishness = dict(map(lambda (w,e): (w, int(e)),[ line.strip().split('\t') for line in open(filename_englishness) ]))

debug = True

users = [ line.split(',') for line in open(filename_users) ]
followers = dict(map(lambda user: (user[0], int(user[2])), users))
following = dict(map(lambda user: (user[0], int(user[1])), users))


def nmf_sparse(M, components=5, iterations=100):
    if debug:
        print("Initializing")
    W = numpy.mat(numpy.random.rand(M.shape[0], components))
    H = numpy.mat(numpy.random.rand(components, M.shape[1]))
    if debug:
        print("Iterating")
    if components == 1:
        for n in range(0, iterations): 
            H = numpy.multiply(H, (W.T * M) / (W.T * W * H + 0.001))
            W = numpy.multiply(W, (M * H.T) / (W * (H * H.T) + 0.001))
            if debug: 
                print "%d/%d" % (n, iterations)
    else:
        for n in range(0, iterations): 
            H = numpy.multiply(H, (W.T * M).todense() / (W.T * W * H + 0.001))
            W = numpy.multiply(W, (M * H.T).todense() / (W * (H * H.T) + 0.001))
            if debug: 
                print "%d/%d" % (n, iterations)
    sumW = sum(W)
    sumH = sum(H.T)
    sqrtsumWH = numpy.sqrt(numpy.multiply(sumW, sumH))
    W = numpy.multiply(W, numpy.mat(numpy.ones((M.shape[0], 1))) * (sqrtsumWH / sumW))
    H = numpy.multiply(H, (sqrtsumWH / sumH).T * numpy.mat(numpy.ones((1, M.shape[1]))))
    return (W, H)

pattern_words = compile(r"""(?:\w+(?:-\w+)?|http://\S+)""")
pattern_http = compile(r"""http://\S+""")
pattern_retweet = compile(r"\b(?:RT\b|via\s@)", UNICODE)
pattern_lt = compile(r"&lt;", IGNORECASE)
pattern_gt = compile(r"&gt;", IGNORECASE)

pattern_url = compile(r"http://", IGNORECASE)
pattern_strip = compile(r"((?:http://\S+)|(?:@\w+))", IGNORECASE)
pattern_mention = compile(r"@\w")  # This pattern is not sufficient to exclude retweets.
pattern_mention1 = compile(r"((?:\b(?:RT|via):?\s*)?@\w+)")
pattern_mention2 = compile(r"^(?:RT|via)")
pattern_hashtag = compile(r"#\w")
stringpatterns_retweet = [ r"^RT @", r"^RT\b", r"\bRT\b", r"\b(?:RT\b|via\s@)"]
patterns_retweet = [ compile(s, UNICODE) for s in stringpatterns_retweet ]


connection = sqlite.connect(filename_database)
cursor = connection.cursor()


# 147041 December tweets with sentiment and no language code filter.
# 136260 after englishness filter.
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


f = open("Hansen2010Diffusion_cop15glm.csv", "w")
f.write("""retweet, url, mention, hashtag, length, lengthnourl, ambivalence, valence, arousal, normvalence, normarousal, followers, following\n""")
frows = open('mat_rows.txt', 'w')
frows_date = open('mat_rows_date.txt', 'w')
frows_user = open('mat_rows_user.txt', 'w')
frows_tweets = open('mat_rows_tweets.txt', 'w')
frows_valence = open('mat_rows_valence.txt', 'w')
frows_retweet = open('mat_rows_retweet.txt', 'w')


tweets = []
n = 1
for (language, text, date, to_user, source, user, user_id, to_user_id, id, query, valence, ambivalence) in cursor: 
    text = pattern_gt.sub('>', pattern_lt.sub('<', text))
    textstripped = pattern_strip.sub(' ', text)
    words = pattern_words.findall(textstripped)
    english = sum(map(lambda w: englishness.get(w, 0), words))
    if True or english > 0:
        frows_valence.write(str(valence) + '\n');
        frows.write(sub('\n', ' ', str(text)) + '\n');
        frows_date.write(sub('\n', ' ', str(date)) + '\n');
        frows_user.write(sub('\n', ' ', str(user)) + '\n');
        t = sub('\n', ' ', str(text))
        frows_tweets.write(sub('\r', ' ', t) + '\n');
        if pattern_retweet.search(str(text)):
            frows_retweet.write('1\n')
        else:
            frows_retweet.write('0\n')
        t = {}
        t['words'] = words
        tweets.append(t)
        retweet = int(bool(search(patterns_retweet[-1], text)))
        url = int(bool(search(pattern_url, text)))
        mention = int(bool(filter(lambda t: not search(pattern_mention2, t), findall(pattern_mention1, text))))
        hashtag = int(bool(search(pattern_hashtag, text)))
        length = len(text)
        lengthnourl = len(text) - sum([len(t) for t in pattern_strip.findall(text)])
        nfollowers = followers.get(user, -2)
        nfollowing = following.get(user, -2)
        if nfollowers>-1:
            sfollowers = str(nfollowers)
        else:
            sfollowers = 'NA'
        if nfollowing>-1:
            sfollowing = str(nfollowing)
        else:
            sfollowing = 'NA'
        f.write(', '.join(map(str, [retweet, url, mention, hashtag, 
                                    length, lengthnourl, ambivalence,
                                    valence, abs(valence), 
                                    valence/(length+0.0001),
                                    abs(valence)/(length+0.0001),
                                    sfollowers, sfollowing ])) + "\n")

        if not (n % 100):
            print(n)
        n += 1

frows.close()
frows_date.close()
frows_user.close()
frows_tweets.close()
frows_valence.close()
frows_retweet.close()
f.close()


#n = 1
#for n in range(len(tweets)):
#    tweets[n]['links'] = pattern_http.findall(tweets[n]['text'])
#    if not (n % 100) and debug:
#        print(n)
#    n += 1

#n = 1
#for n in range(len(tweets)):
#    text = pattern_http.sub(' ', tweets[n]['text'])
#    tweets[n]['words'] = pattern_words.findall(text)
#    if not (n % 100) and debug:
#        print(n)
#    n += 1


allwords = []
n = 1
for tweet in tweets:
    allwords.extend(tweet['words'])
    if not (n % 100) and debug:
        print(n)
    n += 1

alllowerwords = map(lambda s: s.lower(), allwords)

stopwords = [ line.strip() for line in open(filename_stopwords) ]
stopwords.extend(['rt', 'cop15', 'climate', 'copenhagen', 'change'])
stopwords = dict(map(lambda word: (word, 1), stopwords))

wordcount = {}
n = 1
for term in alllowerwords:
    if term not in stopwords:
        wordcount[term] = wordcount.get(term, 0) + 1

items = [ (v,k) for k,v in wordcount.items() ]
items.sort(reverse=True)

if debug: 
    for n in range(0,500):
        print('%3d: %4d "%s"' % (n+1, items[n][0], items[n][1]))

terms = {}
for n in range(min(len(items),10000)):
    terms[items[n][1]] = n



if False:
    M = {}
    M['matrix'] = sparse.lil_matrix((len(tweets), len(terms)))
    M['rows'] = []

    for n in range(len(tweets)):
        M['rows'].append(tweets[n]['id'])
        for word in tweets[n]['words']:
            if word in terms:
                M['matrix'][n,terms[word]] = 1
            if not (n % 100) and debug:
                print(n)

    M['columns'] = [ '' for term in terms ]
    for term in terms:
        M['columns'][terms[term]] = term


wordsvalence = dict([ line.strip().split('\t') for line in open(filename_valence).readlines() ])
termterm = [ '' for term in terms ]
for term in terms:
    termterm[terms[term]] = term

if True:
    # Write files with data
    fmatrix = open('mat_indices.txt', 'w')
    for n in range(len(tweets)):
        for word in set(tweets[n]['words']):
            if word in terms:
                fmatrix.write('%d %d %d\n' % (n, terms[word], 1))
        if not n % 100:
            print(n)
    fmatrix.close()


fcolumns_valence = open('mat_columns_valence.txt', 'w')
fcolumns = open('mat_columns.txt', 'w')
for term in termterm:
    fcolumns_valence.write(wordsvalence.get(term, '0') + '\n')
    fcolumns.write(term + '\n')

fcolumns_valence.close()
fcolumns.close()


if False: 
    for components in [1, 2, 5, 10, 20, 50, 100, 200]:


        # Non-negative matrix factorization
        [W,H] = nmf_sparse(M['matrix'], components=components)


        for n in range(components):
            print("\n" +str(n) + "-" * 70)
            w = []; h = []
            for m in range(W.shape[0]):
                w.append((W[m,n], tweets[m]))
            for m in range(H.shape[1]):
                h.append((H[n,m], M['columns'][m]))
            h.sort(reverse=True)
            w.sort(reverse=True)
            if debug:
                for m in range(0,40):
                    print "%5.5f %10s %15s %s" % (h[m][0], h[m][1], w[m][1]['user'], w[m][1]['text'])


        f = open('mat-%03d.html' % (components,), 'w')
        f.write("""
    <html>
      <head>
        <style type="text/css">
          a:link { text-decoration: none; }
          a:visited { text-decoration: none; }
          a:hover, a.active { text-decoration: underline; }
          a.external { color: #3366bb }
          table.navigationbar { border: 0px; width: 100%; }
          td.navigationbar { text-align: left; }
          table { margin: 1em 1em 1em 0; background: #f9f9f9; 
                  border: 1px #aaa solid; border-collapse: collapse; font-size:small; width="100%" }
          th, td {  border: 1px #aaa solid; padding: 0.2em; }
          th { background: #f2f2f2; text-align: center; }
          td { text-align: center; }
          div.error { color: #ff0000; }
        </style>
      </head>
      <body>
        """)
        for n in range(components):
            w = [ (W[m,n], tweets[m]) for m in range(W.shape[0]) ]
            h = [ (H[n,m], M['columns'][m]) for m in range(H.shape[1]) ]
            h.sort(reverse=True)
            w.sort(reverse=True)
            f.write("""
            <h2>Topic %d</h2>
            <table style="border: none;">
              <tr>
                <td>
                  <img src="mat-%03d-%03d.png">""" % (n+1, components, n+1))
            f.write("""<td>""")
            for m in range(40):
                f.write("""<font size="%d">%s </font>""" % (int(math.ceil(h[m][0])), h[m][1],))
            f.write("""</table>""")
            f.write("""
            <table >
              <tr>
                <th>Date
                <th>User
                <th>Text
            """)
            for m in range(40):
              f.write("""      <tr>
                <td>%10s
                <td><a href="http://twitter.com/%s">%15s</a>
                <td>%s\n""" % (w[m][1]['date'], w[m][1]['user'], w[m][1]['user'], escape(w[m][1]['text'])))
            f.write("""    </table>\n""")
            w = []; h = []
            for m in range(W.shape[0]):
                w.append((W[m,n], tweets[m]))
            w.sort(reverse=True)
            wdate = {}
            positive = {}
            negative = {}
            for d in range(1,32):
                for h in range(23):
                    key = u'2009-12-%02d' % (d,)
                    wdate[key] = 0.0 
                    positive[key] = 0.0 
                    negative[key] = 0.0  
                    # wdate[u'2009-12-%02d %02d' % (d, h)] = 0 
            for m in range(1000):
                key = w[m][1]['date'][:10]
                if key in wdate:
                    wdate[key] += w[m][0]
                    valence = w[m][1]['valence']
                    if valence > 0:
                        positive[key] += valence * w[m][0]
                    elif valence < 0:
                        negative[key] += abs(valence) * w[m][0]
            wdatea = [ (k,v) for k,v in wdate.items() ]
            wdatea.sort()
            positivea = [ (k,v) for k,v in positive.items() ]
            negativea = [ (k,v) for k,v in negative.items() ]
            positivea.sort()
            negativea.sort()
            pylab.clf()
            g = pylab.plot(range(1,32), map(lambda x: x[1], wdatea))
            g = pylab.plot(range(1,32), map(lambda x: x[1], positivea), 'g')
            g = pylab.plot(range(1,32), map(lambda x: x[1], negativea), 'r')
            g = pylab.xlabel('December')
            g = pylab.ylabel('Topic activity')
            g = pylab.legend(('Topic activity', 'Weighted by positives', 'Weighted by negatives'), prop = FontProperties(size='smaller'))
            pylab.savefig('mat-%03d-%03d' % (components, n+1))


        f.write("""
          </body>
        </html>""")
        f.close()


    # pylab.show()

