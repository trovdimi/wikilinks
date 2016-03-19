from __future__ import division
__author__ = 'dimitrovdr'

import numpy as np
from graph_tool.all import *
from matplotlib import pyplot as plt
import pickle
import powerlaw


# wikipedia  graph  structural statistics
print 'before load'
network = load_graph("output/wikipediaNetwork.xml.gz")
print 'after load'
out_hist = vertex_hist(network, "out")
plt.gca().set_yscale('log')
plt.gca().set_xscale('log')
plt.plot(out_hist[0], marker='o')
plt.xlabel('Number of nodes')
plt.ylabel('Degree')
plt.title('Out-Degree Distribution')
plt.savefig('output/wikipedia-out-deg-dist.png')
plt.savefig('output/wikipedia-out-deg-dist.pdf')

plt.clf()

in_hist = vertex_hist(network, "in")
plt.gca().set_yscale('log')
plt.gca().set_xscale('log')
plt.plot(in_hist[0], marker='o')
plt.xlabel('Number of nodes')
plt.ylabel('Degree')
plt.title('In-Degree Distribution')
plt.savefig('wikipedia-in-deg-dist.png')
plt.savefig('wikipedia-in-deg-dist.pdf')

plt.clf()

total_hist = vertex_hist(network, "total")

plt.gca().set_yscale('log')
plt.gca().set_xscale('log')
plt.plot(total_hist[0], marker='o')
plt.xlabel('Number of nodes')
plt.ylabel('Degree')
plt.title('Degree Distribution')
plt.savefig('wikipedia-deg-dist.png')
plt.savefig('wikipedia-deg-dist.pdf')

plt.clf()

clust = network.vertex_properties["local_clust"]
#clust = local_clustering(network, undirected=False)

#hist, bin_edges = np.histogram(clust.get_array(), 100, density=True)
#cdf = np.cumsum(hist)

#plt.plot(bin_edges[1:], cdf, marker='o')
#plt.xlabel('Local Clustering Coefficient C')
#plt.ylabel('P(x<=C)')
#plt.title('Clustering Coefficient Distribution')
#plt.savefig('wikipedia-clust-cdf.png')
#plt.savefig('wikipedia-clust-cdf.pdf')

fig, ax = plt.subplots()
powerlaw.plot_cdf(clust.get_array(), ax)
ax.set_title('Clustering Coefficient Distribution')
ax.set_xlabel('Local Clustering Coefficient C')
ax.set_ylabel('P(x<=C)')
fig.savefig('wikipedia-clust-cdf.pdf')

plt.clf()

prank = network.vertex_properties["page_rank"]

#hist, bin_edges = np.histogram(prank.get_array(), 100, density=True)
#cdf = np.cumsum(hist)

#plt.plot(bin_edges[1:], cdf, marker='o')
#plt.xlabel('Page rank Pr')
#plt.ylabel('P(x<=Pr)')
#plt.title('Page rank Distribution')
#plt.savefig('wikipedia-prank-cdf.png')
#plt.savefig('wikipedia-prank-cdf.pdf')
fig, ax = plt.subplots()
powerlaw.plot_cdf(prank.get_array(), ax)
ax.set_title('Page Rank Distribution')
ax.set_xlabel('Page rank Pr')
ax.set_ylabel('P(x<=Pr)')
fig.savefig('wikipedia-prank-cdf.pdf')

plt.clf()

kcore = network.vertex_properties["kcore"]

#hist, bin_edges = np.histogram(kcore.get_array(), 100, density=True)
#cdf = np.cumsum(hist)
#plt.plot(bin_edges[1:], cdf, marker='o')
#plt.xlabel('Kcore kC')
#plt.ylabel('P(x<=kC)')
#plt.title('K-Core Distribution')
#plt.savefig('wikipedia-kcore-cdf.png')
#plt.savefig('wikipedia-kcore-cdf.pdf')

fig, ax = plt.subplots()
powerlaw.plot_cdf(kcore.get_array(), ax)
ax.set_title('K-Core Distribution')
ax.set_xlabel('k-Core kC')
ax.set_ylabel('P(x<=kC)')
fig.savefig('wikipedia-kcore-cdf.pdf')

plt.clf()


eigenvector_centr = network.vertex_properties["eigenvector_centr"]

#hist, bin_edges = np.histogram(eigenvector_centr.get_array(), 100, density=True)
#cdf = np.cumsum(hist)
#plt.plot(bin_edges[1:], cdf, marker='o')
#plt.xlabel('Eigenvector Centrality E')
#plt.ylabel('P(x<=E)')
#plt.title('Eigenvector Centrality Distribution')
#plt.savefig('wikipedia-eigenvcentr-cdf.png')
#plt.savefig('wikipedia-eigenvcentr-cdf.pdf')

fig, ax = plt.subplots()
powerlaw.plot_cdf(eigenvector_centr.get_array(), ax)
ax.set_title('Eigenvector Centrality E')
ax.set_xlabel('Eigenvector Centrality Distribution')
ax.set_ylabel('P(x<=E)')
fig.savefig('wikipedia-eigenvcentr-cdf.pdf')

plt.clf()


# wikipedia transitions  graph  structural statistics
print 'before load'
network_transitions = load_graph("output/wikipediaNetworkFromTransitions.xml.gz")
print 'after load'

out_hist = vertex_hist(network_transitions, "out")
plt.gca().set_yscale('log')
plt.gca().set_xscale('log')
plt.plot(out_hist[0], marker='o')
plt.xlabel('Number of nodes')
plt.ylabel('Degree')
plt.title('Out-Degree Distribution')
plt.savefig('wikipedia-transitions-out-deg-dist.png')
plt.savefig('wikipedia-transitions-out-deg-dist.pdf')

plt.clf()

in_hist = vertex_hist(network_transitions, "in")
plt.gca().set_yscale('log')
plt.gca().set_xscale('log')
plt.plot(in_hist[0], marker='o')
plt.xlabel('Number of nodes')
plt.ylabel('Degree')
plt.title('In-Degree Distribution')
plt.savefig('wikipedia-transitions-in-deg-dist.png')
plt.savefig('wikipedia-transitions-in-deg-dist.pdf')

plt.clf()

total_hist = vertex_hist(network_transitions, "total")

plt.gca().set_yscale('log')
plt.gca().set_xscale('log')
plt.plot(total_hist[0], marker='o')
plt.xlabel('Number of nodes')
plt.ylabel('Degree')
plt.title('Degree Distribution')
plt.savefig('wikipedia-transitions-deg-dist.png')
plt.savefig('wikipedia-transitions-deg-dist.pdf')

plt.clf()

#clust = local_clustering(network_transitions, undirected=False)
clust = network_transitions.vertex_properties["local_clust"]

#hist, bin_edges = np.histogram(clust.get_array(), 100, density=True)
#cdf = np.cumsum(hist)
#plt.plot(bin_edges[1:], cdf, marker='o')
#plt.xlabel('Local Clustering Coefficient C')
#plt.ylabel('P(x<=C)')
#plt.title('Clustering Coefficient Distribution')
#plt.savefig('wikipedia-transitions-clust-cdf.png')
#plt.savefig('wikipedia-transitions-clust-cdf.pdf')

fig, ax = plt.subplots()
powerlaw.plot_cdf(clust.get_array(), ax)
ax.set_title('Clustering Coefficient Distribution')
ax.set_xlabel('Local Clustering Coefficient C')
ax.set_ylabel('P(x<=C)')
fig.savefig('wikipedia-transitions-clust-cdf.pdf')

plt.clf()

prank = network_transitions.vertex_properties["page_rank"]

#hist, bin_edges = np.histogram(prank.get_array(), 100, density=True)
#cdf = np.cumsum(hist)
#plt.plot(bin_edges[1:], cdf, marker='o')
#plt.xlabel('Page rank Pr')
#plt.ylabel('P(x<=Pr)')
#plt.title('Page rank Distribution')
#plt.savefig('wikipedia-transitions-prank-cdf.png')
#plt.savefig('wikipedia-transitions-prank-cdf.pdf')

fig, ax = plt.subplots()
powerlaw.plot_cdf(prank.get_array(), ax)
ax.set_title('Page Rank Distribution')
ax.set_xlabel('Page rank Pr')
ax.set_ylabel('P(x<=Pr)')
fig.savefig('wikipedia-transitions-prank-cdf.pdf')

plt.clf()

kcore = network_transitions.vertex_properties["kcore"]

#hist, bin_edges = np.histogram(kcore.get_array(), 100, density=True)
#cdf = np.cumsum(hist)

#plt.plot(bin_edges[1:], cdf, marker='o')
#plt.xlabel('Kcore kC')
#plt.ylabel('P(x<=kC)')
#plt.title('K-Core Distribution')
#plt.savefig('wikipedia-transitions-kcore-cdf.png')
#plt.savefig('wikipedia-transitions-kcore-cdf.pdf')

fig, ax = plt.subplots()
powerlaw.plot_cdf(kcore.get_array(), ax)
ax.set_title('K-Core Distribution')
ax.set_xlabel('k-Core kC')
ax.set_ylabel('P(x<=kC)')
fig.savefig('wikipedia-transitions-kcore-cdf.pdf')

plt.clf()


eigenvector_centr = network_transitions.vertex_properties["eigenvector_centr"]

#hist, bin_edges = np.histogram(eigenvector_centr.get_array(), 100, density=True)
#cdf = np.cumsum(hist)

#plt.plot(bin_edges[1:], cdf, marker='o')
#plt.xlabel('Eingenvector centrality E')
#plt.ylabel('P(x<=E)')
#plt.title('Eigenvector Centrality Distribution')
#plt.savefig('wikipedia-transitions-eigenvcentr-cdf.png')
#plt.savefig('wikipedia-transitions-eigenvcentr-cdf.pdf')


fig, ax = plt.subplots()
powerlaw.plot_cdf(eigenvector_centr.get_array(), ax)
ax.set_title('Eigenvector Centrality Distribution')
ax.set_xlabel('Eingenvector centrality E')
ax.set_ylabel('P(x<=E)')
fig.savefig('wikipedia-transitions-eigenvcentr-cdf.pdf')
plt.clf()




