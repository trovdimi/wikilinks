from __future__ import division
__author__ = 'dimitrovdr'

import numpy as np
from graph_tool.all import *
from matplotlib import pyplot as plt
import pickle

# wikipedia  graph  structural statistics
print 'before load'
network = load_graph("wikipediaNetwork.xml.gz")
print 'after load'


clust = network.vertex_properties["local_clust"]
n, bins, patches = plt.hist(clust.get_array(), 100, normed=1,
                            histtype='step', cumulative=True)


plt.xlabel('Local Clustering Coefficient C')
plt.ylabel('P(x<=C)')
plt.title('Clustering Coefficient Distribution')
plt.savefig('wikipedia-clust-cdf-hist.png')
plt.savefig('wikipedia-clust-cdf-hist.pdf')

plt.clf()

prank = network.vertex_properties["page_rank"]

n, bins, patches = plt.hist(prank.get_array(), 100, normed=1,
                            histtype='step', cumulative=True)
plt.xlabel('Page rank Pr')
plt.ylabel('P(x<=Pr)')
plt.title('Page rank Distribution')
plt.savefig('wikipedia-prank-cdf-hist.png')
plt.savefig('wikipedia-prank-cdf-hist.pdf')

plt.clf()

kcore = network.vertex_properties["kcore"]
n, bins, patches = plt.hist(kcore.get_array(), 100, normed=1,
                            histtype='step', cumulative=True)
plt.xlabel('Kcore kC')
plt.ylabel('P(x<=kC)')
plt.title('K-Core Distribution')
plt.savefig('wikipedia-kcore-cdf-hist.png')
plt.savefig('wikipedia-kcore-cdf-hist.pdf')

plt.clf()


eigenvector_centr = network.vertex_properties["eigenvector_centr"]

n, bins, patches = plt.hist(eigenvector_centr.get_array(), 100, normed=1,
                            histtype='step', cumulative=True)
plt.xlabel('Eigenvector Centrality E')
plt.ylabel('P(x<=E)')
plt.title('Eigenvector Centrality Distribution')
plt.savefig('wikipedia-eigenvcentr-cdf-hist.png')
plt.savefig('wikipedia-eigenvcentr-cdf-hist.pdf')

plt.clf()


# wikipedia transitions  graph  structural statistics
print 'before load'
network_transitions = load_graph("wikipediaNetworkFromTransitions.xml.gz")
print 'after load'



clust = network_transitions.vertex_properties["local_clust"]

n, bins, patches = plt.hist(clust.get_array(), 100, normed=1,
                            histtype='step', cumulative=True)

plt.xlabel('Local Clustering Coefficient C')
plt.ylabel('P(x<=C)')
plt.title('Clustering Coefficient Distribution')
plt.savefig('wikipedia-transitions-clust-cdf-hist.png')
plt.savefig('wikipedia-transitions-clust-cdf-hist.pdf')

plt.clf()

prank = network_transitions.vertex_properties["page_rank"]

n, bins, patches = plt.hist(prank.get_array(), 100, normed=1,
                            histtype='step', cumulative=True)
plt.xlabel('Page rank Pr')
plt.ylabel('P(x<=Pr)')
plt.title('Page rank Distribution')
plt.savefig('wikipedia-transitions-prank-cdf-hist.png')
plt.savefig('wikipedia-transitions-prank-cdf-hist.pdf')

plt.clf()

kcore = network_transitions.vertex_properties["kcore"]

n, bins, patches = plt.hist(kcore.get_array(), 100, normed=1,
                            histtype='step', cumulative=True)
plt.xlabel('Kcore kC')
plt.ylabel('P(x<=kC)')
plt.title('K-Core Distribution')
plt.savefig('wikipedia-transitions-kcore-cdf-hist.png')
plt.savefig('wikipedia-transitions-kcore-cdf-hist.pdf')

plt.clf()


eigenvector_centr = network_transitions.vertex_properties["eigenvector_centr"]

n, bins, patches = plt.hist(eigenvector_centr.get_array(), 100, normed=1,
                            histtype='step', cumulative=True)
plt.xlabel('Eingenvector centrality E')
plt.ylabel('P(x<=E)')
plt.title('Eigenvector Centrality Distribution')
plt.savefig('wikipedia-transitions-eigenvcentr-cdf-hist.png')
plt.savefig('wikipedia-transitions-eigenvcentr-cdf-hist.pdf')

plt.clf()




