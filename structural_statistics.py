from __future__ import division


import numpy as np
from graph_tool.all import *
from matplotlib import pyplot as plt
import pickle
import powerlaw
import fitpowerlaw as fp
from wsd.database import MySQLDatabase
from graph_tool.all import *
from conf import *


from matplotlib import style
style.use('acm-3col-bmh')

import pylab
params = {
    'font.family' : 'serif',
    'font.serif' : ['Times New Roman'],
    'font.size' : 7
}
pylab.rcParams.update(params)


def plot_stats():
    # wikipedia  graph  structural statistics
    print 'before load'
    network = load_graph("output/wikipedianetwork.xml.gz")
    print 'after load'
    out_hist = vertex_hist(network, "out")
    plt.gca().set_yscale('log')
    plt.gca().set_xscale('log')
    plt.plot(out_hist[1][:-1], out_hist[0], marker='o')
    plt.xlabel('Out-degree')
    plt.ylabel('Frequency')
    plt.gca().set_ylim([1, 10**6])
    #plt.title('Out-degree Distribution')
    plt.tight_layout()
    plt.savefig('output/wikipedia-out-deg-dist.pdf')

    plt.clf()

    in_hist = vertex_hist(network, "in")
    plt.gca().set_yscale('log')
    plt.gca().set_xscale('log')
    plt.plot(in_hist[1][:-1], in_hist[0], marker='o')
    plt.xlabel('In-degree')
    plt.ylabel('Frequency')
    plt.gca().set_ylim([1, 10**6])
    #plt.title('In-degree Distribution')
    plt.tight_layout()
    plt.savefig('output/wikipedia-in-deg-dist.pdf')

    plt.clf()

    total_hist = vertex_hist(network, "total")

    plt.gca().set_yscale('log')
    plt.gca().set_xscale('log')
    plt.plot(total_hist[1][:-1], total_hist[0], marker='o')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.gca().set_ylim([1, 10**6])
    #plt.title('Degree Distribution')
    plt.tight_layout()
    plt.savefig('output/wikipedia-deg-dist.pdf')

    plt.clf()

    clust = network.vertex_properties["local_clust"]
    #clust = local_clustering(network, undirected=False)

    #hist, bin_edges = np.histogram(clust.get_array(), 100, density=True)
    #cdf = np.cumsum(hist)

    #plt.plot(bin_edges[1:], cdf, marker='o')
    #plt.xlabel('Local Clustering Coefficient C')
    #plt.ylabel('P(x<=C)')
    #plt.title('Clustering Coefficient Distribution')
    #plt.savefig('output/wikipedia-clust-cdf.pdf')

    fig, ax = plt.subplots()
    powerlaw.plot_cdf(clust.get_array(), ax)
    #ax.set_title('Clustering Coefficient Distribution')
    ax.set_xlabel('Local Clustering Coefficient $C')
    ax.set_ylabel('P(x<=C)')
    ax.set_ylim([0, 1])
    fig.tight_layout()
    fig.savefig('output/wikipedia-clust-cdf.pdf')

    plt.clf()


    fig, ax = plt.subplots()
    powerlaw.plot_ccdf(clust.get_array(), ax)
    #ax.set_title('Clustering Coefficient Distribution')
    ax.set_xlabel('Local Clustering Coefficient C')
    ax.set_ylabel('P(x>=C)')
    ax.set_ylim([10**-4, 10**-0.5])
    fig.tight_layout()
    fig.savefig('output/wikipedia-clust-ccdf.pdf')

    plt.clf()

    prank = network.vertex_properties["page_rank"]

    #hist, bin_edges = np.histogram(prank.get_array(), 100, density=True)
    #cdf = np.cumsum(hist)

    #plt.plot(bin_edges[1:], cdf, marker='o')
    #plt.xlabel('Page rank Pr')
    #plt.ylabel('P(x<=Pr)')
    #plt.title('Page rank Distribution')
    #plt.savefig('output/wikipedia-prank-cdf.pdf')
    fig, ax = plt.subplots()
    powerlaw.plot_cdf(prank.get_array(), ax)
    #ax.set_title('Page Rank Distribution')
    ax.set_xlabel('Page rank Pr')
    ax.set_ylabel('P(x<=Pr)')
    ax.set_ylim([0, 1])
    fig.tight_layout()
    fig.savefig('output/wikipedia-prank-cdf.pdf')
    plt.clf()

    fig, ax = plt.subplots()
    powerlaw.plot_ccdf(prank.get_array(), ax)
    #ax.set_title('Page Rank Distribution')
    ax.set_xlabel('Page rank Pr')
    ax.set_ylabel('P(x>=Pr)')
    fig.tight_layout()
    fig.savefig('output/wikipedia-prank-ccdf.pdf')

    plt.clf()

    kcore = network.vertex_properties["kcore"]

    #hist, bin_edges = np.histogram(kcore.get_array(), 100, density=True)
    #cdf = np.cumsum(hist)
    #plt.plot(bin_edges[1:], cdf, marker='o')
    #plt.xlabel('Kcore kC')
    #plt.ylabel('P(x<=kC)')
    #plt.title('K-Core Distribution')
    #plt.savefig('output/wikipedia-kcore-cdf.pdf')

    fig, ax = plt.subplots()
    powerlaw.plot_cdf(kcore.get_array(), ax)
    #ax.set_title('K-Core Distribution')
    ax.set_xlabel('k-Core kC')
    ax.set_ylabel('P(x<=kC)')
    ax.set_ylim([0, 1])
    fig.tight_layout()
    fig.savefig('output/wikipedia-kcore-cdf.pdf')

    plt.clf()

    fig, ax = plt.subplots()
    powerlaw.plot_ccdf(kcore.get_array(), ax)
    #ax.set_title('K-Core Distribution')
    ax.set_xlabel('k-Core kC')
    ax.set_ylabel('P(x>=kC)')
    fig.tight_layout()
    fig.savefig('output/wikipedia-kcore-ccdf.pdf')

    plt.clf()



    eigenvector_centr = network.vertex_properties["eigenvector_centr"]

    #hist, bin_edges = np.histogram(eigenvector_centr.get_array(), 100, density=True)
    #cdf = np.cumsum(hist)
    #plt.plot(bin_edges[1:], cdf, marker='o')
    #plt.xlabel('Eigenvector Centrality E')
    #plt.ylabel('P(x<=E)')
    #plt.title('Eigenvector Centrality Distribution')
    #plt.savefig('output/wikipedia-eigenvcentr-cdf.pdf')

    fig, ax = plt.subplots()
    powerlaw.plot_cdf(eigenvector_centr.get_array(), ax)
    #ax.set_title('Eigenvector Centrality E')
    ax.set_xlabel('Eigenvector Centrality E')
    ax.set_ylabel('P(x<=E)')
    ax.set_ylim([0, 1])
    fig.tight_layout()
    fig.savefig('output/wikipedia-eigenvcentr-cdf.pdf')

    plt.clf()

    fig, ax = plt.subplots()
    powerlaw.plot_ccdf(eigenvector_centr.get_array(), ax)
    #ax.set_title('Eigenvector Centrality E')
    ax.set_xlabel('Eigenvector Centrality E')
    ax.set_ylabel('P(x>=E)')
    fig.tight_layout()
    fig.savefig('output/wikipedia-eigenvcentr-ccdf.pdf')

    plt.clf()


    colors= {'local_clust':'r','eigenvector_centr':'b', 'page_rank': 'g', 'kcore':'m', 'hub': 'c', 'authority':'k'}
    labels = {'local_clust': 'clust.', 'eigenvector_centr':'eigen. centr.','page_rank': 'page rank', 'kcore': 'kcore', 'hub':'hub', 'authority':'authority'}
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for f in ['local_clust','page_rank', 'hub', 'authority', 'kcore']:
        feature = network.vertex_properties[f]
        powerlaw.plot_cdf(feature.get_array(), ax, label=labels[f],color=colors[f])
    ax.set_xlabel('Feature $f$')
    ax.set_ylabel('$P(X>=f)$')
    ax.set_ylim([0, 1])
    plt.legend(fancybox=True, loc=3, ncol=2, prop={'size':4})
    plt.tight_layout()
    plt.savefig('output/wikipedia-features-cdf.pdf')

    plt.clf()
    colors= {'local_clust':'r','eigenvector_centr':'b', 'page_rank': 'g', 'kcore':'m', 'hub': 'c', 'authority':'k'}
    labels = {'local_clust': 'clust.', 'eigenvector_centr':'eigen. centr.','page_rank': 'page rank', 'kcore': 'kcore', 'hub':'hub', 'authority':'authority'}
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for f in ['local_clust','eigenvector_centr','page_rank', 'hub', 'authority', 'kcore']:
        feature = network.vertex_properties[f]
        powerlaw.plot_cdf(feature.get_array(), ax, label=labels[f],color=colors[f])
    ax.set_xlabel('Feature $f$')
    ax.set_ylabel('$P(X<=f)$')
    plt.legend(fancybox=True, loc=3, ncol=2, prop={'size':4})
    plt.tight_layout()
    plt.savefig('output/wikipedia-features-ccdf.pdf')


    plt.clf()





    # wikipedia transitions  graph  structural statistics
    print 'before load'
    network_transitions = load_graph("output/transitionsnetwork.xml.gz")
    print 'after load'

    out_hist = vertex_hist(network_transitions, "out")
    plt.gca().set_yscale('log')
    plt.gca().set_xscale('log')
    plt.plot(out_hist[1][:-1], out_hist[0], marker='o')
    plt.xlabel('Out-degree')
    plt.ylabel('Frequency')
    plt.gca().set_ylim([1, 10**6])
    #plt.title('Out-degree Distribution')
    plt.savefig('output/wikipedia-transitions-out-deg-dist.pdf')

    plt.clf()

    in_hist = vertex_hist(network_transitions, "in")
    plt.gca().set_yscale('log')
    plt.gca().set_xscale('log')
    plt.plot(in_hist[1][:-1], in_hist[0], marker='o')
    plt.xlabel('In-degree')
    plt.ylabel('Frequency')
    #plt.title('In-degree Distribution')
    plt.gca().set_ylim([1, 10**6])
    plt.savefig('output/wikipedia-transitions-in-deg-dist.pdf')

    plt.clf()

    total_hist = vertex_hist(network_transitions, "total")

    plt.gca().set_yscale('log')
    plt.gca().set_xscale('log')
    plt.plot(total_hist[1][:-1], total_hist[0], marker='o')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    #plt.title('Degree Distribution')
    plt.gca().set_ylim([1, 10**6])
    plt.savefig('output/wikipedia-transitions-deg-dist.pdf')

    plt.clf()

    #clust = local_clustering(network_transitions, undirected=False)
    clust = network_transitions.vertex_properties["local_clust"]

    #hist, bin_edges = np.histogram(clust.get_array(), 100, density=True)
    #cdf = np.cumsum(hist)
    #plt.plot(bin_edges[1:], cdf, marker='o')
    #plt.xlabel('Local Clustering Coefficient C')
    #plt.ylabel('P(x<=C)')
    #plt.title('Clustering Coefficient Distribution')
    #plt.savefig('output/wikipedia-transitions-clust-cdf.pdf')

    fig, ax = plt.subplots()
    powerlaw.plot_cdf(clust.get_array(), ax)
    #ax.set_title('Clustering Coefficient Distribution')
    ax.set_xlabel('Local Clustering Coefficient C')
    ax.set_ylabel('P(x<=C)')
    fig.savefig('output/wikipedia-transitions-clust-cdf.pdf')

    plt.clf()

    fig, ax = plt.subplots()
    powerlaw.plot_ccdf(clust.get_array(), ax)
    ax.set_title('Clustering Coefficient Distribution')
    ax.set_xlabel('Local Clustering Coefficient C')
    ax.set_ylabel('P(x>=C)')
    fig.savefig('output/wikipedia-transitions-clust-ccdf.pdf')

    plt.clf()

    prank = network_transitions.vertex_properties["page_rank"]

    #hist, bin_edges = np.histogram(prank.get_array(), 100, density=True)
    #cdf = np.cumsum(hist)
    #plt.plot(bin_edges[1:], cdf, marker='o')
    #plt.xlabel('Page rank Pr')
    #plt.ylabel('P(x<=Pr)')
    #plt.title('Page rank Distribution')
    #plt.savefig('output/wikipedia-transitions-prank-cdf.pdf')

    fig, ax = plt.subplots()
    powerlaw.plot_cdf(prank.get_array(), ax)
    #ax.set_title('Page Rank Distribution')
    ax.set_xlabel('Page rank Pr')
    ax.set_ylabel('P(x<=Pr)')
    fig.savefig('output/wikipedia-transitions-prank-cdf.pdf')

    plt.clf()

    fig, ax = plt.subplots()
    powerlaw.plot_ccdf(prank.get_array(), ax)
    #ax.set_title('Page Rank Distribution')
    ax.set_xlabel('Page rank Pr')
    ax.set_ylabel('P(x>=Pr)')
    fig.savefig('output/wikipedia-transitions-prank-ccdf.pdf')

    plt.clf()

    kcore = network_transitions.vertex_properties["kcore"]

    #hist, bin_edges = np.histogram(kcore.get_array(), 100, density=True)
    #cdf = np.cumsum(hist)

    #plt.plot(bin_edges[1:], cdf, marker='o')
    #plt.xlabel('Kcore kC')
    #plt.ylabel('P(x<=kC)')
    #plt.title('K-Core Distribution')
    #plt.savefig('output/wikipedia-transitions-kcore-cdf.pdf')

    fig, ax = plt.subplots()
    powerlaw.plot_cdf(kcore.get_array(), ax)
    #ax.set_title('K-Core Distribution')
    ax.set_xlabel('k-Core kC')
    ax.set_ylabel('P(x<=kC)')
    fig.savefig('output/wikipedia-transitions-kcore-cdf.pdf')

    plt.clf()

    fig, ax = plt.subplots()
    powerlaw.plot_ccdf(kcore.get_array(), ax)
    #ax.set_title('K-Core Distribution')
    ax.set_xlabel('k-Core kC')
    ax.set_ylabel('P(x>=kC)')
    fig.savefig('output/wikipedia-transitions-kcore-ccdf.pdf')

    plt.clf()

    eigenvector_centr = network_transitions.vertex_properties["eigenvector_centr"]

    #hist, bin_edges = np.histogram(eigenvector_centr.get_array(), 100, density=True)
    #cdf = np.cumsum(hist)

    #plt.plot(bin_edges[1:], cdf, marker='o')
    #plt.xlabel('Eingenvector centrality E')
    #plt.ylabel('P(x<=E)')
    #plt.title('Eigenvector Centrality Distribution')
    #plt.savefig('output/wikipedia-transitions-eigenvcentr-cdf.pdf')


    fig, ax = plt.subplots()
    powerlaw.plot_cdf(eigenvector_centr.get_array(), ax)
    #ax.set_title('Eigenvector Centrality Distribution')
    ax.set_xlabel('Eingenvector centrality E')
    ax.set_ylabel('P(x<=E)')
    fig.savefig('output/wikipedia-transitions-eigenvcentr-cdf.pdf')
    plt.clf()

    fig, ax = plt.subplots()
    powerlaw.plot_ccdf(eigenvector_centr.get_array(), ax)
    #ax.set_title('Eigenvector Centrality Distribution')
    ax.set_xlabel('Eingenvector centrality E')
    ax.set_ylabel('P(x>=E)')
    fig.savefig('output/wikipedia-transitions-eigenvcentr-ccdf.pdf')
    plt.clf()

    print 'before hits'
    #ee, authority, hub = hits(network_transitions)
    #network_transitions.vertex_properties["authority"] = authority
    #network_transitions.vertex_properties["hub"] = hub
    #network_transitions.save("output/transitionsnetwork.xml.gz")
    print 'after hits'

    colors= {'local_clust':'r','eigenvector_centr':'b', 'page_rank': 'g', 'kcore':'m', 'hub': 'c', 'authority':'k'}
    labels = {'local_clust': 'clust.', 'eigenvector_centr':'eigen. centr.','page_rank': 'page rank', 'kcore': 'kcore', 'hub':'hub', 'authority':'authority'}
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for f in ['local_clust','page_rank', 'hub', 'authority', 'kcore']:
        feature = network_transitions.vertex_properties[f]
        powerlaw.plot_cdf(feature.get_array(), ax, label=labels[f],color=colors[f])
    ax.set_xlabel('Feature $f$')
    ax.set_ylabel('$P(X>=f)$')
    ax.set_ylim([0, 1])
    plt.legend(fancybox=True, loc=3, ncol=2, prop={'size':4})
    plt.tight_layout()
    plt.savefig('output/wikipedia-transitions-features-cdf.pdf')
    plt.clf()

    colors= {'local_clust':'r','eigenvector_centr':'b', 'page_rank': 'g', 'kcore':'m', 'hub': 'c', 'authority':'k'}
    labels = {'local_clust': 'clust.', 'eigenvector_centr':'eigen. centr.','page_rank': 'page rank', 'kcore': 'kcore', 'hub':'hub', 'authority':'authority'}
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for f in ['local_clust','page_rank', 'hub', 'authority', 'kcore']:
        feature = network_transitions.vertex_properties[f]
        powerlaw.plot_cdf(feature.get_array(), ax, label=labels[f],color=colors[f])
    ax.set_xlabel('Feature $f$')
    ax.set_ylabel('$P(X<=f)$')
    plt.legend(fancybox=True, loc=3, ncol=2, prop={'size':4})
    plt.tight_layout()
    plt.savefig('output/wikipedia-transitions-features-ccdf.pdf')

    plt.clf()

def plot_degree():
    # wikipedia  graph  structural statistics
    print 'before load'
    network = load_graph("output/wikipedianetwork.xml.gz")
    print 'after load'

    print 'before load'
    network_transitions = load_graph("output/transitionsnetwork.xml.gz")
    print 'after load'
    out_hist = vertex_hist(network, "out")
    fig, ax = plt.subplots()

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.plot(out_hist[1][:-1], out_hist[0], marker='o', markersize=3, label='wikipedia', color='b')

    out_hist = vertex_hist(network_transitions, "out")
    ax.plot(out_hist[1][:-1], out_hist[0], marker='o', markersize=3, label='transitions', color='r')
    plt.legend(fancybox=True, loc='upper right', ncol=1, prop={'size':4}, numpoints=1, handlelength=0)
    ax.set_ylim([10**0, 10**6])
    ax.set_xlabel('Out-degree')
    ax.set_ylabel('Frequency')
    fig.tight_layout()
    fig.savefig('output/wikipedia-transitions-outdegree.pdf')

    out_hist = vertex_hist(network, "in")
    fig, ax = plt.subplots()

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.plot(out_hist[1][:-1], out_hist[0], marker='o', markersize=3, label='wikipedia', color='b')

    out_hist = vertex_hist(network_transitions, "in")
    ax.plot(out_hist[1][:-1], out_hist[0], marker='o', markersize=3, label='transitions', color='r')
    plt.legend(fancybox=True, loc='upper right', ncol=1, prop={'size':4}, numpoints=1, handlelength=0)
    ax.set_ylim([10**0, 10**6])
    ax.set_xlabel('In-degree')
    ax.set_ylabel('Frequency')
    fig.tight_layout()
    fig.savefig('output/wikipedia-transitions-indegree.pdf')

    out_hist = vertex_hist(network, "total")
    fig, ax = plt.subplots()

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.plot(out_hist[1][:-1], out_hist[0], marker='o', markersize=3, label='wikipeida', color='b')

    out_hist = vertex_hist(network_transitions, "total")
    ax.plot(out_hist[1][:-1], out_hist[0], marker='o', markersize=3, label='transitions', color='r')
    plt.legend(fancybox=True, loc='upper right', ncol=1, prop={'size':4}, numpoints=1, handlelength=0)
    ax.set_ylim([10**0, 10**6])
    ax.set_xlabel('Degree')
    ax.set_ylabel('Frequency')
    fig.tight_layout()
    fig.savefig('output/wikipedia-transitions-degree.pdf')

def plot_degree_filtered():
    # wikipedia  graph  structural statistics
    print 'before load'
    network = load_graph("output/wikipedianetwork.xml.gz")
    print 'after load'

    print 'before load'
    network_transitions = load_graph("output/transitionsnetwork.xml.gz")
    print 'after load'

    network = GraphView(network, vfilt=filter_transitions(network,network_transitions))
    print 'filter out'
    out_hist = vertex_hist(network, "out")
    fig, ax = plt.subplots()

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.plot(out_hist[1][:-1], out_hist[0], marker='o', markersize=3, label='wikipedia', color='b')

    out_hist = vertex_hist(network_transitions, "out")
    ax.plot(out_hist[1][:-1], out_hist[0], marker='o', markersize=3, label='transitions', color='r')
    plt.legend(fancybox=True, loc='upper right', ncol=1, prop={'size':4}, numpoints=1, handlelength=0)
    ax.set_ylim([10**0, 10**6])
    ax.set_xlim([10**0, 10**6])
    ax.set_xlabel('Out-degree')
    ax.set_ylabel('Frequency')
    fig.tight_layout()
    fig.savefig('output/wikipedia-transitions-outdegree-filtered.pdf')

    out_hist = vertex_hist(network, "in")
    fig, ax = plt.subplots()

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.plot(out_hist[1][:-1], out_hist[0], marker='o', markersize=3, label='wikipedia', color='b')

    out_hist = vertex_hist(network_transitions, "in")
    ax.plot(out_hist[1][:-1], out_hist[0], marker='o', markersize=3, label='transitions', color='r')
    plt.legend(fancybox=True, loc='upper right', ncol=1, prop={'size':4}, numpoints=1, handlelength=0)
    ax.set_ylim([10**0, 10**6])
    ax.set_xlim([10**0, 10**6])
    ax.set_xlabel('In-degree')
    ax.set_ylabel('Frequency')
    fig.tight_layout()
    fig.savefig('output/wikipedia-transitions-indegree-filtered.pdf')

    out_hist = vertex_hist(network, "total")
    fig, ax = plt.subplots()

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.plot(out_hist[1][:-1], out_hist[0], marker='o', markersize=3, label='wikipeida', color='b')

    out_hist = vertex_hist(network_transitions, "total")
    ax.plot(out_hist[1][:-1], out_hist[0], marker='o', markersize=3, label='transitions', color='r')
    plt.legend(fancybox=True, loc='upper right', ncol=1, prop={'size':4}, numpoints=1, handlelength=0)
    ax.set_ylim([10**0, 10**6])
    ax.set_xlim([10**0, 10**6])
    ax.set_xlabel('Degree')
    ax.set_ylabel('Frequency')
    fig.tight_layout()
    fig.savefig('output/wikipedia-transitions-degree-filtered.pdf')
    print 'fit'
    fp.powerLawExponent('transitions', network_transitions)
    fp.powerLawExponent('filtred_network', network)

def filter_transitions(network1, network2):
    filter = network1.new_vertex_property('bool')
    print 'filter'
    found_false = False
    for i,v in enumerate(network1.vertices()):
        if i% 100000==0:
            print i
        if v in network2.vertices():
            #print "true"
            filter[v]=True
        else:
            if not found_false:
                print "false"
                found_false=True
            filter[v]=False
    return filter





def plot_features():
    print 'before load'
    network = load_graph("output/wikipedianetwork.xml.gz")
    print 'after load'

    print 'before load'
    network_transitions = load_graph("output/transitionsnetwork.xml.gz")
    print 'after load'

    colors= {'local_clust':'r','eigenvector_centr':'b', 'page_rank': 'g', 'kcore':'m', 'hub': 'c', 'authority':'k'}
    labels = {'local_clust': 'clust.', 'eigenvector_centr':'eigen. centr.','page_rank': 'page rank', 'kcore': 'kcore', 'hub':'hub', 'authority':'authority'}
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for f in ['local_clust','page_rank', 'hub', 'authority', 'kcore']:
        feature = network_transitions.vertex_properties[f]
        powerlaw.plot_cdf(feature.get_array(), ax, label=labels[f],color=colors[f])
    ax.set_xlabel('Feature $f$')
    ax.set_ylabel('$P(X>=f)$')
    ax.set_ylim([0, 1])
    plt.legend(fancybox=True, loc=3, ncol=2, prop={'size':4})
    plt.tight_layout()
    plt.savefig('output/wikipedia-transitions-features-cdf.pdf')
    plt.clf()

    colors= {'local_clust':'r','eigenvector_centr':'b', 'page_rank': 'g', 'kcore':'m', 'hub': 'c', 'authority':'k'}
    labels = {'local_clust': 'clust.', 'eigenvector_centr':'eigen. centr.','page_rank': 'page rank', 'kcore': 'kcore', 'hub':'hub', 'authority':'authority'}
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for f in ['local_clust','page_rank', 'hub', 'authority', 'kcore']:
        feature = network_transitions.vertex_properties[f]
        powerlaw.plot_cdf(feature.get_array(), ax, label=labels[f],color=colors[f])
    ax.set_xlabel('Feature $f$')
    ax.set_ylabel('$P(X<=f)$')
    plt.legend(fancybox=True, loc=3, ncol=2, prop={'size':4})
    plt.tight_layout()
    plt.savefig('output/wikipedia-transitions-features-ccdf.pdf')

    plt.clf()

    colors= {'local_clust':'r','eigenvector_centr':'b', 'page_rank': 'g', 'kcore':'m', 'hub': 'c', 'authority':'k'}
    labels = {'local_clust': 'clust.', 'eigenvector_centr':'eigen. centr.','page_rank': 'page rank', 'kcore': 'kcore', 'hub':'hub', 'authority':'authority'}
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for f in ['local_clust','page_rank', 'hub', 'authority', 'kcore']:
        feature = network.vertex_properties[f]
        powerlaw.plot_cdf(feature.get_array(), ax, label=labels[f],color=colors[f])
    ax.set_xlabel('Feature $f$')
    ax.set_ylabel('$P(X>=f)$')
    ax.set_ylim([0, 1])
    plt.legend(fancybox=True, loc=3, ncol=2, prop={'size':4})
    plt.tight_layout()
    plt.savefig('output/wikipedia-features-cdf.pdf')

    plt.clf()
    colors= {'local_clust':'r','eigenvector_centr':'b', 'page_rank': 'g', 'kcore':'m', 'hub': 'c', 'authority':'k'}
    labels = {'local_clust': 'clust.', 'eigenvector_centr':'eigen. centr.','page_rank': 'page rank', 'kcore': 'kcore', 'hub':'hub', 'authority':'authority'}
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for f in ['local_clust','eigenvector_centr','page_rank', 'hub', 'authority', 'kcore']:
        feature = network.vertex_properties[f]
        powerlaw.plot_cdf(feature.get_array(), ax, label=labels[f],color=colors[f])
    ax.set_xlabel('Feature $f$')
    ax.set_ylabel('$P(X<=f)$')
    plt.legend(fancybox=True, loc=3, ncol=2, prop={'size':4})
    plt.tight_layout()
    plt.savefig('output/wikipedia-features-ccdf.pdf')



def plot_degree_filtered_sql():
    print 'before select'
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    conn = db._create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT source_article_id, target_article_id FROM link_occurences where source_article_id in '
                   ' (select distinct prev_id from clickstream_derived_internal_links);')
    result = cursor.fetchall()
    network = Graph()
    print 'after select'
    print 'result len'
    print len(result)

    for i, link in enumerate(result):
        if i % 1000000==0:
            print i, len(result)
        network.add_edge(link[0], link[1])

    # filter all nodes that have no edges
    print 'filter nodes with degree zero graph tool specific code'
    network = GraphView(network, vfilt=lambda v : v.out_degree()+v.in_degree()>0 )
    print 'before save'
    network.save("output/wikipedianetworkfilteredwithtransitions_prev_id.xml.gz")
    print 'done'

    cursor.execute('SELECT source_article_id, target_article_id FROM link_occurences where target_article_id in '
                   ' (select distinct curr_id from clickstream_derived_internal_links);')
    result = cursor.fetchall()
    network = Graph()
    print 'after select'
    print 'resutl len'
    print len(result)

    for i, link in enumerate(result):
        if i % 1000000==0:
            print i, len(result)
        network.add_edge(link[0], link[1])

    # filter all nodes that have no edges
    print 'filter nodes with degree zero graph tool specific code'
    network = GraphView(network, vfilt=lambda v : v.out_degree()+v.in_degree()>0 )
    print 'before save'
    network.save("output/wikipedianetworkfilteredwithtransitions_curr_id.xml.gz")
    print 'done'

def plot_degree_filtered_with_transitions(network_name):
    # wikipedia  graph  structural statistics
    print 'before load'
    network = load_graph("output/wikipedianetworkfilteredwithtransitions_"+network_name+".xml.gz")
    print 'after load'

    print 'before load'
    network_transitions = load_graph("output/transitionsnetwork.xml.gz")
    print 'after load'

    out_hist = vertex_hist(network, "out")
    fig, ax = plt.subplots()

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.plot(out_hist[1][:-1], out_hist[0], marker='o', markersize=3, markeredgecolor='none', label=r'$D_{wiki}$')

    out_hist = vertex_hist(network_transitions, "out")
    ax.plot(out_hist[1][:-1], out_hist[0], marker='o', markersize=3, markeredgecolor='none', label=r'$D_{trans}$')
    plt.legend(fancybox=True, loc='upper right', ncol=1, prop={'size':5})
    #plt.legend(fancybox=True, loc='upper right', ncol=1, prop={'size':5}, numpoints=1, handlelength=0)
    ax.set_ylim([10**0, 10**6])
    ax.set_xlim([10**0, 10**4])
    ax.set_xlabel('Out-degree')
    ax.set_ylabel('Frequency')
    fig.tight_layout()
    fig.savefig('output/wikipedia-transitions-outdegree-filtered'+network_name+'-sql.pdf', bbox_inches='tight')

    out_hist = vertex_hist(network, "in")
    fig, ax = plt.subplots()

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.plot(out_hist[1][:-1], out_hist[0], marker='o', markersize=3, markeredgecolor='none', label=r'$D_{wiki}$')

    out_hist = vertex_hist(network_transitions, "in")
    ax.plot(out_hist[1][:-1], out_hist[0], marker='o', markersize=3, markeredgecolor='none', label=r'$D_{trans}$')
    plt.legend(fancybox=True, loc='upper right', ncol=1, prop={'size':5})
    #plt.legend(fancybox=True, loc='upper right', ncol=1, prop={'size':5}, numpoints=1, handlelength=0)
    ax.set_ylim([10**0, 10**6])
    ax.set_xlim([10**0, 10**6])
    ax.set_xlabel('In-degree')
    ax.set_ylabel('Frequency')
    fig.tight_layout()
    fig.savefig('output/wikipedia-transitions-indegree-filtered'+network_name+'-sql.pdf', bbox_inches='tight')

    out_hist = vertex_hist(network, "total")
    fig, ax = plt.subplots()

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.plot(out_hist[1][:-1], out_hist[0], marker='o', markersize=3, markeredgecolor='none', label='wikipeida')

    out_hist = vertex_hist(network_transitions, "total")
    ax.plot(out_hist[1][:-1], out_hist[0], marker='o', markersize=3, markeredgecolor='none', label='transitions')
    plt.legend(fancybox=True, loc='upper right', ncol=1, prop={'size':5})
    #plt.legend(fancybox=True, loc='upper right', ncol=1, prop={'size':5}, numpoints=1, handlelength=0)
    ax.set_ylim([10**0, 10**6])
    ax.set_xlim([10**0, 10**6])
    ax.set_xlabel('Degree')
    ax.set_ylabel('Frequency')
    fig.tight_layout()
    fig.savefig('output/wikipedia-transitions-degree-filtered'+network_name+'-sql.pdf', bbox_inches='tight')
    print 'fit'+network_name
    fp.powerLawExponent('transitions', network_transitions)
    fp.powerLawExponent(network_name, network)




if __name__ == '__main__':
    #plot_degree_filtered_sql()
    plot_degree_filtered_with_transitions('prev_id')
    #plot_degree_filtered_with_transitions('curr_id')

    #plot_degree_filtered()
    #plot_degree()
    #plot_features()




