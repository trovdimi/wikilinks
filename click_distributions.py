import scipy.stats as stats
import matplotlib.pyplot as plt
import MySQLdb
from wsd.database import MySQLDatabase
import matplotlib.cm as cm
from matplotlib.colors import LogNorm, Normalize, BoundaryNorm, PowerNorm
from conf import *
from collections import defaultdict
import cPickle as pickle
import pandas as pd
import numpy as np
import pylab
from scipy.stats.stats import pearsonr,spearmanr,kendalltau
import math
import cPickle as pickle
import powerlaw
import matplotlib.mlab as mlab
import random
from collections import Counter
from operator import itemgetter


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



def plot_counts_category_distributions_ccdf():
    category_distributions = read_pickle(HOME+'output/category_counts_distribution.obj')

    for  i in category_distributions.values():
        print len(i)

    colors= {'lead':'r','infobox':'b', 'body':'g',  'left-body':'m','navbox':'c', 'counts':'k'}


    fig = plt.figure()
    ax = fig.add_subplot(111)

    for category in ['lead', 'infobox', 'body', 'left-body', 'navbox', 'counts']:

        data = category_distributions[category]
        data = [x[0] for x in data]
        powerlaw.plot_ccdf(data, ax, label=category,color=colors[category])
    # further plotting
    ax.set_xlabel("Number of clicks n")
    ax.set_ylabel("Pr(X>=n)")
    plt.legend(fancybox=True, loc=3, ncol=2, prop={'size':4})
    #leg = plt.gca().get_legend()
    #ltext  = leg.get_texts()  # all the text.Text instance in the legend
    #llines = leg.get_lines()
    #plt.setp(ltext, fontsize='small')    # the legend text fontsize
    #plt.setp(llines, linewidth=1)
    plt.tight_layout()
    plt.savefig('output/category_counts_distributions.pdf')

    data = category_distributions['counts']
    data = [int(x[0]) for x in data]

    hist, bin_edges = np.histogram(data, 100, density=True)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot( bin_edges[:-1],hist, marker='o')
    ax.set_xlabel('#Counts')
    ax.set_ylabel('#Pages')
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.legend(fancybox=True, loc=3,  prop={'size':4})
    plt.tight_layout()
    plt.savefig('output/counts_distribution.pdf')


def plot_aggregated_counts_distributions_ccdf():
    #agg_distributions = read_pickle(HOME+'output/aggregated_counts_distribution.obj')

    #for  i in agg_distributions.values():
    #    print len(i)

    colors= {'source_article':'r','target_article':'b'}
    labels = {'source_article': 'source article', 'target_article':'target article'}
    fig = plt.figure()
    ax = fig.add_subplot(111)

    #for category in ['source_article', 'target_article']:
    #    data = agg_distributions[category]
    #    data = [int(x[0]) for x in data]
    #    powerlaw.plot_ccdf(data, ax, label=labels[category],color=colors[category])

    category_distributions = read_pickle(HOME+'output/category_counts_distribution.obj')
    data = category_distributions['counts']
    data = [int(x[0]) for x in data]
    #to consider the edges that have zero transitions we substract the number transitions from the number of edges in wikipeida
    number_of_edges = 339463340
    listofzeros = [0] * (number_of_edges - len(data))
    print len(data)
    print len(listofzeros)
    zeros = np.zeros((number_of_edges - len(data)))
    data = np.append(zeros, data)
    #data = data.extend(listofzeros)
    print data
    #hist, bin_edges = np.histogram(data, bins=100, normed=True)
    #ones = np.ones(100)
    #ccdf = ones - np.cumsum(data)

    #cdf = np.cumsum(hist)
    #print cdf
    #print ccdf
    bins, CDF = powerlaw.cdf(data, survival=True)
    plt.plot(bins, CDF)
    plt.xscale('symlog')

    #powerlaw.plot_cdf(data, ax, label='transitions', color='r')
    # further plotting
    #ax.set_xlabel(r'Number of transitions $n$')
    #ax.set_ylabel(r'$P(X \geq n)$')
    plt.legend(fancybox=True, loc='lower left', ncol=1, prop={'size':5})

    #leg = plt.gca().get_legend()
    #ltext  = leg.get_texts()  # all the text.Text instance in the legend
    #plt.setp(ltext, fontsize='small')    # the legend text fontsize
    plt.tight_layout()
    plt.savefig('output/agg_counts_distributions.pdf', bbox_inches='tight')


    # data = agg_distributions['target_article']
    # data = [int(x[0]) for x in data]
    #
    # hist, bin_edges = np.histogram(data, 100, density=True)
    # print len(hist)
    # print len(hist[:-1])
    # print len(bin_edges)
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.plot(bin_edges[:-1],hist,  marker='o')
    # ax.set_xlabel('#Counts')
    # ax.set_ylabel('#Pages')
    # ax.set_yscale('log')
    # ax.set_xscale('log')
    # plt.legend(fancybox=True, loc=3,  prop={'size':4})
    # plt.tight_layout()
    # plt.savefig('output/agg_counts_distributions_target.pdf')
    #
    # data = agg_distributions['source_article']
    # data = [int(x[0]) for x in data]
    #
    # hist, bin_edges = np.histogram(data, 100, density=True)
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.plot( bin_edges[:-1],hist, marker='o')
    # ax.set_xlabel('#Counts')
    # ax.set_ylabel('#Pages')
    # ax.set_yscale('log')
    # ax.set_xscale('log')
    # plt.legend(fancybox=True, loc=3,  prop={'size':4})
    # plt.tight_layout()
    # plt.savefig('output/agg_counts_distributions_source.pdf')


def plot_counts_frequency():

    fig = plt.figure()
    ax = fig.add_subplot(111)


    category_distributions = read_pickle(HOME+'output/category_counts_distribution.obj')
    data = category_distributions['counts']
    data = [int(x[0]) for x in data]
    #to consider the edges that have zero transitions we substract the number transitions from the number of edges in wikipeida
    #number_of_edges = 339463340
    #zeros = np.zeros((number_of_edges - len(data)))
    #data = np.append(zeros, data)
    #bins = [0,11]
    #bins.extend(np.linspace(100,10000))
    #data = data.extend(listofzeros)
    #print data
    hist, bin_edges = np.histogram(data, bins=10000)
    #print len(hist)
    #print len(bin_edges)
    print hist, bin_edges

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.plot(bin_edges[:-1], hist, marker='o', markersize=3, markeredgecolor='none', color='#D65F5F')

    #ax.set_ylim([10**0, 10**6])
    #ax.set_xlim([10**0, 10**6])
    ax.set_xlabel('Number of transitions')
    ax.set_ylabel('Frequency')

    fig.tight_layout()
    fig.savefig( 'output/agg_counts_distributions.pdf', bbox_inches='tight')


def pickle_category_counts_distribution():
    results =  {}
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    db_worker_view = db.get_work_view()
    cursor = db_worker_view._cursor
    for category in ['lead', 'infobox', 'body', 'left-body', 'navbox']:
        try:
            cursor.execute('select counts from link_features where counts is not null and visual_region=%s;', (category,))
            result = cursor.fetchall()
            results[category] = result
        except MySQLdb.Error, e:
            print e

    try:
        cursor.execute('select counts from clickstream_derived_internal_links;')
        result = cursor.fetchall()
        results['counts'] = result
    except MySQLdb.Error, e:
        print e

    write_pickle(HOME+'output/category_counts_distribution.obj', results)


def pickle_aggregated_counts_distribution():

    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    db_worker_view = db.get_work_view()
    cursor = db_worker_view._cursor
    results = {}
    try:
        cursor.execute('select sum(counts) from clickstream_derived_internal_links group by prev_id;')
        result = cursor.fetchall()
        results['source_article']=result
    except MySQLdb.Error, e:
        print e

    try:
        cursor.execute('select sum(counts) from clickstream_derived_internal_links group by curr_id;')
        result = cursor.fetchall()
        results['target_article']=result
    except MySQLdb.Error, e:
        print e

    write_pickle(HOME+'output/aggregated_counts_distribution.obj', results)

def trim_to_range(data, xmin=None, xmax=None, **kwargs):
    """
    Removes elements of the data that are above xmin or below xmax (if present)
    """
    from numpy import asarray
    data = asarray(data)
    if xmin:
        data = data[data>=xmin]
    if xmax:
        data = data[data<=xmax]
    return data

if __name__ == '__main__':
    #pickle_category_counts_distribution()
    #pickle_aggregated_counts_distribution()
    #plot_counts_category_distributions_ccdf()
    #plot_aggregated_counts_distributions_ccdf()
    plot_counts_frequency()