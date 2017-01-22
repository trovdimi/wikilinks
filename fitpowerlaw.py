from __future__ import division


import numpy as np
from graph_tool.all import *
from matplotlib import pyplot as plt
import pickle
import powerlaw


from matplotlib import style
style.use('acm-3col')

import pylab
params = {
    'font.family' : 'serif',
    'font.serif' : ['Times New Roman'],
    'font.size' : 15
}
pylab.rcParams.update(params)




def powerLawExponent(net_name, net):
    # degree_dist={}
    # for v in net.vertices():
    #     degree_dist[v] = v.out_degree() + v.in_degree()
    # results = powerlaw.Fit(degree_dist.values(), discrete=True, xmin=1)
    # print 'power law for network: ', net_name
    # print 'alpha: ', results.power_law.alpha
    # print 'xmin: ', results.power_law.xmin
    # print 'D', results.D
    # print 'distribution camparison power law - exponential: ', results.distribution_compare('power_law', 'exponential', normalized_ratio=True)
    # print 'distribution camparison power law - lognormal: ', results.distribution_compare('power_law', 'lognormal', normalized_ratio=True)
    # print 'distribution camparison power law - truncated: ', results.distribution_compare('power_law', 'truncated_power_law', normalized_ratio=True)
    #
    # results = powerlaw.Fit(degree_dist.values(), discrete=True)
    # print 'power law for network: ', net_name
    # print 'alpha: ', results.power_law.alpha
    # print 'xmin: ', results.power_law.xmin
    # print 'D', results.D
    # print 'distribution camparison power law - exponential: ', results.distribution_compare('power_law', 'exponential', normalized_ratio=True)
    # print 'distribution camparison power law - lognormal: ', results.distribution_compare('power_law', 'lognormal', normalized_ratio=True)
    # print 'distribution camparison power law - truncated: ', results.distribution_compare('power_law', 'truncated_power_law', normalized_ratio=True)


    in_degree_dist={}
    for v in net.vertices():
        in_degree_dist[v] = v.in_degree()
    results = powerlaw.Fit(in_degree_dist.values(), discrete=True, xmin=1)
    print 'power law for network: ', net_name
    print 'alpha: ', results.power_law.alpha
    print 'xmin: ', results.power_law.xmin
    print 'D', results.D
    print 'distribution camparison power law - exponential: ', results.distribution_compare('power_law', 'exponential', normalized_ratio=True)
    print 'distribution camparison power law - lognormal: ', results.distribution_compare('power_law', 'lognormal', normalized_ratio=True)
    print 'distribution camparison power law - truncated: ', results.distribution_compare('power_law', 'truncated_power_law', normalized_ratio=True)
    print 'distribution camparison lognormal - truncated: ', results.distribution_compare('lognormal', 'truncated_power_law', normalized_ratio=True)

    results = powerlaw.Fit(in_degree_dist.values(), discrete=True)
    print 'power law for network: ', net_name
    print 'alpha: ', results.power_law.alpha
    print 'xmin: ', results.power_law.xmin
    print 'D', results.D
    print 'distribution camparison power law - exponential: ', results.distribution_compare('power_law', 'exponential', normalized_ratio=True)
    print 'distribution camparison power law - lognormal: ', results.distribution_compare('power_law', 'lognormal', normalized_ratio=True)
    print 'distribution camparison power law - truncated: ', results.distribution_compare('power_law', 'truncated_power_law', normalized_ratio=True)
    print 'distribution camparison lognormal - truncated: ', results.distribution_compare('lognormal', 'truncated_power_law', normalized_ratio=True)

    out_degree_dist={}
    for v in net.vertices():
        out_degree_dist[v] = v.out_degree()
    results = powerlaw.Fit(out_degree_dist.values(), discrete=True, xmin=1)
    print 'power law for network: ', net_name
    print 'alpha: ', results.power_law.alpha
    print 'xmin: ', results.power_law.xmin
    print 'D', results.D
    print 'distribution camparison power law - exponential: ', results.distribution_compare('power_law', 'exponential', normalized_ratio=True)
    print 'distribution camparison power law - lognormal: ', results.distribution_compare('power_law', 'lognormal', normalized_ratio=True)
    print 'distribution camparison power law - truncated: ', results.distribution_compare('power_law', 'truncated_power_law', normalized_ratio=True)
    print 'distribution camparison lognormal - truncated: ', results.distribution_compare('lognormal', 'truncated_power_law', normalized_ratio=True)

    results = powerlaw.Fit(out_degree_dist.values(), discrete=True)
    print 'power law for network: ', net_name
    print 'alpha: ', results.power_law.alpha
    print 'xmin: ', results.power_law.xmin
    print 'D', results.D
    print 'distribution camparison power law - exponential: ', results.distribution_compare('power_law', 'exponential', normalized_ratio=True)
    print 'distribution camparison power law - lognormal: ', results.distribution_compare('power_law', 'lognormal', normalized_ratio=True)
    print 'distribution camparison power law - truncated: ', results.distribution_compare('power_law', 'truncated_power_law', normalized_ratio=True)
    print 'distribution camparison lognormal - truncated: ', results.distribution_compare('lognormal', 'truncated_power_law', normalized_ratio=True)

def meanClustering(net_name, net):
    clust = network.vertex_properties["local_clust"]
    print 'clustering mean for network: ', net_name
    print np.mean(clust.get_array())
    return

def giniCoeff(net_name, net):
    # requires all values in x to be zero or positive numbers,
    # otherwise results are undefined
    degree_dist={}
    for v in net.vertices():
        degree_dist[v] = v.out_degree() + v.in_degree()
    x = np.asarray(degree_dist.values())
    n = len(x)
    s = x.sum()
    r = np.argsort(np.argsort(-x)) # calculates zero-based ranks
    gini = 1 - (2.0 * (r*x).sum() + s)/(n*s)
    print 'gini', str(gini)

    degree_dist={}
    for v in net.vertices():
        degree_dist[v] =v.in_degree()
    x = np.asarray(degree_dist.values())
    n = len(x)
    s = x.sum()
    r = np.argsort(np.argsort(-x)) # calculates zero-based ranks
    gini = 1 - (2.0 * (r*x).sum() + s)/(n*s)
    print "in"
    print 'gini', str(gini)

    degree_dist={}
    for v in net.vertices():
        degree_dist[v] =v.out_degree()
    x = np.asarray(degree_dist.values())
    n = len(x)
    s = x.sum()
    r = np.argsort(np.argsort(-x)) # calculates zero-based ranks
    gini = 1 - (2.0 * (r*x).sum() + s)/(n*s)
    print "out"
    print 'gini', str(gini)
    return gini

if __name__ == '__main__':
    # wikipedia  graph  structural statistics
    print 'before load'
    network = load_graph("output/wikipedianetwork.xml.gz")
    print 'after load'

    powerLawExponent("wikipedia", network)
    #giniCoeff("wikipedia", network)
    #meanClustering("wikipeida", network)

