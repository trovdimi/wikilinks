from wsd.database import MySQLDatabase
from graph_tool.all import *
from conf import *
import logging
import MySQLdb
import cPickle as pickle
from scipy.stats.stats import pearsonr,spearmanr,kendalltau
import cPickle as pickle
import numpy as np
import pandas as pd
from scipy.sparse import sparsetools
from joblib import Parallel, delayed



from scipy.sparse import csr_matrix
from scipy.sparse.sparsetools import csr_scale_rows

def read_pickle(fpath):
    with open(fpath, 'rb') as infile:
        obj = pickle.load(infile)
    return obj


def write_pickle(fpath, obj):
    with open(fpath, 'wb') as outfile:
        pickle.dump(obj, outfile, -1)

def weighted_pagerank():
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    conn = db._create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT source_article_id, target_article_id, occ FROM link_occurences;')
    result = cursor.fetchall()
    wikipedia = Graph()
    eprop = wikipedia.new_edge_property("int")

    for link in result:
        e = wikipedia.add_edge(link[0], link[1])
        eprop[e] = link[2]
    # filter all nodes that have no edges
    wikipedia = GraphView(wikipedia, vfilt=lambda v : v.out_degree()+v.in_degree()>0 )


    print "page_rank_weighted"
    for damping in [0.8, 0.85, 0.9 ,0.95]:
        print damping
        key = "page_rank_weighted"+str(damping)
        wikipedia.vertex_properties[key] = pagerank(wikipedia, weight=eprop,damping=damping)

    print "page_rank"
    for damping in [0.8, 0.85, 0.9 ,0.95]:
        print damping
        key = "page_rank"+str(damping)
        wikipedia.vertex_properties[key] = pagerank(wikipedia, damping=damping)




    wikipedia.save("output/weightedpagerank/wikipedianetwork_link_occ.xml.gz")
    print 'link_occ done'


    cursor.execute('SELECT source_article_id, target_article_id, sim FROM semantic_similarity group by '
                   'source_article_id, target_article_id;')
    result = cursor.fetchall()
    wikipedia = Graph()
    eprop = wikipedia.new_edge_property("double")

    for link in result:
        e = wikipedia.add_edge(link[0], link[1])
        eprop[e] = link[2]
    # filter all nodes that have no edges
    print 'filter nodes graph tool specific code'
    wikipedia = GraphView(wikipedia, vfilt=lambda v : v.out_degree()+v.in_degree()>0 )


    print "page_rank_weighted"
    for damping in [0.8, 0.85, 0.9 ,0.95]:
        print damping
        key = "page_rank_weighted"+str(damping)
        wikipedia.vertex_properties[key] = pagerank(wikipedia, weight=eprop,damping=damping)

    print "page_rank"
    for damping in [0.8, 0.85, 0.9 ,0.95]:
        print damping
        key = "page_rank"+str(damping)
        wikipedia.vertex_properties[key] = pagerank(wikipedia, damping=damping)


    wikipedia.save("output/weightedpagerank/wikipedianetwork_sem_sim_distinct_links.xml.gz")
    print 'sem sim distrinct links done'

    cursor.execute('SELECT source_article_id, target_article_id, sim FROM semantic_similarity;')
    result = cursor.fetchall()
    wikipedia = Graph()
    eprop = wikipedia.new_edge_property("double")

    for link in result:
        e = wikipedia.add_edge(link[0], link[1])
        eprop[e] = link[2]
    # filter all nodes that have no edges
    wikipedia = GraphView(wikipedia, vfilt=lambda v : v.out_degree()+v.in_degree()>0 )


    print "page_rank_weighted"
    for damping in [0.8, 0.85, 0.9 ,0.95]:
        print damping
        key = "page_rank_weighted"+str(damping)
        wikipedia.vertex_properties[key] = pagerank(wikipedia, weight=eprop,damping=damping)

    print "page_rank"
    for damping in [0.8, 0.85, 0.9 ,0.95]:
        print damping
        key = "page_rank"+str(damping)
        wikipedia.vertex_properties[key] = pagerank(wikipedia, damping=damping)

    wikipedia.save("output/weightedpagerank/wikipedianetwork_sem_sim.xml.gz")
    print 'sem_sim done'


def norm (hypothesis):
    hypothesis = hypothesis.copy()
    norma = hypothesis.sum(axis=1)
    n_nzeros = np.where(norma > 0)
    n_zeros,_ = np.where(norma == 0)
    norma[n_nzeros] = 1.0 / norma[n_nzeros]
    norma = norma.T[0]
    csr_scale_rows(hypothesis.shape[0], hypothesis.shape[1], hypothesis.indptr, hypothesis.indices, hypothesis.data, norma)
    return hypothesis

def weighted_pagerank_hyp_engineering_struct(labels):

    #read vocab, graph
    graph =  read_pickle(SSD_HOME+"pickle/graph")
    print "loaded graph"
    values =  read_pickle(SSD_HOME+"pickle/values")
    values_kcore = read_pickle(SSD_HOME+"pickle/values_kcore")

    # transform kcore values to model going out of the kcore
    values_kcore = [1./np.sqrt(float(x)) for x in values_kcore]
    print 'kcore values tranfsormation'

    #sem_sim_hyp = read_pickle(SSD_HOME+"pickle/sem_sim_hyp")
    #print "sem_sim_hyp values"

    #lead_hyp = read_pickle(SSD_HOME+"pickle/lead_hyp")
    #infobox_hyp = read_pickle(SSD_HOME+"pickle/infobox_hyp")
    #left_body_hyp = read_pickle(SSD_HOME+"pickle/left-body_hyp")
    #print "gamma values"

    vocab = read_pickle(SSD_HOME+"pickle/vocab")
    print "loaded vocab"

    state_count = len(vocab)
    states = vocab.keys()
    shape = (state_count, state_count)


    hyp_structural = csr_matrix((values, (graph[0], graph[1])),
                                shape=shape, dtype=np.float)


    hyp_kcore = csr_matrix((values_kcore, (graph[0], graph[1])),
                           shape=shape, dtype=np.float)
    print "hyp_kcore"

    del graph
    del values_kcore

    print "after delete"


    #read sem sim form db and create hyp
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    conn = db._create_connection()

    print 'read'
    df = pd.read_sql('select source_article_id, target_article_id, sim from semantic_similarity', conn)
    print 'map sem sim'
    sem_sim_hyp_i = map_to_hyp_indicies(vocab, df['source_article_id'])
    sem_sim_hyp_j = map_to_hyp_indicies(vocab, df['target_article_id'])

    hyp_sem_sim = csr_matrix((df['sim'].values, (sem_sim_hyp_i, sem_sim_hyp_j)),
                             shape=shape, dtype=np.float)
    print 'done map sem sim'
    print hyp_sem_sim.shape
    del sem_sim_hyp_i
    del sem_sim_hyp_j
    del df

    #read vis form csv and create hyp
    lead = pd.read_csv(TMP+'lead.tsv',sep='\t')
    lead_i = map_to_hyp_indicies(vocab, lead['source_article_id'])
    lead_j = map_to_hyp_indicies(vocab, lead['target_article_id'])
    lead_v = np.ones(len(lead_i), dtype=np.float)

    hyp_lead = csr_matrix((lead_v, (lead_i, lead_j)),
                          shape=shape, dtype=np.float)
    print 'done map lead'
    print hyp_lead.shape
    del lead
    del lead_i
    del lead_j
    del lead_v

    infobox = pd.read_csv(TMP+'infobox.tsv',sep='\t')
    infobox_i = map_to_hyp_indicies(vocab, infobox['source_article_id'])
    infobox_j = map_to_hyp_indicies(vocab, infobox['target_article_id'])
    infobox_v = np.ones(len(infobox_i), dtype=np.float)

    hyp_infobox = csr_matrix((infobox_v, (infobox_i, infobox_j)),
                             shape=shape, dtype=np.float)
    print 'done map infobox'
    print hyp_infobox.shape
    del infobox
    del infobox_i
    del infobox_j
    del infobox_v

    left_body = pd.read_csv(TMP+'left-body.tsv',sep='\t')
    left_body_i = map_to_hyp_indicies(vocab, left_body['source_article_id'])
    left_body_j = map_to_hyp_indicies(vocab, left_body['target_article_id'])
    left_body_v = np.ones(len(left_body_i), dtype=np.float)

    hyp_left_body = csr_matrix((left_body_v, (left_body_i, left_body_j)),
                               shape=shape, dtype=np.float)
    print 'done map infobox'
    print hyp_left_body.shape
    del left_body
    del left_body_i
    del left_body_j
    del left_body_v

    #add the visual hyps to one matrix and set all non zero fields to 1.0
    print 'before gamma'
    hyp_gamma = hyp_left_body + hyp_infobox + hyp_lead
    hyp_gamma.data = np.ones_like(hyp_gamma.data, dtype=np.float)
    print 'after gamma'

    del hyp_left_body
    del hyp_infobox
    del hyp_lead

    #norm
    print "in norm each "
    hyp_structural = norm(hyp_structural)
    hyp_kcore = norm(hyp_kcore)
    hyp_sem_sim = norm(hyp_sem_sim)
    hyp_gamma = norm(hyp_gamma)

    #engineering of hypos and norm again

    hyp_mix_semsim_kcore = norm(hyp_structural+hyp_kcore + hyp_sem_sim)
    hyp_mix_semsim_visual = norm(hyp_structural+hyp_sem_sim + hyp_gamma)
    hyp_mix_kcore_visual= norm(hyp_structural+hyp_kcore + hyp_gamma)



    print 'test hypos'


    hypos={}


    hypos['hyp_mix_semsim_kcore']=hyp_mix_semsim_kcore
    hypos['hyp_mix_semsim_visual']=hyp_mix_semsim_visual
    hypos['hyp_mix_kcore_visual']=hyp_mix_kcore_visual



    #load network
    print "weighted page rank engineering"
    wikipedia = load_graph("output/wikipedianetwork.xml.gz")

    #for label, hyp in hypos.iteritems():
    name = '_'.join(labels)
    for label in labels:
        print label
        eprop = create_eprop(wikipedia,  hypos[label], vocab)
        wikipedia.edge_properties[label]=eprop
        #for damping in [0.8, 0.85, 0.9 ,0.95]:
        for damping in [0.8,0.85,0.9]:
            key = label+"_page_rank_weighted_"+str(damping)
            print key
            wikipedia.vertex_properties[key] = pagerank(wikipedia, weight=eprop, damping=damping)
        print 'save network'

        wikipedia.save("output/weightedpagerank/wikipedianetwork_hyp_engineering_strcut_"+name+".xml.gz")

    print 'save network'
    wikipedia.save("output/weightedpagerank/wikipedianetwork_hyp_engineering_strcut_"+name+".xml.gz")
    print 'done'



def weighted_pagerank_hyp_engineering(labels):

    #read vocab, graph
    graph =  read_pickle(SSD_HOME+"pickle/graph")
    print "loaded graph"
    values =  read_pickle(SSD_HOME+"pickle/values")
    values_kcore = read_pickle(SSD_HOME+"pickle/values_kcore")

    # transform kcore values to model going out of the kcore
    values_kcore = [1./np.sqrt(float(x)) for x in values_kcore]
    print 'kcore values tranfsormation'

    #sem_sim_hyp = read_pickle(SSD_HOME+"pickle/sem_sim_hyp")
    #print "sem_sim_hyp values"

    #lead_hyp = read_pickle(SSD_HOME+"pickle/lead_hyp")
    #infobox_hyp = read_pickle(SSD_HOME+"pickle/infobox_hyp")
    #left_body_hyp = read_pickle(SSD_HOME+"pickle/left-body_hyp")
    #print "gamma values"

    vocab = read_pickle(SSD_HOME+"pickle/vocab")
    print "loaded vocab"

    state_count = len(vocab)
    states = vocab.keys()
    shape = (state_count, state_count)


    hyp_structural = csr_matrix((values, (graph[0], graph[1])),
                                shape=shape, dtype=np.float)


    hyp_kcore = csr_matrix((values_kcore, (graph[0], graph[1])),
                           shape=shape, dtype=np.float)
    print "hyp_kcore"

    del graph
    del values_kcore

    print "after delete"


    #read sem sim form db and create hyp
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    conn = db._create_connection()

    print 'read'
    df = pd.read_sql('select source_article_id, target_article_id, sim from semantic_similarity', conn)
    print 'map sem sim'
    sem_sim_hyp_i = map_to_hyp_indicies(vocab, df['source_article_id'])
    sem_sim_hyp_j = map_to_hyp_indicies(vocab, df['target_article_id'])

    hyp_sem_sim = csr_matrix((df['sim'].values, (sem_sim_hyp_i, sem_sim_hyp_j)),
                             shape=shape, dtype=np.float)
    print 'done map sem sim'
    print hyp_sem_sim.shape
    del sem_sim_hyp_i
    del sem_sim_hyp_j
    del df

    #read vis form csv and create hyp
    lead = pd.read_csv(TMP+'lead.tsv',sep='\t')
    lead_i = map_to_hyp_indicies(vocab, lead['source_article_id'])
    lead_j = map_to_hyp_indicies(vocab, lead['target_article_id'])
    lead_v = np.ones(len(lead_i), dtype=np.float)
    
    hyp_lead = csr_matrix((lead_v, (lead_i, lead_j)),
                            shape=shape, dtype=np.float)
    print 'done map lead'
    print hyp_lead.shape
    del lead
    del lead_i
    del lead_j
    del lead_v

    infobox = pd.read_csv(TMP+'infobox.tsv',sep='\t')
    infobox_i = map_to_hyp_indicies(vocab, infobox['source_article_id'])
    infobox_j = map_to_hyp_indicies(vocab, infobox['target_article_id'])
    infobox_v = np.ones(len(infobox_i), dtype=np.float)

    hyp_infobox = csr_matrix((infobox_v, (infobox_i, infobox_j)),
                             shape=shape, dtype=np.float)
    print 'done map infobox'
    print hyp_infobox.shape
    del infobox
    del infobox_i
    del infobox_j
    del infobox_v

    left_body = pd.read_csv(TMP+'left-body.tsv',sep='\t')
    left_body_i = map_to_hyp_indicies(vocab, left_body['source_article_id'])
    left_body_j = map_to_hyp_indicies(vocab, left_body['target_article_id'])
    left_body_v = np.ones(len(left_body_i), dtype=np.float)

    hyp_left_body = csr_matrix((left_body_v, (left_body_i, left_body_j)),
                               shape=shape, dtype=np.float)
    print 'done map infobox'
    print hyp_left_body.shape
    del left_body
    del left_body_i
    del left_body_j
    del left_body_v

    #add the visual hyps to one matrix and set all non zero fields to 1.0
    print 'before gamma'
    hyp_gamma = hyp_left_body + hyp_infobox + hyp_lead
    hyp_gamma.data = np.ones_like(hyp_gamma.data, dtype=np.float)
    print 'after gamma'

    del hyp_left_body
    del hyp_infobox
    del hyp_lead

    #norm
    print "in norm each "
    hyp_structural = norm(hyp_structural)
    hyp_kcore = norm(hyp_kcore)
    hyp_sem_sim = norm(hyp_sem_sim)
    hyp_gamma = norm(hyp_gamma)

    #engineering of hypos and norm again
    hyp_kcore_struct = norm(hyp_structural + hyp_kcore)
    hyp_visual_struct = norm(hyp_structural + hyp_gamma)
    hyp_sem_sim_struct = norm(hyp_structural + hyp_sem_sim)

    hyp_mix_semsim_kcore = norm(hyp_kcore + hyp_sem_sim)
    hyp_mix_semsim_visual = norm(hyp_sem_sim + hyp_gamma)
    hyp_mix_kcore_visual= norm(hyp_kcore + hyp_gamma)


    hyp_all = norm(hyp_kcore + hyp_sem_sim + hyp_gamma)
    hyp_all_struct =  norm(hyp_kcore + hyp_sem_sim + hyp_gamma + hyp_structural)

    hyp_semsim_struct = norm(hyp_structural + hyp_kcore)

    print 'test hypos'


    hypos={}
    hypos['hyp_kcore']=hyp_kcore
    hypos['hyp_sem_sim']=hyp_sem_sim
    hypos['hyp_visual']=hyp_gamma

    hypos['hyp_kcore_struct']=hyp_kcore_struct
    hypos['hyp_visual_struct']=hyp_visual_struct
    hypos['hyp_sem_sim_struct']=hyp_sem_sim_struct

    hypos['hyp_mix_semsim_kcore']=hyp_mix_semsim_kcore
    hypos['hyp_mix_semsim_visual']=hyp_mix_semsim_visual
    hypos['hyp_mix_kcore_visual']=hyp_mix_kcore_visual

    hypos['hyp_all']=hyp_all
    hypos['hyp_all_struct']=hyp_all_struct



    #load network
    print "weighted page rank engineering"
    wikipedia = load_graph("output/wikipedianetwork.xml.gz")

    #for label, hyp in hypos.iteritems():
    name = '_'.join(labels)
    for label in labels:
        print label
        eprop = create_eprop(wikipedia,  hypos[label], vocab)
        wikipedia.edge_properties[label]=eprop
        #for damping in [0.8, 0.85, 0.9 ,0.95]:
        for damping in [0.85]:
            key = label+"_page_rank_weighted_"+str(damping)
            print key
            wikipedia.vertex_properties[key] = pagerank(wikipedia, weight=eprop, damping=damping)
        print 'save network'

        wikipedia.save("output/weightedpagerank/wikipedianetwork_hyp_engineering_"+name+".xml.gz")

    print 'save network'
    wikipedia.save("output/weightedpagerank/wikipedianetwork_hyp_engineering_"+name+".xml.gz")
    print 'done'





def create_eprop(network, hyp, vocab):
    eprop = network.new_edge_property("double")
    i = 0
    for edge in network.edges():
        i+=1
        if i % 100000000==0:
            print i
        src = vocab[str(edge.source())]
        trg = vocab[str(edge.target())]
        eprop[edge] = hyp[src,trg]

    return eprop


def correlations(network_name):
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    conn = db._create_connection()
    cursor = conn.cursor()
    # wikipedia  graph  structural statistics

    results = None
    try:
        results = cursor.execute('select c.curr_id,  sum(c.counts) as counts from clickstream_derived c where c.link_type_derived= %s  group by c.curr_id;', ("internal-link",))
        results = cursor.fetchall()


    except MySQLdb.Error, e:
        print ('error retrieving xy coord for all links links %s (%d)' % (e.args[1], e.args[0]))
    print 'after sql load'


    print 'before load'
    wikipedia = load_graph("output/weightedpagerank/wikipedianetwork_"+network_name+".xml.gz")
    print 'after load'
    cor = {}
    #for kk in ['page_rank', 'page_rank_weighted']:
    for kk in ['page_rank_weighted']:
        correlations_sem_sim_weighted_pagerank ={}
        #for damping in [0.8, 0.85, 0.9 ,0.95]:
        for damping in [0.85]:
            correlations={}
            print damping
            key = kk+str(damping)
            print key
            pagerank = wikipedia.vertex_properties[key]
            counts=[]
            page_rank_values=[]
            for row in results:
                counts.append(float(row[1]))
                page_rank_values.append(pagerank[wikipedia.vertex(int(row[0]))])
            #for index, row in df.iterrows():
            #    counts.append(float(row['counts']))
            #    page_rank_values.append(pagerank[wikipedia.vertex(int(row['target_article_id']))])
            print 'pearson'
            p = pearsonr(page_rank_values, counts)
            print p
            correlations['pearson']=p
            print 'spearmanr'
            s= spearmanr(page_rank_values, counts)
            print s
            correlations['spearmanr']=s
            print 'kendalltau'
            k= kendalltau(page_rank_values, counts)
            print k
            correlations['kendalltau']=k
            correlations_sem_sim_weighted_pagerank[key]=correlations
        cor[kk]=correlations_sem_sim_weighted_pagerank


    write_pickle(HOME+'output/correlations/correlations_pagerank_without_zeros'+network_name+'.obj', cor)


def map_to_hyp_indicies(vocab, l):
    ids = list()
    for v in l.values:
        ids.append(vocab[str(v)])
    return ids

def pickle_correlations_zeros():
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    conn = db._create_connection()

    print 'read'
    df = pd.read_sql('select source_article_id, target_article_id, IFNULL(counts, 0) as counts from link_features group by source_article_id, target_article_id', conn)
    print 'group'
    article_counts = df.groupby(by=["target_article_id"])['counts'].sum().reset_index()
    print 'write to file'
    article_counts[["target_article_id","counts"]].to_csv(TMP+'article_counts.tsv', sep='\t', index=False)


def pickle_correlations_zeros_january():
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    conn = db._create_connection()

    print 'read'
    df = pd.read_sql('select source_article_id, target_article_id from link_features', conn)
    print 'loaded links'
    df2 = pd.read_sql('select prev_id, curr_id, counts from clickstream_derived_en_201501  where link_type_derived= "internal-link";',  conn)
    print 'loaded counts'
    result = pd.merge(df, df2, how='left', left_on = ['source_article_id', 'target_article_id'], right_on = ['prev_id', 'curr_id'])
    print 'merged counts'
    print result
    article_counts = result.groupby(by=["target_article_id"])['counts'].sum().reset_index()
    article_counts['counts'].fillna(0.0, inplace=True)
    print article_counts
    print 'write to file'
    article_counts[["target_article_id","counts"]].to_csv(TMP+'january_article_counts.tsv', sep='\t', index=False)


def correlations_ground_truth():
    print 'ground truth'
    #load network
    wikipedia = load_graph("output/weightedpagerank/wikipedianetwork_hyp_engineering.xml.gz")
    #read counts with zeros
    article_counts  =  pd.read_csv(TMP+'article_counts.tsv', sep='\t')
    cor = {}
    for damping in [0.8,0.9]:
        page_rank = pagerank(wikipedia, damping=damping)
        wikipedia.vertex_properties['page_rank_'+str(damping)] = page_rank
        page_rank_values = list()
        counts = list()
        correlations_values = {}
        for index, row in article_counts.iterrows():
            counts.append(float(row['counts']))
            page_rank_values.append(page_rank[wikipedia.vertex(int(row['target_article_id']))])
        print 'pearson'
        p = pearsonr(page_rank_values, counts)
        print p
        correlations_values['pearson']=p
        print 'spearmanr'
        s = spearmanr(page_rank_values, counts)
        print s
        correlations_values['spearmanr']=s
        print 'kendalltau'
        k = kendalltau(page_rank_values, counts)
        print k
        correlations_values['kendalltau']=k
        cor['page_rank_'+str(damping)]=correlations_values
    write_pickle(HOME+'output/correlations/correlations_pagerank.obj', cor)


def correlations_zeros(labels, consider_zeros=True, clickstream_data='', struct=False):
    #load network
    print struct
    name = '_'.join(labels)
    wikipedia = load_graph("output/weightedpagerank/wikipedianetwork_hyp_engineering_"+name+".xml.gz")
    #read counts with zeros
    if consider_zeros:
        article_counts  =  pd.read_csv(TMP+clickstream_data+'article_counts.tsv', sep='\t')
        print TMP+clickstream_data+'article_counts.tsv'
        correlations_weighted_pagerank = {}
        for label in labels:
            if struct:
                label = label[7:]
            for damping in [0.8,0.85,0.9]:
                key = label+"_page_rank_weighted_"+str(damping)
                pagerank = wikipedia.vertex_properties[key]
                page_rank_values = list()
                counts = list()
                correlations_values = {}
                for index, row in article_counts.iterrows():
                    counts.append(float(row['counts']))
                    page_rank_values.append(pagerank[wikipedia.vertex(int(row['target_article_id']))])
                print 'pearson'
                p = pearsonr(page_rank_values, counts)
                print p
                correlations_values['pearson']=p
                print 'spearmanr'
                s = spearmanr(page_rank_values, counts)
                print s
                correlations_values['spearmanr']=s
                print 'kendalltau'
                k = kendalltau(page_rank_values, counts)
                print k
                correlations_values['kendalltau']=k
                correlations_weighted_pagerank[key]=correlations_values

        write_pickle(HOME+'output/correlations/'+clickstream_data+'correlations_pagerank_'+name+'.obj', correlations_weighted_pagerank)
    else:
        db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
        conn = db._create_connection()
        cursor = conn.cursor()
        # wikipedia  graph  structural statistics

        results = None
        try:
            if clickstream_data != '':

                results = cursor.execute('select c.curr_id,  sum(c.counts) as counts from clickstream_derived c where c.link_type_derived= %s  group by c.curr_id;', ("internal-link",))
                results = cursor.fetchall()
            else:
                results = cursor.execute('select c.curr_id,  sum(c.counts) as counts from clickstream_derived_en_201501 c where c.link_type_derived= %s  group by c.curr_id;', ("internal-link",))
                results = cursor.fetchall()

        except MySQLdb.Error, e:
            print ('error retrieving xy coord for all links links %s (%d)' % (e.args[1], e.args[0]))
        print 'after sql load'


        correlations_weighted_pagerank = {}
        for label in labels:
            if struct:
                label = label[7:]
            for damping in [0.8,0.85,0.9]:
                key = label+"_page_rank_weighted_"+str(damping)
                pagerank = wikipedia.vertex_properties[key]
                correlations={}
                counts=[]
                page_rank_values=[]
                for row in results:
                    counts.append(float(row[1]))
                    page_rank_values.append(pagerank[wikipedia.vertex(int(row[0]))])
                print 'pearson'
                p = pearsonr(page_rank_values, counts)
                print p
                correlations['pearson']=p
                print 'spearmanr'
                s= spearmanr(page_rank_values, counts)
                print s
                correlations['spearmanr']=s
                print 'kendalltau'
                k= kendalltau(page_rank_values, counts)
                print k
                correlations['kendalltau']=k
                correlations_weighted_pagerank[key]=correlations



        write_pickle(HOME+'output/correlations/'+clickstream_data+'correlations_pagerank_without_zeros'+name+'.obj', correlations_weighted_pagerank)



def correlations_weighted_unweighted(labels):
    #load network
    print 'weighted vs unweighted'
    name = '_'.join(labels)
    wikipedia = load_graph("output/weightedpagerank/wikipedianetwork_hyp_engineering_"+name+".xml.gz")
    #read counts with zeros

    wikipedia_u = load_graph("output/weightedpagerank/wikipedianetwork_sem_sim_distinct_links.xml.gz")
    correlations_weighted_pagerank = {}
    for label in labels:
        for damping in [0.8,0.85,0.9]:
            correlations_values={}
            key_weighted = label+"_page_rank_weighted_"+str(damping)
            pagerank_weighted = wikipedia.vertex_properties[key_weighted]
            key_unweighted = "page_rank"+str(damping)
            pagerank_unweighted = wikipedia_u.vertex_properties[key_unweighted]
            print 'pearson'
            p = pearsonr(pagerank_weighted.a, pagerank_unweighted.a)
            print p
            correlations_values['pearson']=p
            print 'spearmanr'
            s = spearmanr(pagerank_weighted.a, pagerank_unweighted.a)
            print s
            correlations_values['spearmanr']=s
            print 'kendalltau'
            k = kendalltau(pagerank_weighted.a, pagerank_unweighted.a)
            print k
            correlations_values['kendalltau']=k
            correlations_weighted_pagerank[label+str(damping)]=correlations_values

    write_pickle(HOME+'output/correlations/correlations_pagerank_weightedvsunweighted'+name+'.obj', correlations_weighted_pagerank)





def damping_factors(networks_list):

    for labels in networks_list:
        name = '_'.join(labels)
        print name
        wikipedia = load_graph("output/weightedpagerank/wikipedianetwork_hyp_engineering_"+name+".xml.gz")
        for label in labels:
            eprop = wikipedia.edge_properties[label]
            for damping in [0.8, 0.9]:
                key = label+"_page_rank_weighted_"+str(damping)
                print key
                wikipedia.vertex_properties[key] = pagerank(wikipedia, weight=eprop, damping=damping)

        wikipedia.save("output/weightedpagerank/wikipedianetwork_hyp_engineering_"+name+".xml.gz")


def wpr():
    #load network
    print "wpr"
    wikipedia = load_graph("output/wikipedianetwork.xml.gz")
    eprop = wikipedia.new_edge_property("double")
    i = 0
    for edge in wikipedia.edges():
        i+=1
        if i % 100000000==0:
            print i
        v = edge.source()
        u = edge.target()
        sum_v_out_neighbors_indegree = sum([node.in_degree() for node in v.out_neighbours()])
        win = float(u.in_degree())/float(sum_v_out_neighbors_indegree)
        sum_v_out_neighbors_out_degree = sum ([node.out_degree() for node in v.out_neighbours()])
        wout =  float(u.out_degree())/float(sum_v_out_neighbors_out_degree)
        eprop[edge] = win*wout
    print "done edge prop"
    wikipedia.edge_properties['wpr']=eprop

    for damping in [0.8, 0.85, 0.9]:
        wikipedia.vertex_properties['wpr'+str(damping)] = pagerank(wikipedia, weight=eprop, damping=damping)
    print 'save network'

    wikipedia.save("output/weightedpagerank/wikipedianetworkwpralg.xml.gz")

    print 'done'



if __name__ == '__main__':

    #Parallel(n_jobs=3, backend="multiprocessing")(delayed(weighted_pagerank_hyp_engineering)(labels) for labels in
    #                                              [['hyp_kcore','hyp_sem_sim','hyp_visual','hyp_kcore_struct'],
    #                                               ['hyp_visual_struct','hyp_mix_semsim_kcore','hyp_mix_semsim_visual'],
    #                                               ['hyp_all','hyp_all_struct','hyp_mix_kcore_visual']])

    #Parallel(n_jobs=3, backend="multiprocessing")(delayed(weighted_pagerank_hyp_engineering_struct)(labels) for labels in
    #                                              [['hyp_mix_semsim_kcore'],
    #                                               ['hyp_mix_semsim_visual'],
    #                                               ['hyp_mix_kcore_visual']])


    #Parallel(n_jobs=1, backend="multiprocessing")(delayed(weighted_pagerank_hyp_engineering)(labels) for labels in
    #                                              [['hyp_sem_sim_struct']])




    #Parallel(n_jobs=4, backend="multiprocessing")(delayed(correlations_zeros)(labels, True) for labels in
    #                                              [['hyp_kcore','hyp_sem_sim','hyp_visual','hyp_kcore_struct'],
    #                                               ['hyp_visual_struct','hyp_mix_semsim_kcore','hyp_mix_semsim_visual'],
    #                                               ['hyp_all','hyp_all_struct','hyp_mix_kcore_visual'],['hyp_sem_sim_struct']])


    Parallel(n_jobs=4, backend="multiprocessing")(delayed(correlations_zeros)(labels,  True, 'january_', False) for labels in
                                                  [['hyp_kcore','hyp_sem_sim','hyp_visual','hyp_kcore_struct'],
                                                   ['hyp_visual_struct','hyp_mix_semsim_kcore','hyp_mix_semsim_visual'],
                                                   ['hyp_all','hyp_all_struct','hyp_mix_kcore_visual'],['hyp_sem_sim_struct']])


    #Parallel(n_jobs=4, backend="multiprocessing")(delayed(correlations_zeros)(labels, False) for labels in
    #                                              [['hyp_kcore','hyp_sem_sim','hyp_visual','hyp_kcore_struct'],
    #                                               ['hyp_visual_struct','hyp_mix_semsim_kcore','hyp_mix_semsim_visual'],
    #                                               ['hyp_all','hyp_all_struct','hyp_mix_kcore_visual'],['hyp_sem_sim_struct']])


    #Parallel(n_jobs=4, backend="multiprocessing")(delayed(correlations_weighted_unweighted)(labels) for labels in
    #                                              [['hyp_kcore','hyp_sem_sim','hyp_visual','hyp_kcore_struct'],
    #                                               ['hyp_visual_struct','hyp_mix_semsim_kcore','hyp_mix_semsim_visual'],
    #                                               ['hyp_all','hyp_all_struct','hyp_mix_kcore_visual'],['hyp_sem_sim_struct']])


    #Parallel(n_jobs=3, backend="multiprocessing")(delayed(correlations_zeros)(labels, True, True) for labels in
    #                                              [['strcut_hyp_mix_semsim_kcore'],
    #                                               ['strcut_hyp_mix_semsim_visual'],
    #                                               ['strcut_hyp_mix_kcore_visual']])

    #wpr()


    #correlations_ground_truth()

    #damping_factors([['hyp_kcore','hyp_sem_sim','hyp_visual','hyp_kcore_struct'],
    #                ['hyp_visual_struct','hyp_mix_semsim_kcore','hyp_mix_semsim_visual'],
    #                ['hyp_all','hyp_all_struct','hyp_mix_kcore_visual'],['hyp_sem_sim_struct']])

    #weigted_pagerank()
    #correlations('sem_sim_distinct_links')
    #correlations('link_occ')
    #correlations('sem_sim')
    #correlations('hyp_engineering')
    #pickle_correlations_zeros()
    #pickle_correlations_zeros_january()

