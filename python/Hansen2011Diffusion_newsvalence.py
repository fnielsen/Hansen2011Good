# $Id: Hansen2011Diffusion_newsvalence.py,v 1.1 2011/10/30 23:36:06 fn Exp $

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


filebase = "/home/fnielsen/"
filename = filebase + "/tmp/AFINN/AFINN-111.txt"

afinn = dict(map(lambda (w, s): (unicode(w, 'utf-8'), int(s)), [ 
            ws.strip().split('\t') for ws in open(filename) ]))

x = []
y = []
z = []
t = []
for k,v in afinn.items():
    x.append(v)
    y.append(classifier_other.prob_classify({k: True}).prob('news'))
    z.append(classifier_others.prob_classify({k: True}).prob('news'))
    t.append(k)


from matplotlib import pyplot as plt
import numpy as np

plt.figure(1)
plt.scatter(x, z)
plt.xlabel('AFINN valence')
plt.ylabel('Newsness probability')
plt.show()
plt.title("Valence and newsness of individual words")
plt.text(1.5, 0.6, "r = %.3f" % np.corrcoef(x, y)[0,1])
for n in range(-5, 6):
    plt.scatter(n, np.median(np.asarray(z)[np.where(np.asarray(x) == n)]), 
                s=200, c='g', alpha=0.5)


sorted(zip(z,t))

# plt.savefig(filebase + "/fnielsen/eps/Hansen2011Diffusion_newsvalence.eps")
