import scipy.stats as stats
import matplotlib.pyplot as plt
import MySQLdb
from wsd.database import MySQLDatabase
import matplotlib.cm as cm
from matplotlib.colors import LogNorm, Normalize, BoundaryNorm, PowerNorm
from conf import *
from collections import defaultdict
import cPickle as pickle
import numpy as np
import pylab
from scipy.stats.stats import pearsonr,spearmanr,kendalltau
import math
import cPickle as pickle
import powerlaw
import matplotlib.mlab as mlab
import random
from scipy.sparse import csr_matrix
from scipy.special import gammaln
from collections import defaultdict
import os
import array
from scipy.sparse.sparsetools import csr_scale_rows
from joblib import Parallel, delayed


from matplotlib import style
style.use('acm-3col-bmh')

import pylab
params = {
    'font.family' : 'serif',
    'font.serif' : ['Times New Roman'],
    'font.size' : 7
}
pylab.rcParams.update(params)




def read_pickle(fpath):
    with open(fpath, 'rb') as infile:
        obj = pickle.load(infile)
    return obj


def write_pickle(fpath, obj):
    with open(fpath, 'wb') as outfile:
        pickle.dump(obj, outfile, -1)

def normalized_entropy():
    transition_matrix = pickle.load( open( SSD_HOME+"pickle/transition_matrix", "rb" ) )
    print "loaded transitions"
    graph = pickle.load( open( SSD_HOME+"pickle/graph", "rb" ) )
    print "loaded graph"
    values = pickle.load( open( SSD_HOME+"pickle/values", "rb" ) )


    vocab = pickle.load( open( SSD_HOME+"pickle/vocab", "rb" ) )
    print "loaded vocab"

    state_count = len(vocab)
    states = vocab.keys()
    shape = (state_count, state_count)



    # structural hypothesises
    hyp_structural = csr_matrix((values, (graph[0], graph[1])),
                                shape=shape, dtype=np.float)



    transitions = csr_matrix((transition_matrix[2], (transition_matrix[0], transition_matrix[1])),
                             shape=shape)

    del transition_matrix

    #delete all zero rows from all  see  http://stackoverflow.com/questions/31188141/scipy-sparse-matrix-remove-the-rows-whose-all-elements-are-zero
    print transitions.shape
    nonzero_row_indice, _ = transitions.nonzero()
    unique_nonzero_indice = np.unique(nonzero_row_indice)
    transitions = transitions[unique_nonzero_indice]
    print transitions.shape

    hyp_data = csr_matrix(transitions, copy=True)
    print hyp_data.shape

    hyp_structural = hyp_structural[unique_nonzero_indice]
    #norm the data
    norm_h = hyp_data.sum(axis=1)
    n_nzeros = np.where(norm_h > 0)
    norm_h[n_nzeros] = 1.0 / norm_h[n_nzeros]
    norm_h = np.array(norm_h).T[0]

    csr_scale_rows(hyp_data.shape[0],
                   hyp_data.shape[1],
                   hyp_data.indptr,
                   hyp_data.indices,
                   hyp_data.data, norm_h)

    #calculate the entropy for a row
    #entropy = np.apply_along_axis( entropy_step, axis=1, arr=hyp_data )
    entropy =[]
    c=0
    for i in range(0,hyp_data.shape[0]):
        c+=1
        if c % 100000 == 0:
            print c
        x = hyp_data.getrow(i)
        entropy.append(entropy_step(x))

    print "entropy"
    #number of link for a row, needed for normalization fo the
    norm_h = hyp_structural.sum(axis=1)
    #print norm_h
    normalized_entropy = []
    for i, x in enumerate(entropy):
        if i % 100000 == 0:
            print i

        if math.log(norm_h[i][0])==0:
            normalized_entropy.append(0)
        else:
            e = x/math.log(norm_h[i][0])
            normalized_entropy.append(e)

    print "normed entropy"
    write_pickle('output/normalized_entropy.obj',normalized_entropy)





def gini(row_normed):
    print "gini"
    print row_normed
    transition_matrix = pickle.load( open( SSD_HOME+"pickle/transition_matrix", "rb" ) )
    print "loaded transitions"
    graph = pickle.load( open( SSD_HOME+"pickle/graph", "rb" ) )
    print "loaded graph"
    values = pickle.load( open( SSD_HOME+"pickle/values", "rb" ) )


    vocab = pickle.load( open( SSD_HOME+"pickle/vocab", "rb" ) )
    print "loaded vocab"

    state_count = len(vocab)
    states = vocab.keys()
    shape = (state_count, state_count)



    # structural hypothesises
    hyp_structural = csr_matrix((values, (graph[0], graph[1])),
                                shape=shape, dtype=np.float)



    transitions = csr_matrix((transition_matrix[2], (transition_matrix[0], transition_matrix[1])),
                             shape=shape)

    del transition_matrix

    #delete all zero rows from all  see  http://stackoverflow.com/questions/31188141/scipy-sparse-matrix-remove-the-rows-whose-all-elements-are-zero
    print transitions.shape
    nonzero_row_indice, _ = transitions.nonzero()
    unique_nonzero_indice = np.unique(nonzero_row_indice)
    transitions = transitions[unique_nonzero_indice]
    print transitions.shape

    hyp_data = csr_matrix(transitions, copy=True)
    print hyp_data.shape

    hyp_structural = hyp_structural[unique_nonzero_indice]
    if row_normed:
        #norm the data
        norm_h = hyp_data.sum(axis=1)
        n_nzeros = np.where(norm_h > 0)
        norm_h[n_nzeros] = 1.0 / norm_h[n_nzeros]
        norm_h = np.array(norm_h).T[0]

        csr_scale_rows(hyp_data.shape[0],
                       hyp_data.shape[1],
                       hyp_data.indptr,
                       hyp_data.indices,
                       hyp_data.data, norm_h)

    #calculate the gini for a row

    gini =[]
    c=0
    for i in range(0,hyp_data.shape[0]):
        c+=1
        if c % 10000 == 0:
            print c
        counts = hyp_data.getrow(i).toarray()[0]
        links = hyp_structural.getrow(i).toarray()[0]
        indices_of_links =  links > 0
        gini_data = counts[indices_of_links]
        gini.append(gini_step(gini_data))

    print "gini"
    if row_normed:
        write_pickle('output/gini_row_normed.obj',gini)
    else:
        write_pickle('output/gini.obj',gini)


def gini_random_rows(row_normed):
    print "gini"
    print row_normed
    transition_matrix = pickle.load( open( SSD_HOME+"pickle/transition_matrix", "rb" ) )
    print "loaded transitions"
    graph = pickle.load( open( SSD_HOME+"pickle/graph", "rb" ) )
    print "loaded graph"
    values = pickle.load( open( SSD_HOME+"pickle/values", "rb" ) )


    vocab = pickle.load( open( SSD_HOME+"pickle/vocab", "rb" ) )
    print "loaded vocab"

    state_count = len(vocab)
    states = vocab.keys()
    shape = (state_count, state_count)



    # structural hypothesises
    hyp_structural = csr_matrix((values, (graph[0], graph[1])),
                                shape=shape, dtype=np.float)



    transitions = csr_matrix((transition_matrix[2], (transition_matrix[0], transition_matrix[1])),
                             shape=shape)

    del transition_matrix

    #delete all zero rows from all  see  http://stackoverflow.com/questions/31188141/scipy-sparse-matrix-remove-the-rows-whose-all-elements-are-zero
    print transitions.shape
    nonzero_row_indice, _ = transitions.nonzero()
    unique_nonzero_indice = np.unique(nonzero_row_indice)
    transitions = transitions[unique_nonzero_indice]
    print transitions.shape

    hyp_data = csr_matrix(transitions, copy=True)
    print hyp_data.shape

    hyp_structural = hyp_structural[unique_nonzero_indice]
    if row_normed:
        #norm the data
        norm_h = hyp_data.sum(axis=1)
        n_nzeros = np.where(norm_h > 0)
        norm_h[n_nzeros] = 1.0 / norm_h[n_nzeros]
        norm_h = np.array(norm_h).T[0]

        csr_scale_rows(hyp_data.shape[0],
                       hyp_data.shape[1],
                       hyp_data.indptr,
                       hyp_data.indices,
                       hyp_data.data, norm_h)

    #calculate the gini for a row

    gini =[]
    c=0
    #for i in range(0,hyp_data.shape[0]):

    import random
    for i in random.sample(range(0,hyp_data.shape[0]), 10000):
        c+=1
        if c % 1000 == 0:
            print c
        counts = hyp_data.getrow(i).toarray()[0]
        links = hyp_structural.getrow(i).toarray()[0]
        indices_of_links =  links > 0
        gini_data = counts[indices_of_links]
        gini.append(gini_step(gini_data))

    print "gini"
    if row_normed:
        write_pickle('output/gini_random_rows_row_normed.obj',gini)
    else:
        write_pickle('output/gini_random_rows.obj',gini)



def gini_step(list_of_values):
    #list_of_values=list_of_values.todense()
    #list_of_values=list_of_values.toarray()
    #print list_of_values[0]
    #print len(list_of_values)
    #print list_of_values
    sorted_list = sorted(list_of_values)
    height, area = 0, 0
    for value in sorted_list:
        height += value
        area += height - value / 2.
    fair_area = height * len(list_of_values) / 2.
    return (fair_area - area) / fair_area


def entropy_step(x):
    sum = 0
    for i in x.data:
        sum-= i*math.log(i)
    return sum

def plot_entropy_ccdf():
    entropy = read_pickle('output/normalized_entropy.obj')


    fig = plt.figure()
    ax = fig.add_subplot(111)


    powerlaw.plot_ccdf(entropy, ax, label='normalized entropy')
    # further plotting
    ax.set_xlabel("Normalized entropy e")
    ax.set_ylabel("Pr(X>=e)")
    plt.legend(fancybox=True, loc='lower left', ncol=1,prop={'size':5})

    plt.tight_layout()
    plt.savefig('output/normalized_entropy_distribution_ccdf.pdf')

    fig = plt.figure()
    ax = fig.add_subplot(111)

    powerlaw.plot_cdf(entropy, ax, label='normalized entropy',color='r')
    # further plotting
    ax.set_xlabel("Normalized entropy e")
    ax.set_ylabel("Pr(X<=e)")
    plt.legend(fancybox=True, loc='lower left', ncol=1,prop={'size':5})

    plt.tight_layout()
    plt.savefig('output/normalized_entropy_distribution_cdf.pdf')


def plot_entropy_distribution():
    fig = plt.figure()
    ax = fig.add_subplot(111)

    entropy = read_pickle('output/normalized_entropy.obj')

    hist, bin_edges = np.histogram(entropy, bins=10000)
    print hist, bin_edges

    #ax.set_yscale('log')
    #ax.set_xscale('log')
    ax.plot(bin_edges[:-1], hist, marker='o', markersize=3, markeredgecolor='none', color='#D65F5F')

    #ax.set_ylim([10**0, 10**6])
    #ax.set_xlim([10**0, 10**6])
    ax.set_xlabel('Entropy')
    ax.set_ylabel('Frequency')

    fig.tight_layout()
    fig.savefig( 'output/normalized_entropy_distribution.pdf', bbox_inches='tight')


def plot_entropy_boxplot():
    fig = plt.figure()
    ax = fig.add_subplot(111)

    entropy = read_pickle('output/normalized_entropy.obj')
    ax.boxplot(entropy)

    ax.set_ylim([-1,1])
    #ax.set_xlim([10**0, 10**6])
    ax.set_xlabel('Entropy')
    ax.set_ylabel('Frequency')

    fig.tight_layout()
    fig.savefig( 'output/normalized_entropy_boxplot.pdf', bbox_inches='tight')



def plot_entropy_hist():
    fig = plt.figure()
    ax = fig.add_subplot(111)

    entropy = read_pickle('output/normalized_entropy.obj')
    number_of_zeros = [1 if item is 0 else 0 for item in entropy]

    print len(number_of_zeros)
    print sum(number_of_zeros)
    n, bins, patches = ax.hist(entropy, 50)
    ax.plot(bins, )
    #ax.set_ylim([-1,1])
    ax.set_xlim([0,1])
    ax.set_yscale('log')
    ax.set_xlabel('Normalized entropy')
    ax.set_ylabel('Frequency (log)')

    fig.tight_layout()
    fig.savefig( 'output/normalized_entropy_hist.pdf', bbox_inches='tight')


def plot_gini_hist(name):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    gini = read_pickle('output/'+name+'.obj')
    number_of_zeros = [1 if item is 0 else 0 for item in gini]

    print len(number_of_zeros)
    print sum(number_of_zeros)
    #n, bins, patches = ax.hist(gini, 50,  color='#D65F5F', edgecolor='none')
    n, bins, patches = ax.hist(gini, 50,  edgecolor='none')
    ax.plot(bins)
    #ax.set_ylim([-1,1])
    ax.set_xlim([0,1])
    #ax.set_yscale('log')
    ax.set_xlabel('Gini coefficient')
    ax.set_ylabel('Frequency')

    fig.tight_layout()
    fig.savefig( 'output/'+name+'.pdf', bbox_inches='tight')




if __name__ == '__main__':
    #normalized_entropy()
    #plot_entropy_ccdf()
    #plot_entropy_distribution()
    #plot_entropy_boxplot()
    #plot_entropy_hist()

    #Parallel(n_jobs=2, backend="multiprocessing")(delayed(gini)(row_normed) for row_normed in
    #                                             [True,False])


    #gini_random_rows(False)
    #gini_random_rows(True)

    plot_gini_hist('gini')
    plot_gini_hist('gini_random_rows')
    plot_gini_hist('gini_random_rows_row_normed')
