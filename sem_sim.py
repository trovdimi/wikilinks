import tables as tb
from scipy.sparse import csr_matrix
import numpy as np
import cPickle
import datetime

article_ids = cPickle.load(open("../data/article_ids.p"))
vocab = {int(x):i for i,x in enumerate(article_ids)}

print "loaded articles"

f = open('../data/links_unique.p', 'r')
links = cPickle.load(f)

print "loaded links"

#links_unique = list(set([tuple(sorted(tuple_)) for tuple_ in links]))

print "unique links"

h5 = tb.open_file("/home/psinger/WikiLinks/data/tfidf_norm.h5", 'r')
shape = (4805440, 13187)
tfidf = csr_matrix((h5.root.data[:], h5.root.indices[:], h5.root.indptr[:]), shape=shape, dtype=np.float64)
h5.close()

print "loaded tfidf"

import numpy as np
chunks = np.array_split(links,30)

print "chunks"

print datetime.datetime.now()

def sem_sim(links, idx):
    i = 0
    sim = {}
    for row in links:

        i += 1
        if i % 10000 == 0:
            print idx, i
            #break
        #if i % 1000000 == 0:
        #    f = open('../data/sem_sim/' + str(idx) + "/" + str(i) + '.p', 'wb')
        #    cPickle.dump(sim, f, protocol=-1)
        #    sim = {}
        #    break

        try:
            s = vocab[row[0]]
            t = vocab[row[1]]
        except:
            continue

        if s == t:
            sim[(s,t)] = 1.

        a = tfidf.getrow(s)#.todense()
        b = tfidf.getrow(t)#.todense()
        sim[(row[0], row[1])] = a.dot(b.T)[0,0]

    if len(sim) != 0:
        #f = open('../data/sem_sim/' + str(idx) + "_" + str(i) + '.p', 'wb')
        f = open('../data/sem_sim/' + str(idx) + '.p', 'wb')
        cPickle.dump(sim, f, protocol=-1)

from joblib import Parallel, delayed



Parallel(n_jobs=30, backend="multiprocessing")(delayed(sem_sim)(chunks[i],i) for i in range(30))

print datetime.datetime.now()