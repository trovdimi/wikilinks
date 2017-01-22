from wsd.database import MySQLDatabase
from graph_tool.all import *
from conf import *
__author__ = 'dimitrovdr'


db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
db_work_view = db.get_work_view()

wikipedia = Graph()

for link in db_work_view.retrieve_all_internal_transitions_counts():
    for i in range(int(link['counts'])) :
        wikipedia.add_edge(link['from'], link['to'])

    #print 'from %s, to %s', link['from'], link['to']



#wikipedia.save("output/transitionsnetwork.xml.gz")

# filter all nodes that have no edges
transitions_network = GraphView(wikipedia, vfilt=lambda v : v.out_degree()+v.in_degree()>0 )


transitions_network.save("output/transitionsnetworkweighted.xml.gz")

print "Stats for transitions network:"
print "number of nodes: %d" %transitions_network.num_vertices()
print "number of edges: %d" %transitions_network.num_edges()



