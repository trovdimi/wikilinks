import numpy as np

import os
import os.path
import sys
import zipfile
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.random_projection import SparseRandomProjection
from sklearn.preprocessing import normalize
import cPickle
from scipy.sparse import sparsetools
import tables as tb
from scandir import scandir, walk
from scipy.sparse import csr_matrix
import cStringIO

def sparse_save(matrix, filename, dtype=np.dtype(np.float64)):
    print "SAVE SPARSE"
    print matrix.shape

    atom = tb.Atom.from_dtype(dtype)

    f = tb.open_file(filename, 'w')

    print "saving data"
    filters = tb.Filters(complevel=5, complib='blosc')
    out = f.create_carray(f.root, 'data', atom, shape=matrix.data.shape, filters=filters)
    out[:] = matrix.data

    print "saving indices"
    out = f.create_carray(f.root, 'indices', tb.Int64Atom(), shape=matrix.indices.shape, filters=filters)
    out[:] = matrix.indices

    print "saving indptr"
    out = f.create_carray(f.root, 'indptr', tb.Int64Atom(), shape=matrix.indptr.shape, filters=filters)
    out[:] = matrix.indptr

    print "saving done"

    f.close()

def sparse_read(file, shape):
    h5 = tb.open_file(file, 'r')
    return csr_matrix((h5.root.data[:], h5.root.indices[:], h5.root.indptr[:]), shape=(shape,shape), dtype=np.float32)

articles = []
article_ids = []

i = 0
for dirpath, dirnames, filenames in walk("/home/ddimitrov/wikipedia_html_dump/articles_plaintexts"):
    for filename in [f for f in filenames if f.endswith(".txt")]:
        path = os.path.join(dirpath, filename)
        with open(path) as f:
            articles.append(f.read())
        #f = open(path, 'r')
        #articles.append(f.read())
        article_ids.append(filename.split("_")[1])
    i += 1
    if i % 1000 == 0:
        print i
        #break

f = open('../data/article_ids.p', 'wb')
cPickle.dump(article_ids, f, protocol=-1)

f = open('../data/article_text.p', 'wb')
cPickle.dump(articles, f, protocol=-1)

print "saving done"

print len(articles)

vec = TfidfVectorizer(max_df=0.8, sublinear_tf=True)

X = vec.fit_transform(articles)


print X.shape

proj = SparseRandomProjection()

X = proj.fit_transform(X)

print X.shape

sparse_save(X,"../data/tfidf.h5")

# f = open('X_data.p', 'wb')
# cPickle.dump(X.data, f, protocol=-1)
# f = open('X_indices.p', 'wb')
# cPickle.dump(X.indices, f, protocol=-1)
# f = open('X_indptr.p', 'wb')
# cPickle.dump(X.indptr, f, protocol=-1)

#X = normalize(X)

# compute the inverse of l2 norm of non-zero elements
X.data **= 2
norm = X.sum(axis=1)
n_nzeros = np.where(norm > 0)
norm[n_nzeros] = 1.0 / np.sqrt(norm[n_nzeros])
norm = np.array(norm).T[0]
X.data = np.sqrt(X.data)
# modify sparse_csc_matrix in place
sparsetools.csr_scale_rows(X.shape[0],
                              X.shape[1],
                              X.indptr,
                              X.indices,
                              X.data, norm)

print X.shape
print X[0,:].sum()

sparse_save(X,"../data/tfidf_norm.h5")

# f = open('X_norm_data.p', 'wb')
# cPickle.dump(X.data, f, protocol=-1)
# f = open('X__norm_indices.p', 'wb')
# cPickle.dump(X.indices, f, protocol=-1)
# f = open('X_norm_indptr.p', 'wb')
# cPickle.dump(X.indptr, f, protocol=-1)

#matrix = X.dot(X.T)

# f = open('sim_data.p', 'wb')
# cPickle.dump(matrix.data, f, protocol=-1)
# f = open('sim_indices.p', 'wb')
# cPickle.dump(matrix.indices, f, protocol=-1)
# f = open('sim_indptr.p', 'wb')
# cPickle.dump(matrix.indptr, f, protocol=-1)

#sparse_save(matrix,"sim.h5")

f = open('../data/article_ids.p', 'wb')
cPickle.dump(article_ids, f, protocol=-1)

print "saving done"