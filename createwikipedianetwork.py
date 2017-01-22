from wsd.database import MySQLDatabase
from graph_tool.all import *
from conf import *
__author__ = 'dimitrovdr'

db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
conn = db._create_connection()
cursor = conn.cursor()
cursor.execute('SELECT source_article_id, target_article_id FROM link_occurences;')
result = cursor.fetchall()
wikipedia = Graph()

for link in result:
    wikipedia.add_edge(link[0], link[1])

# filter all nodes that have no edges
wikipedia = GraphView(wikipedia, vfilt=lambda v : v.out_degree()+v.in_degree()>0 )

print "clust"
wikipedia.vertex_properties["local_clust"] = local_clustering(wikipedia)

print "page_rank"
wikipedia.vertex_properties["page_rank"] = pagerank(wikipedia)

print "eigenvector_centr"
eigenvalue, eigenvectorcentr = eigenvector(wikipedia)
wikipedia.vertex_properties["eigenvector_centr"] = eigenvectorcentr

print "kcore"
wikipedia.vertex_properties["kcore"] = kcore_decomposition(wikipedia)


#print "closeness"
#wikipedia.vertex_properties["closeness"] = closeness(wikipedia)

#print "katz"
#wikipedia.vertex_properties["katz"] = katz(wikipedia, norm=False)

print "hits"
ee, authority, hub = hits(wikipedia)
wikipedia.vertex_properties["authority"] = authority
wikipedia.vertex_properties["hub"] = hub
#wikipedia.vertex_properties["ee"] = ee

wikipedia.save("output/wikipedianetwork.xml.gz")


