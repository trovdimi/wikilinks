from __future__ import division
import os
from collections import defaultdict
import cPickle as pickle
from graph_tool.all import *
import logging
import MySQLdb
from wsd.database import MySQLDatabase
from conf import *
import time
from scipy.sparse import csr_matrix
from scipy.special import gammaln
from sklearn.preprocessing import normalize
import numpy as np
import array
import os.path
import multiprocessing
import pandas as pd


from joblib import Parallel, delayed


#we export the data first with this cmds
#mysql -u wikilinks wikilinks -p -e 'SELECT source_article_id, target_article_id, occ FROM wikilinks.link_occurences;' -B > /home/ddimitrov/tmp/wikipedia_network.csv
#mysql -u wikilinks wikilinks -p -e 'SELECT prev_id, curr_id, counts FROM clickstream_derived_internal_links;' -B > /home/ddimitrov/tmp/transitions.csv

#mysql -u wikilinks wikilinks -p -e 'SELECT source_article_id, target_article_id, rel_in_degree  FROM link_features;' -B > /home/ddimitrov/tmp/rel_in_degree.tsv
#mysql -u wikilinks wikilinks -p -e 'SELECT source_article_id, target_article_id, rel_out_degree  FROM link_features;' -B > /home/ddimitrov/tmp/rel_out_degree.tsv
#mysql -u wikilinks wikilinks -p -e 'SELECT source_article_id, target_article_id, rel_degree  FROM link_features;' -B > /home/ddimitrov/tmp/rel_degree.tsv
#mysql -u wikilinks wikilinks -p -e 'SELECT source_article_id, target_article_id, rel_page_rank  FROM link_features;' -B > /home/ddimitrov/tmp/rel_page_rank.tsv
#mysql -u wikilinks wikilinks -p -e 'SELECT source_article_id, target_article_id, rel_local_clust  FROM link_features;' -B > /home/ddimitrov/tmp/rel_local_clust.tsv
#mysql -u wikilinks wikilinks -p -e 'SELECT source_article_id, target_article_id, rel_eigen_centr  FROM link_features;' -B > /home/ddimitrov/tmp/rel_eigen_centr.tsv
#mysql -u wikilinks wikilinks -p -e 'SELECT source_article_id, target_article_id, rel_kcore  FROM link_features;' -B > /home/ddimitrov/tmp/rel_kcore.tsv
#mysql -u wikilinks wikilinks -p -e 'SELECT source_article_id, target_article_id, rel_hits_hub  FROM link_features;' -B > /home/ddimitrov/tmp/rel_hits_hub.tsv
#mysql -u wikilinks wikilinks -p -e 'SELECT source_article_id, target_article_id, rel_hits_authority  FROM link_features;' -B > /home/ddimitrov/tmp/rel_hits_authority.tsv

#mysql -u wikilinks wikilinks -p -e 'SELECT source_article_id, target_article_id, target_position_in_text FROM link_features;' -B > /home/ddimitrov/tmp/links_postions_text.tsv
#mysql -u wikilinks wikilinks -p -e 'SELECT source_article_id, target_article_id, target_x_coord_1920_1080  FROM link_features where target_x_coord_1920_1080 is not Null and target_x_coord_1920_1080!=0;' -B > /home/ddimitrov/tmp/links_postions_x.tsv
#mysql -u wikilinks wikilinks -p -e 'SELECT source_article_id, target_article_id, target_y_coord_1920_1080  FROM link_features where target_y_coord_1920_1080 is not Null  and target_y_coord_1920_1080!=0;' -B > /home/ddimitrov/tmp/links_postions_y.tsv

#mysql -u wikilinks wikilinks -p -e 'SELECT source_article_id, target_article_id, sim  FROM topic_similarity;' -B > /home/ddimitrov/tmp/topic_sim.tsv

def dd():
    return defaultdict(float)

def pickle_inv_voc_linkand_helpers():
    transitions = pickle.load( open( "/ssd/ddimitrov/pickle/transitions", "rb" ) )
    print "loaded transitions"
    graph = pickle.load( open( "/ssd/ddimitrov/pickle/graph", "rb" ) )
    print "loaded graph"
    values = pickle.load( open( "/ssd/ddimitrov/pickle/values", "rb" ) )

    vocab = pickle.load( open( "/ssd/ddimitrov/pickle/vocab", "rb" ) )
    print "loaded vocab"

    state_count = len(vocab)
    states = vocab.keys()
    shape = (state_count, state_count)

    inv_vocab = {v: k for k, v in vocab.items()}

    # structural hypothesis
    hyp_structural = csr_matrix((values, (graph[0], graph[1])),
                                shape=shape, dtype=np.float)
    i_indices = array.array(str("l"))
    j_indices = array.array(str("l"))
    values = array.array(str("d"))

    for s, targets in transitions.iteritems():
        for t, v in targets.iteritems():
            i_indices.append(vocab[s])
            j_indices.append(vocab[t])
            values.append(v)

    i_indices = np.frombuffer(i_indices, dtype=np.int_)
    j_indices = np.frombuffer(j_indices, dtype=np.int_)
    values = np.frombuffer(values, dtype=np.float64)

    transitions = csr_matrix((values, (i_indices, j_indices)),
                             shape=shape)



    #delete all zero rows from all  see  http://stackoverflow.com/questions/31188141/scipy-sparse-matrix-remove-the-rows-whose-all-elements-are-zero
    print transitions.shape
    nonzero_row_indice, _ = transitions.nonzero()
    unique_nonzero_indice = np.unique(nonzero_row_indice)
    transitions = transitions[unique_nonzero_indice]
    print transitions.shape

    hyp_data = csr_matrix(transitions, copy=True)
    print hyp_data.shape

    hyp_structural_red = hyp_structural[unique_nonzero_indice]


    shape_red = hyp_structural_red.shape
    uniqeu_nonzero_map = {v: k for k, v in enumerate(unique_nonzero_indice)}
    value = hyp_structural_red.data
    column_index = hyp_structural_red.indices
    row_pointers = hyp_structural_red.indptr
    print column_index
    print row_pointers
    print value

    Knz = hyp_structural_red.nonzero()
    sparserows = Knz[0]
    sparsecols = Knz[1]
    #The Non-Zero Value of K at each (Row,Col)
    #vals = np.empty(sparserows.shape).astype(np.float)
    #for i in range(len(sparserows)):
    #    vals[i] = hyp_structural_red[sparserows[i],sparsecols[i]]



    ziped_links  = zip(sparserows,sparsecols)
    voc_zip_links = [(inv_vocab[unique_nonzero_indice[link[0]]],inv_vocab[link[1]]) for link in ziped_links]
    pickle.dump(uniqeu_nonzero_map, open("/ssd/ddimitrov/pickle/uniqeu_nonzero_map", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(voc_zip_links, open("/ssd/ddimitrov/pickle/voc_zip_links", "wb"), protocol=pickle.HIGHEST_PROTOCOL)



def pickle_rel(rel_feature):
    i = 0

    #ziped_links = pickle.load( open( "/ssd/ddimitrov/pickle/ziped_links", "rb" ) )
    #print "loaded ziped_links"
    voc_zip_links = pickle.load( open( "/ssd/ddimitrov/pickle/voc_zip_links", "rb" ) )
    print "loaded voc_zip_links"
    uniqeu_nonzero_map = pickle.load( open( "/ssd/ddimitrov/pickle/uniqeu_nonzero_map", "rb" ) )
    vocab = pickle.load( open( "/ssd/ddimitrov/pickle/vocab", "rb" ) )
    print "loaded vocab"

    rel_feature_map = {}
    print rel_feature
    with open(os.path.join(os.path.dirname('__file__'), "/home/ddimitrov/tmp/"+rel_feature+".tsv")) as f:
        next(f)
        for line in f:
            #i += 1
            #if i % 10000 == 0:
            #    print rel_feature, i
            line = line.strip().split('\t')
            rel_feature_map[(line[0],line[1])]=float(line[2])

    print rel_feature


    # print rel_feature
    # values_rel_faeture_positive = list()
    # values_rel_faeture_negative = list()
    # i_indices = list()
    # j_indices = list()
    # with open(os.path.join(os.path.dirname('__file__'), "/home/ddimitrov/tmp/"+rel_feature+".tsv")) as f:
    #    next(f)
    #    for line in f:
    #        i += 1
    #        if i % 10 == 0:
    #            print rel_feature, i
    #        line = line.strip().split('\t')
    #        #rel_feature_map[(line[0],line[1])]=float(line[2])
    #        from_id = line[0]
    #        to_id = line[1]
    #        v = float(line[2])
    #        if (from_id,to_id) in voc_zip_links:
    #            i_indices.append(uniqeu_nonzero_map[vocab[from_id]])
    #            j_indices.append(vocab[to_id])
    #            if v > 0:
    #                values_rel_faeture_positive.append(v)
    #                values_rel_faeture_negative.append(0)
    #            else:
    #                values_rel_faeture_negative.append(v)
    #                values_rel_faeture_positive.append(0)
    # rel_feature_hyp_data = [i_indices, j_indices, values_rel_faeture_positive, values_rel_faeture_negative]
    # pickle.dump(rel_feature_hyp_data, open("/ssd/ddimitrov/pickle/"+rel_feature+"_hyp", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    #start = time.time()


    #degree_result = set(voc_zip_links).intersection(set(rel_degree_map.keys()))
    #rel_degree_map_filtered = {k:rel_degree_map[k] for k in degree_result}
    #i_indices = list()
    #j_indices = list()
    #values_rel_degree = list()
    #for link in voc_zip_links:
    #i_indices.append(uniqeu_nonzero_map[vocab[link[0]]])
    #j_indices.append(vocab[link[1]])
    #    values_rel_degree.append(rel_degree_map_filtered[link])
    #print len(values_rel_degree)
    #print "intersetct"
    #m = (time.time()-start)/60
    #print("--- %d minutes ---" % m)



    values_rel_faeture_positive = list()
    values_rel_faeture_negative = list()
    i_indices_positive = list()
    j_indices_positive = list()
    i_indices_negative = list()
    j_indices_negative = list()

    i = 0
    for link in voc_zip_links:
        i += 1
        if i % 1000000 == 0:
            print rel_feature, i
        rel_value = rel_feature_map[link]
        if rel_value > 0:
            i_indices_positive.append(uniqeu_nonzero_map[vocab[link[0]]])
            j_indices_positive.append(vocab[link[1]])
            values_rel_faeture_positive.append(rel_value)
        else:
            i_indices_negative.append(uniqeu_nonzero_map[vocab[link[0]]])
            j_indices_negative.append(vocab[link[1]])
            values_rel_faeture_negative.append(abs(rel_value))

    positive_rel_feature_hyp_data = [i_indices_positive, j_indices_positive, values_rel_faeture_positive]
    negative_rel_feature_hyp_data = [i_indices_negative, i_indices_negative, values_rel_faeture_negative]
    pickle.dump(positive_rel_feature_hyp_data, open("/ssd/ddimitrov/pickle/positive_"+rel_feature+"_hyp", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(negative_rel_feature_hyp_data, open("/ssd/ddimitrov/pickle/negative_"+rel_feature+"_hyp", "wb"), protocol=pickle.HIGHEST_PROTOCOL)



def pickle_topic_sim():
    i = 0
    print "loading voc_zip_links"
    voc_zip_links = pickle.load( open( "/ssd/ddimitrov/pickle/voc_zip_links", "rb" ) )
    print "loaded voc_zip_links"
    uniqeu_nonzero_map = pickle.load( open( "/ssd/ddimitrov/pickle/uniqeu_nonzero_map", "rb" ) )
    vocab = pickle.load( open( "/ssd/ddimitrov/pickle/vocab", "rb" ) )
    print "loaded vocab"

    rel_feature_map = {}
    print 'topicsim'
    with open(os.path.join(os.path.dirname('__file__'), "/home/ddimitrov/tmp/"+"topic_sim"+".tsv")) as f:
        next(f)
        for line in f:
            #i += 1
            #if i % 1000000 == 0:
            #    print rel_feature, i
            line = line.strip().split('\t')
            rel_feature_map[(line[0],line[1])]=float(line[2])

    print 'topicsim'

    values_rel_faeture = list()
    i_indices = list()
    j_indices = list()
    i = 0
    for link in voc_zip_links:
        i += 1
        if i % 1000000 == 0:
            print 'topicsim', i
        if link in rel_feature_map:
            i_indices.append(uniqeu_nonzero_map[vocab[link[0]]])
            j_indices.append(vocab[link[1]])
            print rel_feature_map[link]
            values_rel_faeture.append(rel_feature_map[link])
    rel_feature_hyp_data = [i_indices, j_indices, values_rel_faeture]
    pickle.dump(rel_feature_hyp_data, open("/ssd/ddimitrov/pickle/topic_sim_hyp", "wb"), protocol=pickle.HIGHEST_PROTOCOL)



def pickle_viz(rel_feature):
    i = 0

    voc_zip_links = pickle.load( open( "/ssd/ddimitrov/pickle/voc_zip_links", "rb" ) )
    print "loaded voc_zip_links"
    uniqeu_nonzero_map = pickle.load( open( "/ssd/ddimitrov/pickle/uniqeu_nonzero_map", "rb" ) )
    vocab = pickle.load( open( "/ssd/ddimitrov/pickle/vocab", "rb" ) )
    print "loaded vocab"

    rel_feature_set = set()
    print rel_feature
    with open(os.path.join(os.path.dirname('__file__'), "/home/ddimitrov/tmp/"+rel_feature+".tsv")) as f:
        next(f)
        for line in f:
            #i += 1
            #if i % 10000 == 0:
            #    print rel_feature, i
            line = line.strip().split('\t')
            rel_feature_set.add((line[0],line[1]))

    print rel_feature

    values_rel_faeture = list()
    i_indices = list()
    j_indices = list()
    i = 0
    for link in voc_zip_links:
        i += 1
        if i % 1000000 == 0:
            print rel_feature, i
        if link in rel_feature_set:
            i_indices.append(uniqeu_nonzero_map[vocab[link[0]]])
            j_indices.append(vocab[link[1]])
            values_rel_faeture.append(1)
    rel_feature_hyp_data = [i_indices, j_indices, values_rel_faeture]
    pickle.dump(rel_feature_hyp_data, open("/ssd/ddimitrov/pickle/"+rel_feature+"_hyp", "wb"), protocol=pickle.HIGHEST_PROTOCOL)


def pickle_viz_matrix_shape():
    # setup logging
    print 'vis matrix shape'
    LOGGING_FORMAT = '%(levelname)s:\t%(asctime)-15s %(message)s'
    LOGGING_PATH = 'tmp/semsim-pickle.log'
    logging.basicConfig(filename=LOGGING_PATH, level=logging.DEBUG, format=LOGGING_FORMAT, filemode='w')
    i = 0
    sem_sim = pickle.load( open( "/ssd/ddimitrov/pickle/sem_sim", "rb" ) )
    print 'semsim loaded'


    lead_feature_set = set()
    print "lead"
    with open(os.path.join(os.path.dirname('__file__'), "/home/ddimitrov/tmp/lead.tsv")) as f:
        next(f)
        for line in f:
            #i += 1
            #if i % 10000 == 0:
            #    print rel_feature, i
            line = line.strip().split('\t')
            lead_feature_set.add((line[0],line[1]))

    infobox_feature_set = set()
    print "infobox"
    with open(os.path.join(os.path.dirname('__file__'), "/home/ddimitrov/tmp/infobox.tsv")) as f:
        next(f)
        for line in f:
            #i += 1
            #if i % 10000 == 0:
            #    print rel_feature, i
            line = line.strip().split('\t')
            infobox_feature_set.add((line[0],line[1]))

    left_body_feature_set = set()
    print "left-body"
    with open(os.path.join(os.path.dirname('__file__'), "/home/ddimitrov/tmp/left-body.tsv")) as f:
        next(f)
        for line in f:
            #i += 1
            #if i % 10000 == 0:
            #    print rel_feature, i
            line = line.strip().split('\t')
            left_body_feature_set.add((line[0],line[1]))


    values_lead = list()
    values_infobox = list()
    values_left_body= list()
    values_sem_sim = list()
    i_indices = list()
    j_indices = list()
    i = 0
    with open(os.path.join(os.path.dirname(__file__), "/home/ddimitrov/tmp/wikipedia_network.csv")) as f:
        next(f)
        for line in f:
            i += 1
            if i % 1000000 == 0:
                print  i
            line = line.strip().split('\t')
            i_indices.append(vocab[line[0]])
            j_indices.append(vocab[line[1]])
            if (line[0],line[1]) in lead_feature_set:
                values_lead.append(1.0)
            else:
                values_lead.append(0.0)
            if (line[0],line[1]) in infobox_feature_set:
                values_infobox.append(1.0)
            else:
                values_infobox.append(0.0)
            if (line[0],line[1]) in left_body_feature_set:
                values_left_body.append(1.0)
            else:
                values_left_body.append(0.0)
            from_id = int(line[0])
            to_id = int(line[1])
            if from_id<=to_id:
                try:
                    values_sem_sim.append(sem_sim[(from_id,to_id)])
                except KeyError as e:
                    logging.error(e)
            else:
                try:
                    values_sem_sim.append(sem_sim[(to_id,from_id)])
                except KeyError as e:
                    logging.error(e)
    rel_feature_hyp_data = [i_indices, j_indices, values_lead, values_infobox,values_left_body, values_sem_sim ]
    pickle.dump(rel_feature_hyp_data, open("/ssd/ddimitrov/pickle/values_lead_infobox_left-body_sem_sim", "wb"), protocol=pickle.HIGHEST_PROTOCOL)


def pickle_viz_positions(rel_feature):
    i = 0

    voc_zip_links = pickle.load( open( "/ssd/ddimitrov/pickle/voc_zip_links", "rb" ) )
    print "loaded voc_zip_links"
    uniqeu_nonzero_map = pickle.load( open( "/ssd/ddimitrov/pickle/uniqeu_nonzero_map", "rb" ) )
    vocab = pickle.load( open( "/ssd/ddimitrov/pickle/vocab", "rb" ) )
    print "loaded vocab"

    rel_feature_map = {}
    print rel_feature
    with open(os.path.join(os.path.dirname('__file__'), "/home/ddimitrov/tmp/"+rel_feature+".tsv")) as f:
        next(f)
        for line in f:
            #i += 1
            #if i % 10000 == 0:
            #    print rel_feature, i
            line = line.strip().split('\t')
            rel_feature_map[(line[0],line[1])]=float(line[2])

    print rel_feature

    values_rel_faeture = list()
    i_indices = list()
    j_indices = list()
    i = 0
    for link in voc_zip_links:
        i += 1
        if i % 1000000 == 0:
            print rel_feature, i
        if link in rel_feature_map:
            #print rel_feature_map[link]
            i_indices.append(uniqeu_nonzero_map[vocab[link[0]]])
            j_indices.append(vocab[link[1]])
            values_rel_faeture.append(rel_feature_map[link])
    rel_feature_hyp_data = [i_indices, j_indices, values_rel_faeture]
    pickle.dump(rel_feature_hyp_data, open("/ssd/ddimitrov/pickle/"+rel_feature+"_hyp", "wb"), protocol=pickle.HIGHEST_PROTOCOL)


def pickle_sim():
    # setup logging
    LOGGING_FORMAT = '%(levelname)s:\t%(asctime)-15s %(message)s'
    LOGGING_PATH = 'tmp/semsim-pickle.log'
    logging.basicConfig(filename=LOGGING_PATH, level=logging.DEBUG, format=LOGGING_FORMAT, filemode='w')
    i = 0
    voc_zip_links = pickle.load( open( "/ssd/ddimitrov/pickle/voc_zip_links", "rb" ) )
    print "loaded voc_zip_links"
    uniqeu_nonzero_map = pickle.load( open( "/ssd/ddimitrov/pickle/uniqeu_nonzero_map", "rb" ) )
    vocab = pickle.load( open( "/ssd/ddimitrov/pickle/vocab", "rb" ) )
    print "loaded vocab"
    sem_sim = pickle.load( open( "/ssd/ddimitrov/pickle/sem_sim", "rb" ) )


    values_rel_faeture = list()
    i_indices = list()
    j_indices = list()
    i = 0
    for link in voc_zip_links:
        i += 1
        if i % 1000000 == 0:
            print  i
        i_indices.append(uniqeu_nonzero_map[vocab[link[0]]])
        j_indices.append(vocab[link[1]])
        from_id = int(link[0])
        to_id = int(link[1])
        if from_id<=to_id:
            try:
                values_rel_faeture.append(sem_sim[(from_id,to_id)])
            except KeyError as e:
                logging.error(e)
        else:
            try:
                values_rel_faeture.append(sem_sim[(to_id,from_id)])
            except KeyError as e:
                logging.error(e)
    rel_feature_hyp_data = [i_indices, j_indices, values_rel_faeture]
    pickle.dump(rel_feature_hyp_data, open("/ssd/ddimitrov/pickle/sem_sim_hyp", "wb"), protocol=pickle.HIGHEST_PROTOCOL)




def pickle_data():
    network = load_graph("output/wikipedianetwork.xml.gz")
    states = set()


    with open(os.path.join(os.path.dirname(__file__), "/home/ddimitrov/tmp/wikipedia_network.csv")) as f:
        next(f)
        for line in f:
            line = line.strip().split('\t')
            states.add(line[0])
            states.add(line[1])
    print "network" + str(len(states))


    wikidata_transitions = defaultdict(dd)
    with open(os.path.join(os.path.dirname(__file__), "/home/ddimitrov/tmp/transitions.csv")) as f:
        next(f)
        for line in f:
            line = line.strip().split('\t')
            #skips transitions that are not in our the network
            if line[0] in states and line[1] in states:
                wikidata_transitions[line[0]][line[1]] = float(line[2])
    pickle.dump(wikidata_transitions, open("/ssd/ddimitrov/pickle/transitions", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    print "wikidata " + str(len(states))


    vocab = dict(((t, i) for i, t in enumerate(states)))
    pickle.dump(vocab, open("/ssd/ddimitrov/pickle/vocab", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    print "vocab"

    i_indices = list()
    j_indices = list()
    values = list()
    values_m = list()
    velues_out_deg = list()
    velues_in_deg = list()
    velues_deg = list()
    values_page_rank = list()
    values_local_clust = list()
    values_kcore = list()
    values_eigenvector_centr= list()
    values_hubs = list()
    values_authority = list()
    with open(os.path.join(os.path.dirname(__file__), "/home/ddimitrov/tmp/wikipedia_network.csv")) as f:
        next(f)
        for line in f:
            line = line.strip().split('\t')
            i_indices.append(vocab[line[0]])
            j_indices.append(vocab[line[1]])
            values.append(1)
            values_m.append(float(line[2]))

            target_vertex = network.vertex(line[1])

            velues_out_deg.append(target_vertex.out_degree())
            velues_in_deg.append(target_vertex.in_degree())
            velues_deg.append(target_vertex.in_degree()+target_vertex.out_degree())
            values_page_rank.append(network.vertex_properties["page_rank"][target_vertex])
            values_local_clust.append(network.vertex_properties["local_clust"][target_vertex])
            values_kcore.append(network.vertex_properties["kcore"][target_vertex])
            values_eigenvector_centr.append(network.vertex_properties["eigenvector_centr"][target_vertex])
            values_hubs.append(network.vertex_properties["hub"][target_vertex])
            values_authority.append(network.vertex_properties["authority"][target_vertex])
    graph = list()
    graph.append(i_indices)
    graph.append(j_indices)
    pickle.dump(graph, open("/ssd/ddimitrov/pickle/graph", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    print "network"

    pickle.dump(values, open("/ssd/ddimitrov/pickle/values", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(values_m, open("/ssd/ddimitrov/pickle/values_m", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(velues_out_deg, open("/ssd/ddimitrov/pickle/velues_out_deg", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(velues_in_deg, open("/ssd/ddimitrov/pickle/velues_in_deg", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(velues_deg, open("/ssd/ddimitrov/pickle/velues_deg", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(values_page_rank, open("/ssd/ddimitrov/pickle/values_page_rank", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(values_local_clust, open("/ssd/ddimitrov/pickle/values_local_clust", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(values_kcore, open("/ssd/ddimitrov/pickle/values_kcore", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(values_eigenvector_centr, open("/ssd/ddimitrov/pickle/values_eigenvector_centr", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(values_hubs, open("/ssd/ddimitrov/pickle/values_hubs", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(values_authority, open("/ssd/ddimitrov/pickle/values_authority", "wb"), protocol=pickle.HIGHEST_PROTOCOL)



def pickle_page_rank_data():
    network = load_graph("output/wikipedianetwork.xml.gz")
    print "after load"
    values_page_rank = list()
    with open(os.path.join(os.path.dirname(__file__), "/home/ddimitrov/tmp/wikipedia_network.csv")) as f:
        print "page"
        next(f)
        for line in f:
            line = line.strip().split('\t')

            target_vertex = network.vertex(line[1])

            values_page_rank.append(network.vertex_properties["page_rank"][target_vertex])

    print "network"

    pickle.dump(values_page_rank, open("/ssd/ddimitrov/pickle/values_page_rank", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    print "done"


def pickle_rel_data():

    #Parallel(n_jobs=9, backend="multiprocessing")(delayed(pickle_rel)(rel_feature) for rel_feature in
    #        ['rel_degree','rel_in_degree','rel_out_degree','rel_page_rank','rel_local_clust','rel_eigen_centr',
    #                    'rel_hits_hub','rel_hits_authority','rel_kcore'])

    Parallel(n_jobs=3, backend="multiprocessing")(delayed(pickle_rel)(rel_feature) for rel_feature in
                                                  ['rel_degree','rel_in_degree','rel_out_degree'])

    #Parallel(n_jobs=3, backend="multiprocessing")(delayed(pickle_rel)(rel_feature) for rel_feature in
    #        ['rel_hits_hub','rel_hits_authority','rel_kcore'])

    #Parallel(n_jobs=3, backend="multiprocessing")(delayed(pickle_rel)(rel_feature) for rel_feature in
    #        ['rel_page_rank','rel_local_clust','rel_eigen_centr'])


def pickle_vis_data():
    pickle_vis_data_pandas()
    Parallel(n_jobs=5, backend="multiprocessing")(delayed(pickle_viz)(rel_feature) for rel_feature in
                                                  ['infobox','lead','left-body','navbox', 'body'])
    #Parallel(n_jobs=3, backend="multiprocessing")(delayed(pickle_viz_positions)(rel_feature) for rel_feature in
    #                                              ['links_postions_text','links_postions_x','links_postions_y'])


def pickle_sem_sim_data():
    # setup logging
    LOGGING_FORMAT = '%(levelname)s:\t%(asctime)-15s %(message)s'
    LOGGING_PATH = 'tmp/semsim-pickle.log'
    logging.basicConfig(filename=LOGGING_PATH, level=logging.DEBUG, format=LOGGING_FORMAT, filemode='w')
    sem_sim = pickle.load( open( "/ssd/ddimitrov/pickle/sem_sim", "rb" ) )

    values_sem_sim=list()
    with open(os.path.join(os.path.dirname(__file__), "/home/ddimitrov/tmp/wikipedia_network.csv")) as f:
        next(f)
        for line in f:
            line = line.strip().split('\t')
            from_id = int(line[0])
            to_id = int(line[1])
            if from_id<=to_id:
                try:
                    value = sem_sim[(from_id,to_id)]
                    values_sem_sim.append(value)
                except KeyError as e:
                    logging.error(e)
            else:
                try:
                    value = sem_sim[(to_id,from_id)]
                    values_sem_sim.append(value)
                except KeyError as e:
                    logging.error(e)


    pickle.dump(values_sem_sim, open("/ssd/ddimitrov/pickle/values_sem_sim", "wb"), protocol=pickle.HIGHEST_PROTOCOL)




def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z

def merge_semsim():
    merge = {}
    for dirname, dirnames, filenames in os.walk("/home/psinger/WikiLinks/data/sem_sim"):
        for file_name in filenames:
            if file_name.endswith(".p"):
                sem_sim = pickle.load( open( "/home/psinger/WikiLinks/data/sem_sim/"+file_name, "rb" ) )
                merge = merge_two_dicts(merge, sem_sim)
                print len(merge)
    pickle.dump(merge, open("/ssd/ddimitrov/pickle/sem_sim", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    print "semsim"

def pickle_visual_data_test():
    links = [(91,92), (93,91), (93,95), (95,92)]
    transitions=[(91,92, 20), (95,92,6)]
    states = set()

    for link in links:
        states.add(link[0])
        states.add(link[1])



    vocab = dict(((t, i) for i, t in enumerate(states)))

    inv_vocab = {v: k for k, v in vocab.items()}

    state_count = len(vocab)
    states = vocab.keys()
    shape = (state_count, state_count)

    i_indices = list()
    j_indices = list()
    values = list()
    for link in links:
        i_indices.append(vocab[link[0]])
        j_indices.append(vocab[link[1]])
        values.append(1)

    hyp_structural = csr_matrix((values, (i_indices, j_indices)),
                                shape=shape, dtype=np.float)



    i_indices = array.array(str("l"))
    j_indices = array.array(str("l"))
    values = array.array(str("d"))

    for transition in transitions:
        i_indices.append(vocab[transition[0]])
        j_indices.append(vocab[transition[1]])
        values.append(transition[2])

    i_indices = np.frombuffer(i_indices, dtype=np.int_)
    j_indices = np.frombuffer(j_indices, dtype=np.int_)
    values = np.frombuffer(values, dtype=np.float64)

    hyp_data = csr_matrix((values, (i_indices, j_indices)),
                             shape=shape)

    nonzero_row_indice, _ = hyp_data.nonzero()
    unique_nonzero_indice = np.unique(nonzero_row_indice)
    hyp_data_red = hyp_data[unique_nonzero_indice]

    hyp_structural_red = hyp_structural[unique_nonzero_indice]
    shape_red = hyp_structural_red.shape
    uniqeu_nonzero_map = {v: k for k, v in enumerate(unique_nonzero_indice)}
    value = hyp_structural_red.data
    column_index = hyp_structural_red.indices
    row_pointers = hyp_structural_red.indptr
    print column_index
    print row_pointers
    print value

    Knz = hyp_structural_red.nonzero()
    sparserows = Knz[0]
    sparsecols = Knz[1]
    #The Non-Zero Value of K at each (Row,Col)
    vals = np.empty(sparserows.shape).astype(np.float)
    for i in range(len(sparserows)):
        vals[i] = hyp_structural_red[sparserows[i],sparsecols[i]]

    ziped_links  = zip(sparserows,sparsecols)


    voc_zip_links = [(inv_vocab[unique_nonzero_indice[link[0]]],inv_vocab[link[1]]) for link in ziped_links]
    print voc_zip_links
    print links

    i_indices = list()
    j_indices = list()
    values = list()
    for link in voc_zip_links:
        i_indices.append(uniqeu_nonzero_map[vocab[link[0]]])
        j_indices.append(vocab[link[1]])
        values.append(1)

    hyp_structural_d = csr_matrix((values, (i_indices, j_indices)),
                                shape=shape_red, dtype=np.float)

def pickle_transitions_matrix_data():
    transitions = pickle.load( open( "/ssd/ddimitrov/pickle/transitions", "rb" ) )
    vocab = pickle.load( open( "/ssd/ddimitrov/pickle/vocab", "rb" ) )

    i_indices = array.array(str("l"))
    j_indices = array.array(str("l"))
    values = array.array(str("d"))

    for s, targets in transitions.iteritems():
        for t, v in targets.iteritems():
            i_indices.append(vocab[s])
            j_indices.append(vocab[t])
            values.append(v)

    i_indices = np.frombuffer(i_indices, dtype=np.int_)
    j_indices = np.frombuffer(j_indices, dtype=np.int_)
    values = np.frombuffer(values, dtype=np.float64)
    transition_matrix=[i_indices,j_indices,values]
    pickle.dump(transition_matrix, open("/ssd/ddimitrov/pickle/transition_matrix", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    print "transition_matrix"



def pickle_vis_data_pandas():
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    conn = db._create_connection()


    df = pd.read_sql('select source_article_id, target_article_id, target_y_coord_1920_1080, target_x_coord_1920_1080, visual_region from link_features', conn)
    print len(df)

    no_dup = df.sort(['source_article_id','target_y_coord_1920_1080','target_x_coord_1920_1080']).groupby(["source_article_id", "target_article_id"]).first()
    print len(no_dup)

    feature = no_dup.loc[no_dup['visual_region']=='lead']
    print len(feature)
    feature.reset_index(inplace=True)


    feature = no_dup.loc[no_dup['visual_region']=='infobox']
    print len(feature)
    feature.reset_index(inplace=True)
    feature[['source_article_id','target_article_id']].to_csv('/home/ddimitrov/tmp/infobox.tsv', sep='\t', index=False)

    feature = no_dup.loc[no_dup['visual_region']=='navbox']
    print len(feature)
    feature.reset_index(inplace=True)
    feature[['source_article_id','target_article_id']].to_csv('/home/ddimitrov/tmp/navbox.tsv', sep='\t', index=False)

    feature = no_dup.loc[no_dup['visual_region']=='left-body']
    print len(feature)
    feature.reset_index(inplace=True)
    feature[['source_article_id','target_article_id']].to_csv('/home/ddimitrov/tmp/left-body.tsv', sep='\t',index=False)

    feature = no_dup.loc[no_dup['visual_region']=='body']
    print len(feature)
    feature.reset_index(inplace=True)
    feature[['source_article_id','target_article_id']].to_csv('/home/ddimitrov/tmp/body.tsv', sep='\t',index=False)




if __name__ == '__main__':
    #pickle_data()
    #merge_semsim()
    #pickle_sem_sim_data()
    #pickle_visual_data()
    #pickle_inv_voc_linkand_helpers()
    #pickle_rel_data()
    #pickle_topic_sim()
    #pickle_vis_data()
    #pickle_page_rank_data()
    #pickle_sim()
    #pickle_transitions_matrix_data()
    pickle_viz_matrix_shape()