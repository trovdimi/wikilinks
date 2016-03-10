from wsd.database import MySQLDatabase
from graph_tool.all import *
from dbsettings import *
__author__ = 'dimitrovdr'

db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
db_work_view = db.get_work_view()

wikipedia = Graph()

for link in db_work_view.retrieve_all_unique_links():
    wikipedia.add_edge(link['from'], link['to'])

print "clust"
wikipedia.vertex_properties["local_clust"] = local_clustering(wikipedia)

print "page_rank"
wikipedia.vertex_properties["page_rank"] = pagerank(wikipedia)

print "eigenvector_centr"
eigenvalue, eigenvectorcentr = eigenvector(wikipedia)
wikipedia.vertex_properties["eigenvector_centr"] = eigenvectorcentr

print "kcore"
wikipedia.vertex_properties["kcore"] = kcore_decomposition(wikipedia)

wikipedia.save("wikipediaNetwork.xml.gz")


