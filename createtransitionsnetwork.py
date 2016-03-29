from wsd.database import MySQLDatabase
from graph_tool.all import *
from conf import *
__author__ = 'dimitrovdr'


db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
db_work_view = db.get_work_view()

wikipedia = Graph()

for link in db_work_view.retrieve_all_transitions():
    wikipedia.add_edge(link['from'], link['to'])
    #print 'from %s, to %s', link['from'], link['to']



#wikipedia.save("output/transitionsnetwork.xml.gz")

# filter all nodes that have no edges
transitions_network = GraphView(wikipedia, vfilt=lambda v : v.out_degree()+v.in_degree()>0 )

print "clust"
transitions_network.vertex_properties["local_clust"] = local_clustering(transitions_network)

print "page_rank"
transitions_network.vertex_properties["page_rank"] = pagerank(transitions_network)

print "eigenvector_centr"
eigenvalue, eigenvectorcentr = eigenvector(transitions_network)
transitions_network.vertex_properties["eigenvector_centr"] = eigenvectorcentr

print "kcore"
transitions_network.vertex_properties["kcore"] = kcore_decomposition(transitions_network)

transitions_network.save("output/transitionsnetwork.xml.gz")

print "Stats for transitions network:"
print "number of nodes: %d" %transitions_network.num_vertices()
print "number of edges: %d" %transitions_network.num_edges()

scc_labels = label_largest_component(transitions_network, directed=True)
wcc_labels = label_largest_component(transitions_network, directed=False)


networks_transitions_scc = GraphView(transitions_network, vfilt=scc_labels)
print "SCC for transitions network:"
print "number of nodes: %d" %networks_transitions_scc.num_vertices()
print "number of edges: %d" %networks_transitions_scc.num_edges()


networks_transitions_wcc = GraphView(transitions_network, vfilt=wcc_labels)
print "WCC for transitions network:"
print "number of nodes: %d"  %networks_transitions_wcc.num_vertices()
print "number of edges: %d"  %networks_transitions_wcc.num_edges()


