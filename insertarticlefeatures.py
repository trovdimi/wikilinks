import logging
import MySQLdb
from wsd.database import MySQLDatabase
from graph_tool.all import *
from conf import *
import cPickle
import os

__author__ = 'dimitrovdr'

db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
db_work_view = db.get_work_view()


def build_article_features_table():
    """creates up the basic database structure
    """
    connection = db._create_connection()
    cursor = connection.cursor()

    # build article_featues table
    cursor.execute('CREATE TABLE `article_features` ('
           '`id` bigint(20) unsigned NOT NULL,'
           '`in_degree` int(11) NOT NULL DEFAULT 0,'
           '`out_degree` int(11) NOT NULL DEFAULT 0,'
           '`degree` int(11) NOT NULL DEFAULT 0,'
           '`page_rank` double DEFAULT NULL,'
           '`local_clustering` double DEFAULT NULL,'
           '`eigenvector_centr` double DEFAULT NULL,'
           '`kcore` double DEFAULT NULL,'
           '`hits_authority` double DEFAULT NULL,'
           '`hits_hub` double DEFAULT NULL,'
           'PRIMARY KEY (`id`)'
           ') ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;')
    connection.close()

def insert_article_features():

    connection = db._create_connection()
    cursor = connection.cursor()

    network = load_graph("output/wikipedianetwork.xml.gz")
    print 'graph loaded'
    articles = db_work_view.retrieve_all_articles()
    print 'articles loaded'

    # setup logging
    LOGGING_FORMAT = '%(levelname)s:\t%(asctime)-15s %(message)s'
    LOGGING_PATH = 'tmp/articlefeatures-dbinsert.log'
    logging.basicConfig(filename=LOGGING_PATH, level=logging.DEBUG, format=LOGGING_FORMAT, filemode='w')

    for article in articles:
        try:
            article_features = {}
            vertex = network.vertex(article['id'])
            article_features['id'] = article['id']
            article_features['in_degree'] = vertex.in_degree()
            article_features['out_degree'] = vertex.out_degree()
            article_features['degree'] = vertex.in_degree() + vertex.out_degree()
            article_features['page_rank'] = network.vertex_properties["page_rank"][vertex]
            article_features['eigenvector_centr'] = network.vertex_properties["eigenvector_centr"][vertex]
            article_features['local_clust'] = network.vertex_properties["local_clust"][vertex]
            article_features['kcore'] = network.vertex_properties["kcore"][vertex]
            article_features['hits_authority'] = network.vertex_properties["authority"][vertex]
            article_features['hits_hub'] = network.vertex_properties["hub"][vertex]

            sql = "INSERT INTO article_features (id, in_degree," \
                             "out_degree, degree, page_rank, " \
                             "local_clustering, eigenvector_centr," \
                             " kcore, hits_authority, hits_hub) VALUES" \
                             "(%(id)s, %(in_degree)s, %(out_degree)s," \
                             "%(degree)s, %(page_rank)s,  %(eigenvector_centr)s, " \
                             "%(local_clust)s, %(kcore)s, %(hits_authority)s, %(hits_hub)s);"


            cursor.execute(sql, article_features)
            #logging.info('DB Insert Success for article id: "%s" ' % article['id'])
        except MySQLdb.Error as e:
            logging.error('DB Insert Error  article id: "%s" ' % article['id'])
        except ValueError:
            logging.error('ValueError for article id: "%s"' % article['id'])
        connection.commit()
    connection.close()


def alter_article_features_table():
    """add further features columns
    """
    connection = db._create_connection()
    cursor = connection.cursor()

    # alter article_featues table
    cursor.execute('ALTER TABLE article_features ADD COLUMN hits_authority DOUBLE, \
                    ADD COLUMN hits_hub DOUBLE, ADD COLUMN katz DOUBLE;')
    connection.close()

def update_article_features():

    connection = db._create_connection()
    cursor = connection.cursor()

    network = load_graph("output/wikipedianetwork.xml.gz")
    print 'graph loaded'
    articles = db_work_view.retrieve_all_articles()
    print 'articles loaded'

    # setup logging
    LOGGING_FORMAT = '%(levelname)s:\t%(asctime)-15s %(message)s'
    LOGGING_PATH = 'tmp/articlefeatures-dbinsert.log'
    logging.basicConfig(filename=LOGGING_PATH, level=logging.DEBUG, format=LOGGING_FORMAT, filemode='w')

    for article in articles:
        try:
            article_features = {}
            vertex = network.vertex(article['id'])
            article_features['id'] = article['id']
            article_features['hits_authority'] = network.vertex_properties["authority"][vertex]
            article_features['hits_hub'] = network.vertex_properties["hub"][vertex]
            #article_features['katz'] = network.vertex_properties["katz"][vertex]

            sql  = "UPDATE article_features " \
                   "SET hits_authority = %(hits_authority)s, hits_hub = %(hits_hub)s " \
                   "WHERE id = %(id)s;"

            cursor.execute(sql, article_features)

        except MySQLdb.Error as e:
            #logging.error('DB Insert Error  article id: "%s" ' % article['id'])
            print e
        except ValueError as v:
            logging.error('ValueError for article id: "%s"' % article['id'])
            print v
        connection.commit()
    connection.close()

def update_article_features_karz():

    connection = db._create_connection()
    cursor = connection.cursor()

    network = load_graph("output/wikipedianetwork.xml.gz")
    print 'graph loaded'
    articles = db_work_view.retrieve_all_articles()
    print 'articles loaded'

    # setup logging
    LOGGING_FORMAT = '%(levelname)s:\t%(asctime)-15s %(message)s'
    LOGGING_PATH = 'tmp/articlefeatures-dbinsert.log'
    logging.basicConfig(filename=LOGGING_PATH, level=logging.DEBUG, format=LOGGING_FORMAT, filemode='w')

    for article in articles:
        try:
            article_features = {}
            vertex = network.vertex(article['id'])
            article_features['id'] = article['id']
            article_features['katz'] = network.vertex_properties["katz"][vertex]

            sql  = "UPDATE article_features " \
                   "SET  katz=%(katz)s " \
                   "WHERE id = %(id)s;"

            cursor.execute(sql, article_features)

        except MySQLdb.Error as e:
            logging.error('DB Insert Error  article id: "%s" ' % article['id'])
            #print e
        except ValueError:
            logging.error('ValueError for article id: "%s"' % article['id'])
        connection.commit()
    connection.close()

def update_link_features_sem_similarity():

    connection = db._create_connection()
    cursor = connection.cursor()

    # setup logging
    LOGGING_FORMAT = '%(levelname)s:\t%(asctime)-15s %(message)s'
    LOGGING_PATH = 'tmp/link_features_semsim-dbinsert.log'
    logging.basicConfig(filename=LOGGING_PATH, level=logging.DEBUG, format=LOGGING_FORMAT, filemode='w')
    for dirname, dirnames, filenames in os.walk("/home/psinger/WikiLinks/data/sem_sim"):
        for file_name in filenames:
            if file_name.endswith(".p"):
                print file_name
                sem_sim = cPickle.load( open( "/home/psinger/WikiLinks/data/sem_sim/"+file_name, "rb" ) )
                for link, sim in sem_sim.iteritems():
                    try:
                        link_features = {}
                        link_features['source_article_id'] = link[0]
                        link_features['target_article_id'] = link[1]
                        link_features['sim'] = sim

                        sql  = "UPDATE link_features " \
                               "SET  sem_similarity=%(sim)s " \
                               "WHERE source_article_id = %(source_article_id)s AND target_article_id = %(target_article_id)s;"

                        cursor.execute(sql, link_features)

                    except MySQLdb.Error as e:
                        logging.error(e)
                    connection.commit()
                    try:
                        link_features = {}
                        link_features['source_article_id'] = link[1]
                        link_features['target_article_id'] = link[0]
                        link_features['sim'] = sim

                        sql  = "UPDATE link_features " \
                               "SET  sem_similarity=%(sim)s " \
                               "WHERE source_article_id = %(source_article_id)s AND target_article_id = %(target_article_id)s;"

                        cursor.execute(sql, link_features)

                    except MySQLdb.Error as e:
                        logging.error(e)
                    connection.commit()
                connection.close()



if __name__ == '__main__':
    update_link_features_sem_similarity()
    #build_article_features_table()
    #insert_article_features()
    #alter_article_features_table()
    #update_article_features()





