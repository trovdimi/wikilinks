import matplotlib.pyplot as plt
from HypTrails import HypTrails
import cPickle
import pickle_data
import itertools
from scipy.sparse import csr_matrix
from scipy.special import gammaln
from collections import defaultdict
from sklearn.preprocessing import normalize
import numpy as np
import os
import array
from graph_tool.all import *
from scipy.sparse.sparsetools import csr_scale_rows
import operator
from conf import *


from matplotlib import style
style.use('acm-2col-bmh')

import pylab
params = {
    'font.family' : 'serif',
    'font.serif' : ['Times New Roman'],
    'font.size' : 7
}
pylab.rcParams.update(params)



def dd():
    return defaultdict(float)

def compare_vusual(additive, inverted):
    #read vocab, graph, transitions
    transition_matrix = cPickle.load( open( SSD_HOME+"pickle/transition_matrix", "rb" ) )
    print "loaded transitions"
    graph = cPickle.load( open( SSD_HOME+"pickle/graph", "rb" ) )
    print "loaded graph"
    values = cPickle.load( open( SSD_HOME+"pickle/values", "rb" ) )
    print "loaded values"


    lead_hyp = cPickle.load( open( SSD_HOME+"pickle/lead_hyp", "rb" ) )
    infobox_hyp = cPickle.load( open( SSD_HOME+"pickle/infobox_hyp", "rb" ) )
    navbox_hyp = cPickle.load( open( SSD_HOME+"pickle/navbox_hyp", "rb" ) )
    left_body_hyp = cPickle.load( open( SSD_HOME+"pickle/left-body_hyp", "rb" ) )
    body_hyp = cPickle.load( open( SSD_HOME+"pickle/body_hyp", "rb" ) )
    links_postions_text_hyp = cPickle.load( open( SSD_HOME+"pickle/links_postions_text_hyp", "rb" ) )
    links_postions_x_hyp = cPickle.load( open( SSD_HOME+"pickle/links_postions_x_hyp", "rb" ) )
    links_postions_y_hyp = cPickle.load( open( SSD_HOME+"pickle/links_postions_y_hyp", "rb" ) )


    if inverted:
        lead_hyp[2] = [1.0/x if x >0 else 0 for x in lead_hyp[2]]
        infobox_hyp[2] = [1.0/x if x >0 else 0 for x in infobox_hyp[2]]
        navbox_hyp[2] = [1.0/x if x >0 else 0 for x in navbox_hyp[2]]
        left_body_hyp[2] = [1.0/x if x >0 else 0 for x in left_body_hyp[2]]
        body_hyp[2] = [1.0/x if x >0 else 0 for x in body_hyp[2]]
        links_postions_text_hyp[2] = [1.0/x if x >0 else 0 for x in links_postions_text_hyp[2]]
        links_postions_x_hyp[2] = [1.0/x if x >0 else 0 for x in links_postions_x_hyp[2]]
        links_postions_y_hyp[2] = [1.0/x if x >0 else 0 for x in links_postions_y_hyp[2]]



    vocab = cPickle.load( open( SSD_HOME+"pickle/vocab", "rb" ) )
    print "loaded vocab"



    state_count = len(vocab)
    states = vocab.keys()
    shape = (state_count, state_count)

    # we can use an empty matrix here as the HypTrails class then
    # properly distributes the chips for elicitation
    hyp_uniform = csr_matrix((state_count,state_count))



    # structural hypothesis
    hyp_structural = csr_matrix((values, (graph[0], graph[1])),
                                shape=shape, dtype=np.float)




    del graph

    # i_indices = array.array(str("l"))
    # j_indices = array.array(str("l"))
    # values = array.array(str("d"))
    #
    # for s, targets in transitions.iteritems():
    #     for t, v in targets.iteritems():
    #         i_indices.append(vocab[s])
    #         j_indices.append(vocab[t])
    #         values.append(v)
    #
    # i_indices = np.frombuffer(i_indices, dtype=np.int_)
    # j_indices = np.frombuffer(j_indices, dtype=np.int_)
    # values = np.frombuffer(values, dtype=np.float64)
    #
    # transitions = csr_matrix((values, (i_indices, j_indices)),
    #                          shape=shape)

    transitions = csr_matrix((transition_matrix[2], (transition_matrix[0], transition_matrix[1])),
                             shape=shape)

    del transition_matrix



    #delete all zero rows from all  see  http://stackoverflow.com/questions/31188141/scipy-sparse-matrix-remove-the-rows-whose-all-elements-are-zero
    print transitions.shape
    nonzero_row_indice, _ = transitions.nonzero()
    unique_nonzero_indice = np.unique(nonzero_row_indice)
    transitions = transitions[unique_nonzero_indice]
    print transitions.shape

    hyp_structural = hyp_structural[unique_nonzero_indice]
    print hyp_structural.shape
    Knz = hyp_structural.nonzero()
    sparserows = Knz[0]
    sparsecols = Knz[1]
    print len(sparserows)
    print len(sparserows)

    hyp_uniform = hyp_uniform[unique_nonzero_indice]
    print hyp_uniform.shape

    hyp_data = csr_matrix(transitions, copy=True)
    print hyp_data.shape


    hyp_lead = csr_matrix((lead_hyp[2], (lead_hyp[0], lead_hyp[1])),
                          shape=hyp_data.shape, dtype=np.float)
    print hyp_lead.shape
    Knz = hyp_lead.nonzero()
    sparserows = Knz[0]
    sparsecols = Knz[1]
    print len(sparserows)
    print len(sparserows)

    hyp_infobox = csr_matrix((infobox_hyp[2], (infobox_hyp[0], infobox_hyp[1])),
                          shape=hyp_data.shape, dtype=np.float)
    print hyp_infobox.shape
    Knz = hyp_infobox.nonzero()
    sparserows = Knz[0]
    sparsecols = Knz[1]
    print len(sparserows)
    print len(sparserows)

    hyp_navbox = csr_matrix((navbox_hyp[2], (navbox_hyp[0], navbox_hyp[1])),
                             shape=hyp_data.shape, dtype=np.float)
    print hyp_navbox.shape
    Knz = hyp_navbox.nonzero()
    sparserows = Knz[0]
    sparsecols = Knz[1]
    print len(sparserows)
    print len(sparserows)

    hyp_left_body = csr_matrix((left_body_hyp[2], (left_body_hyp[0], left_body_hyp[1])),
                            shape=hyp_data.shape, dtype=np.float)
    print hyp_left_body.shape
    Knz = hyp_left_body.nonzero()
    sparserows = Knz[0]
    sparsecols = Knz[1]
    print len(sparserows)
    print len(sparserows)

    hyp_body = csr_matrix((body_hyp[2], (body_hyp[0], body_hyp[1])),
                               shape=hyp_data.shape, dtype=np.float)
    print hyp_body.shape
    Knz = hyp_body.nonzero()
    sparserows = Knz[0]
    sparsecols = Knz[1]
    print len(sparserows)
    print len(sparserows)

    hyp_links_postions_text = csr_matrix((links_postions_text_hyp[2], (links_postions_text_hyp[0], links_postions_text_hyp[1])),
                          shape=hyp_data.shape, dtype=np.float)

    hyp_links_postions_x = csr_matrix((links_postions_x_hyp[2], (links_postions_x_hyp[0], links_postions_x_hyp[1])),
                                         shape=hyp_data.shape, dtype=np.float)

    hyp_links_postions_y = csr_matrix((links_postions_y_hyp[2], (links_postions_y_hyp[0], links_postions_y_hyp[1])),
                                      shape=hyp_data.shape, dtype=np.float)

    del left_body_hyp
    del navbox_hyp
    del infobox_hyp
    del lead_hyp
    del body_hyp
    del links_postions_text_hyp
    del links_postions_x_hyp
    del links_postions_y_hyp

    ht = HypTrails(vocab)
    ht.fit(transitions)
    print "after fit"

    fig = plt.figure()
    ax = fig.add_subplot(111)

    r_first = 0.0001
    r = np.logspace(np.log10(r_first), np.log10(10000), 6)

    evidences_dict = {}
    evidences_dict['r'] = r
    evidences_dict['r_first'] = r_first

    #norm
    print "in norm each "
    hyp_structural = norm_hyp(hyp_structural)
    hyp_lead = norm_hyp(hyp_lead)
    hyp_infobox = norm_hyp(hyp_infobox)
    hyp_navbox = norm_hyp(hyp_navbox)
    hyp_left_body = norm_hyp(hyp_left_body)
    hyp_body = norm_hyp(hyp_body)
    hyp_links_postions_text = norm_hyp(hyp_links_postions_text)
    hyp_links_postions_x = norm_hyp(hyp_links_postions_x)
    hyp_links_postions_y = norm_hyp(hyp_links_postions_y)

    # uniform hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_uniform, hyp_structural, k=i, norm=True ))
    ax.plot(r, evidences, marker='o', clip_on = False, label="uniform", color='#FF3333', linestyle='--')
    print "uniform done"
    print evidences
    evidences_dict['uniform']=evidences

    # structural hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_structural,hyp_structural,k=i, norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="structural", color='#FF8D33', linestyle='--')
    print "structural done"
    print evidences
    evidences_dict['structural']=evidences

    # data hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_data,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="data", color='#A8FF33', linestyle='--')
    print "data done"
    print evidences
    evidences_dict['data']=evidences

    if additive == True:
        hyp_lead = hyp_lead + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_lead,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="lead",  color='#137117',linestyle='--')
    print "lead done"
    print evidences
    evidences_dict['lead']=evidences

    if additive == True:
        hyp_infobox = hyp_infobox + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_infobox,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="infobox", color='#711360', linestyle='--')
    print "infobox done"
    print evidences
    evidences_dict['infobox']=evidences

    if additive == True:
        hyp_navbox = hyp_navbox + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_navbox,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="navbox", color='#491371', linestyle='--')
    print "navbox done"
    print evidences
    evidences_dict['navbox']=evidences

    if additive == True:
        hyp_left_body = hyp_left_body + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_left_body,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="left body", color='#136871', linestyle='--')
    print "left-body done"
    print evidences
    evidences_dict['left-body']=evidences

    if additive == True:
        hyp_body = hyp_body + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_body,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="body", color='#132071', linestyle='--')
    print "body done"
    print evidences
    evidences_dict['body']=evidences



    if additive == True:
        hyp_links_postions_text = hyp_links_postions_text + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_links_postions_text,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="postions text", color='#3358FF', linestyle='--')
    print "postions text done"
    print evidences
    evidences_dict['postions text']=evidences

    if additive == True:
        hyp_links_postions_x = hyp_links_postions_x + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_links_postions_x,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="postions x coord", color='#7133FF', linestyle='--')
    print "postions x coord done"
    print evidences
    evidences_dict['postions x coord']=evidences

    if additive == True:
        hyp_links_postions_y = hyp_links_postions_y + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_links_postions_y,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="postions y coord", color='#FEC380', linestyle='--')
    print "postions y coord done"
    print evidences
    evidences_dict['postions y coord']=evidences

    # further plotting
    ax.set_xlabel("hypothesis weighting factor k")
    ax.set_ylabel("marginal likelihood / evidence (log)")
    # if we use log space for k then we need to set x also to log and improve the labels
    ax.set_xscale("log")

    plt.grid(False)
    ax.xaxis.grid(True)
    handles, labels = ax.get_legend_handles_labels()
    lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,-0.1), ncol=4)

    if additive == False:
        if inverted:
            plt.savefig('output/compare_visual_inverted_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_visual_inverted_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)
        else:
            plt.savefig('output/compare_visual_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/visual_evidences.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)

    else:
        if inverted:
            plt.savefig('output/compare_visual_additive_inverted_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_visual_additive_inverted_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)
        else:
            plt.savefig('output/compare_visual_additive_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_visual_additive_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)

    print "visual_evidences"


def compare_structural(additive, inverted):
    print 'additve'
    print additive
    print 'inverted'
    print inverted
    #read vocab, graph, transitions
    #transitions = cPickle.load( open( SSD_HOME+"pickle/transitions", "rb" ) )
    transition_matrix = cPickle.load( open( SSD_HOME+"pickle/transition_matrix", "rb" ) )
    print "loaded transitions"
    graph = cPickle.load( open( SSD_HOME+"pickle/graph", "rb" ) )
    print "loaded graph"
    values = cPickle.load( open( SSD_HOME+"pickle/values", "rb" ) )
    values_m = cPickle.load( open( SSD_HOME+"pickle/values_m", "rb" ) )
    velues_out_deg = cPickle.load( open( SSD_HOME+"pickle/velues_out_deg", "rb" ) )
    velues_in_deg = cPickle.load( open( SSD_HOME+"pickle/velues_in_deg", "rb" ) )
    velues_deg = cPickle.load( open( SSD_HOME+"pickle/velues_deg", "rb" ) )
    #values_page_rank = cPickle.load( open( SSD_HOME+"pickle/values_page_rank", "rb" ) )
    values_local_clust = cPickle.load( open( SSD_HOME+"pickle/values_local_clust", "rb" ) )
    values_kcore = cPickle.load( open( SSD_HOME+"pickle/values_kcore", "rb" ) )
    values_eigenvector_centr = cPickle.load( open( SSD_HOME+"pickle/values_eigenvector_centr", "rb" ) )
    values_hubs = cPickle.load( open( SSD_HOME+"pickle/values_hubs", "rb" ) )
    values_authority = cPickle.load( open( SSD_HOME+"pickle/values_authority", "rb" ) )

    if inverted:
        values_m = [1.0/x if x >0 else 0 for x in values_m]
        velues_out_deg = [1.0/x if x >0 else 0 for x in velues_out_deg]
        velues_in_deg = [1.0/x if x >0 else 0 for x in velues_in_deg]
        velues_deg = [1.0/x if x >0 else 0 for x in velues_deg]
        #values_page_rank = [1.0/x if x >0 else 0 for x in values_page_rank]
        values_local_clust = [1.0/x if x >0 else 0 for x in values_local_clust]
        values_kcore = [1.0/x if x >0 else 0 for x in values_kcore]
        values_eigenvector_centr = [1.0/x if x >0 else 0 for x in values_eigenvector_centr]
        values_hubs = [1.0/x if x >0 else 0 for x in values_hubs]
        values_authority = [1.0/x if x >0 else 0 for x in values_authority]


    vocab = cPickle.load( open( SSD_HOME+"pickle/vocab", "rb" ) )
    print "loaded vocab"

    state_count = len(vocab)
    states = vocab.keys()
    shape = (state_count, state_count)

    # we can use an empty matrix here as the HypTrails class then
    # properly distributes the chips for elicitation
    hyp_uniform = csr_matrix((state_count,state_count))
    print "hyp uniform"


    # structural hypothesises
    hyp_structural = csr_matrix((values, (graph[0], graph[1])),
                                shape=shape, dtype=np.float)
    print "hyp_structural_m"


    hyp_structural_m = csr_matrix((values_m, (graph[0], graph[1])),
                                  shape=shape, dtype=np.float)
    print "hyp_structural_m"

    hyp_out_degree = csr_matrix((velues_out_deg, (graph[0], graph[1])),
                                shape=shape, dtype=np.float)
    print "hyp_out_degree"

    hyp_in_degree = csr_matrix((velues_in_deg, (graph[0], graph[1])),
                               shape=shape, dtype=np.float)
    print "hyp_in_degree"

    hyp_degree = csr_matrix((velues_deg, (graph[0], graph[1])),
                            shape=shape, dtype=np.float)
    print "hyp_degree"

    #hyp_page_rank = csr_matrix((values_page_rank, (graph[0], graph[1])),
    #                           shape=shape, dtype=np.float)
    print "hyp_page_rank"

    hyp_local_clust = csr_matrix((values_local_clust, (graph[0], graph[1])),
                                 shape=shape, dtype=np.float)
    print "hyp_local_clust"

    hyp_kcore = csr_matrix((values_kcore, (graph[0], graph[1])),
                           shape=shape, dtype=np.float)
    print "hyp_kcore"

    hyp_eigenvector_centr = csr_matrix((values_eigenvector_centr, (graph[0], graph[1])),
                                       shape=shape, dtype=np.float)
    print "hyp_eigenvector_centr"

    hyp_hubs = csr_matrix((values_hubs, (graph[0], graph[1])),
                          shape=shape, dtype=np.float)
    print "hyp_authority"

    hyp_authority = csr_matrix((values_authority, (graph[0], graph[1])),
                               shape=shape, dtype=np.float)
    print "hyp_authority"

    del graph
    del values_m
    del velues_out_deg
    del velues_in_deg
    del velues_deg
    #del values_page_rank
    del values_local_clust
    del values_kcore
    del values_eigenvector_centr
    del values_hubs
    del values_authority

    print "after delete"

    transitions = csr_matrix((transition_matrix[2], (transition_matrix[0], transition_matrix[1])),
                             shape=shape)
    print "transitions"

    del transition_matrix
    print " delete transitions"

    #delete all zero rows from all  see  http://stackoverflow.com/questions/31188141/scipy-sparse-matrix-remove-the-rows-whose-all-elements-are-zero
    print transitions.shape
    nonzero_row_indice, _ = transitions.nonzero()
    unique_nonzero_indice = np.unique(nonzero_row_indice)
    transitions = transitions[unique_nonzero_indice]
    print transitions.shape

    hyp_data = csr_matrix(transitions, copy=True)
    print hyp_data.shape

    hyp_structural = hyp_structural[unique_nonzero_indice]

    hyp_uniform = hyp_uniform[unique_nonzero_indice]

    hyp_structural_m = hyp_structural_m[unique_nonzero_indice]

    hyp_out_degree = hyp_out_degree[unique_nonzero_indice]

    hyp_in_degree = hyp_in_degree[unique_nonzero_indice]

    hyp_degree = hyp_degree[unique_nonzero_indice]

    #hyp_page_rank = hyp_page_rank[unique_nonzero_indice]

    hyp_local_clust = hyp_local_clust[unique_nonzero_indice]

    hyp_kcore = hyp_kcore[unique_nonzero_indice]

    hyp_eigenvector_centr = hyp_eigenvector_centr[unique_nonzero_indice]

    hyp_hubs= hyp_hubs[unique_nonzero_indice]

    hyp_authority = hyp_authority[unique_nonzero_indice]


    ht = HypTrails(vocab)
    ht.fit(transitions)
    print "after fit"

    fig = plt.figure()
    ax = fig.add_subplot(111)

    r_first = 0.0001
    r = np.logspace(np.log10(r_first), np.log10(10000), 6)

    evidences_dict = {}
    evidences_dict['r'] = r
    evidences_dict['r_first'] = r_first

    #norm
    print "in norm each "
    hyp_structural = norm_hyp(hyp_structural)
    hyp_structural_m = norm_hyp(hyp_structural_m)
    hyp_out_degree = norm_hyp(hyp_out_degree)
    hyp_in_degree = norm_hyp(hyp_in_degree)
    hyp_degree = norm_hyp(hyp_degree)
    #hyp_page_rank = norm_hyp(hyp_page_rank)
    hyp_local_clust = norm_hyp(hyp_local_clust)
    hyp_kcore = norm_hyp(hyp_kcore)
    hyp_eigenvector_centr = norm_hyp(hyp_eigenvector_centr)
    hyp_hubs = norm_hyp(hyp_hubs)
    hyp_authority = norm_hyp(hyp_authority)

    #add the normed
    if additive:
        print "in additive"
        hyp_structural_m = hyp_structural + hyp_structural_m
        hyp_out_degree = hyp_structural + hyp_out_degree
        hyp_in_degree = hyp_structural + hyp_in_degree
        hyp_degree = hyp_structural + hyp_degree
        #hyp_page_rank = hyp_structural + hyp_page_rank
        hyp_local_clust = hyp_structural + hyp_local_clust
        hyp_kcore = hyp_structural + hyp_kcore
        hyp_eigenvector_centr = hyp_structural + hyp_eigenvector_centr
        hyp_hubs = hyp_structural + hyp_hubs
        hyp_authority = hyp_structural + hyp_authority



    # uniform hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_uniform,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="uniform", color='#FF3333', linestyle='--')
    print "uniform done"
    evidences_dict['uniform'] = evidences

    # structural hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_structural,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="structural", color='#FF8D33', linestyle='--')
    print "structural done"
    evidences_dict['structural'] = evidences

    # data hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_data,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="data", color='#A8FF33', linestyle='--')
    print "data done"
    evidences_dict['data'] = evidences

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_structural_m,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="link occ.",  color='#33FF36', linestyle='--')
    print "structural_m done"
    evidences_dict['link occ.'] = evidences

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_out_degree,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="out-degree",  color='#33FF96', linestyle='--')
    print "out degree done"
    evidences_dict['out degree'] = evidences


    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_in_degree,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="in-degree", color='#33FFE0', linestyle='--')
    print "in degree done"
    evidences_dict['in degree'] = evidences

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_degree,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="degree", color='#33F3FF', linestyle='--')
    print "degree done"
    evidences_dict['degree'] = evidences

    # evidences = []
    # for i in r:
    #     if i == r_first:
    #         evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
    #     else:
    #         evidences.append(ht.evidence(hyp_page_rank,hyp_structural,k=i,norm=True))
    # ax.plot(r, evidences, marker='o', clip_on = False, label="page rank", color='#33CAFF', linestyle='--')
    # print "page_rank done"
    # evidences_dict['page_rank'] = evidences

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_local_clust,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="clust.", color='#339CFF', linestyle='--')
    print "clust done"
    evidences_dict['clust'] = evidences

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_kcore,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="kcore", color='#3358FF', linestyle='--')
    print "kcore done"
    evidences_dict['kcore'] = evidences

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_eigenvector_centr,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="eigen. centr.", color='#7133FF', linestyle='--')
    print "eigen done"
    evidences_dict['eigen'] = evidences

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_hubs,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="hub", color='#D733FF', linestyle='--')
    print "hubs done"
    evidences_dict['hubs'] = evidences

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_authority,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="authority", color='#FF33CE', linestyle='--')
    print "authority done"
    evidences_dict['authority'] = evidences


    # further plotting
    ax.set_xlabel("hypothesis weighting factor k")
    ax.set_ylabel("marginal likelihood / evidence (log)")
    # if we use log space for k then we need to set x also to log and improve the labels
    ax.set_xscale("log")

    plt.grid(False)
    ax.xaxis.grid(True)
    handles, labels = ax.get_legend_handles_labels()
    lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,-0.1), ncol=4)


    if additive:
        if inverted:
            plt.savefig('output/compare_structural_additive_inverted_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_structural_additive_inverted_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)
        else:
            plt.savefig('output/compare_structural_additive_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_structural_additive_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)

    else:
        if inverted:
            plt.savefig('output/compare_structural_inverted_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_structural_inverted_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)
        else:
            plt.savefig('output/compare_structural_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_structural_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)

    print "structural_evidences"


def compare_structural_page_rank(additive, inverted):
    print 'additve'
    print additive
    print 'inverted'
    print inverted
    #read vocab, graph, transitions
    #transitions = cPickle.load( open( SSD_HOME+"pickle/transitions", "rb" ) )
    transition_matrix = cPickle.load( open( SSD_HOME+"pickle/transition_matrix", "rb" ) )
    print "loaded transitions"
    graph = cPickle.load( open( SSD_HOME+"pickle/graph", "rb" ) )
    print "loaded graph"
    values = cPickle.load( open( SSD_HOME+"pickle/values", "rb" ) )
    values_page_rank = cPickle.load( open( SSD_HOME+"pickle/values_page_rank", "rb" ) )

    if inverted:
        values_page_rank = [1.0/x if x >0 else 0 for x in values_page_rank]


    vocab = cPickle.load( open( SSD_HOME+"pickle/vocab", "rb" ) )
    print "loaded vocab"

    state_count = len(vocab)
    states = vocab.keys()
    shape = (state_count, state_count)

    # we can use an empty matrix here as the HypTrails class then
    # properly distributes the chips for elicitation


    # structural hypothesises
    hyp_structural = csr_matrix((values, (graph[0], graph[1])),
                                shape=shape, dtype=np.float)
    print "hyp_structural_m"



    hyp_page_rank = csr_matrix((values_page_rank, (graph[0], graph[1])),
                               shape=shape, dtype=np.float)


    del graph
    del values_page_rank


    print "after delete"

    transitions = csr_matrix((transition_matrix[2], (transition_matrix[0], transition_matrix[1])),
                             shape=shape)
    print "transitions"

    del transition_matrix
    print " delete transitions"

    #delete all zero rows from all  see  http://stackoverflow.com/questions/31188141/scipy-sparse-matrix-remove-the-rows-whose-all-elements-are-zero
    print transitions.shape
    nonzero_row_indice, _ = transitions.nonzero()
    unique_nonzero_indice = np.unique(nonzero_row_indice)
    transitions = transitions[unique_nonzero_indice]
    print transitions.shape

    hyp_data = csr_matrix(transitions, copy=True)
    print hyp_data.shape

    hyp_structural = hyp_structural[unique_nonzero_indice]



    hyp_page_rank = hyp_page_rank[unique_nonzero_indice]



    ht = HypTrails(vocab)
    ht.fit(transitions)
    print "after fit"

    fig = plt.figure()
    ax = fig.add_subplot(111)

    r_first = 0.0001
    r = np.logspace(np.log10(r_first), np.log10(10000), 6)

    evidences_dict = {}
    evidences_dict['r'] = r
    evidences_dict['r_first'] = r_first

    #norm
    print "in norm each "
    hyp_structural = norm_hyp(hyp_structural)
    hyp_page_rank = norm_hyp(hyp_page_rank)

    #add the normed
    if additive:
        print "in additive"
        hyp_page_rank = hyp_structural + hyp_page_rank






    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_page_rank,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="page rank", color='#33CAFF', linestyle='--')
    print "page_rank done"
    evidences_dict['page_rank'] = evidences




    # further plotting
    ax.set_xlabel("hypothesis weighting factor k")
    ax.set_ylabel("marginal likelihood / evidence (log)")
    # if we use log space for k then we need to set x also to log and improve the labels
    ax.set_xscale("log")

    plt.grid(False)
    ax.xaxis.grid(True)
    handles, labels = ax.get_legend_handles_labels()
    lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,-0.1), ncol=4)


    if additive:
        if inverted:
            plt.savefig('output/compare_structural_page_rank_additive_inverted_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_structural_page_rank_additive_inverted_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)
        else:
            plt.savefig('output/compare_structural_page_rank_additive_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_structural_page_rank_additive_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)

    else:
        if inverted:
            plt.savefig('output/compare_structural_page_rank_inverted_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_structural_page_rank_inverted_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)
        else:
            plt.savefig('output/compare_structural_page_rank_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_structural_page_rank_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)

    print "structural_page_rank_evidences"


def compare_sem_sim(additive, inverted):
    #read vocab, graph, transitions
    transition_matrix = cPickle.load( open( SSD_HOME+"pickle/transition_matrix", "rb" ) )
    print "loaded transitions"
    graph = cPickle.load( open( SSD_HOME+"pickle/graph", "rb" ) )
    print "loaded graph"
    values = cPickle.load( open( SSD_HOME+"pickle/values", "rb" ) )
    print "loaded values"

    sem_sim_hyp = cPickle.load( open( SSD_HOME+"pickle/sem_sim_hyp", "rb" ) )
    print "sem_sim_hyp values"

    sem_sim_topic_hyp = cPickle.load( open( SSD_HOME+"pickle/topic_sim_hyp", "rb" ) )
    print "sem_sim_topic_hyp values"

    vocab = cPickle.load( open( SSD_HOME+"pickle/vocab", "rb" ) )
    print "loaded vocab"

    if inverted:
        sem_sim_hyp[2] = [1.0/x if x >0 else 0 for x in sem_sim_hyp[2]]
        sem_sim_topic_hyp[2] = [1.0/x if x >0 else 0 for x in sem_sim_topic_hyp[2]]



    state_count = len(vocab)
    states = vocab.keys()
    shape = (state_count, state_count)

    # we can use an empty matrix here as the HypTrails class then
    # properly distributes the chips for elicitation
    hyp_uniform = csr_matrix((state_count,state_count))



    # structural hypothesis
    hyp_structural = csr_matrix((values, (graph[0], graph[1])),
                                shape=shape, dtype=np.float)



    del graph

    transitions = csr_matrix((transition_matrix[2], (transition_matrix[0], transition_matrix[1])),
                             shape=shape)

    del transition_matrix


    #delete all zero rows from all  see  http://stackoverflow.com/questions/31188141/scipy-sparse-matrix-remove-the-rows-whose-all-elements-are-zero
    print transitions.shape
    nonzero_row_indice, _ = transitions.nonzero()
    unique_nonzero_indice = np.unique(nonzero_row_indice)
    transitions = transitions[unique_nonzero_indice]
    print transitions.shape

    hyp_structural = hyp_structural[unique_nonzero_indice]
    print hyp_structural.shape

    hyp_uniform = hyp_uniform[unique_nonzero_indice]
    print hyp_uniform.shape


    hyp_data = csr_matrix(transitions, copy=True)
    print hyp_data.shape


    hyp_sem_sim = csr_matrix((sem_sim_hyp[2], (sem_sim_hyp[0], sem_sim_hyp[1])),
                                         shape=hyp_data.shape, dtype=np.float)
    print hyp_sem_sim.shape
    del sem_sim_hyp

    hyp_sem_sim_topic = csr_matrix((sem_sim_topic_hyp[2], (sem_sim_topic_hyp[0], sem_sim_topic_hyp[1])),
                             shape=hyp_data.shape, dtype=np.float)
    print hyp_sem_sim_topic.shape
    del sem_sim_topic_hyp

    #norm
    hyp_structural = norm_hyp(hyp_structural)
    hyp_sem_sim = norm_hyp(hyp_sem_sim)
    hyp_sem_sim_topic = norm_hyp(hyp_sem_sim_topic)

    #add the normed
    if additive:
        hyp_sem_sim = hyp_structural + hyp_sem_sim
        hyp_sem_sim_topic = hyp_structural + hyp_sem_sim_topic

    ht = HypTrails(vocab)
    ht.fit(transitions)
    print "after fit"

    fig = plt.figure()
    ax = fig.add_subplot(111)

    r_first = 0.0001
    r = np.logspace(np.log10(r_first), np.log10(10000), 6)

    evidences_dict = {}
    evidences_dict['r'] = r
    evidences_dict['r_first'] = r_first

    # uniform hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix((hyp_data.shape)),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_uniform, hyp_structural, k=i, norm=True ))
    ax.plot(r, evidences, marker='o', clip_on = False, label="uniform", color='#FF3333', linestyle='--')
    print "uniform done"
    print evidences
    evidences_dict['uniform']=evidences

    # structural hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_structural,hyp_structural,k=i, norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="structural", color='#FF8D33', linestyle='--')
    print "structural done"
    print evidences
    evidences_dict['structural']=evidences

    # data hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_data,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="data", color='#A8FF33', linestyle='--')
    print "data done"
    print evidences
    evidences_dict['data']=evidences


    # sem sim hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_sem_sim,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="sem. sim.", color='#FE0000', linestyle='--')
    print "sem_sim  done"
    print evidences
    evidences_dict['sem_sim']=evidences

    # sem sim topic hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_sem_sim_topic,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="sem. sim. topic", color='#FF33CE', linestyle='--')
    print "sem_sim_topic  done"
    print evidences
    evidences_dict['sem_sim_topic']=evidences

    # further plotting
    ax.set_xlabel("hypothesis weighting factor k")
    ax.set_ylabel("marginal likelihood / evidence (log)")
    # if we use log space for k then we need to set x also to log and improve the labels
    ax.set_xscale("log")

    plt.grid(False)
    ax.xaxis.grid(True)
    handles, labels = ax.get_legend_handles_labels()
    lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,-0.1), ncol=4)

    if additive:
        if inverted:
            plt.savefig('output/compare_sem_sim_additive_inverted_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_sem_sim_additive_inverted_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)
        else:
            plt.savefig('output/compare_sem_sim_additive_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_sem_sim_additive_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)

    else:
        if inverted:
            plt.savefig('output/compare_sem_sim_inverted_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_sem_sim_inverted_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)
        else:
            plt.savefig('output/compare_sem_sim_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_sem_sim_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)

    print "sem_sim_evidences"



def compare_relative_positive(additive, inverted):
    #read vocab, graph, transitions
    #transitions = cPickle.load( open( SSD_HOME+"pickle/transitions", "rb" ) )
    transition_matrix = cPickle.load( open( SSD_HOME+"pickle/transition_matrix", "rb" ) )
    print "loaded transitions"
    graph = cPickle.load( open( SSD_HOME+"pickle/graph", "rb" ) )
    print "loaded graph"
    values = cPickle.load( open( SSD_HOME+"pickle/values", "rb" ) )
    print "loaded values"

    positive_rel_degree_hyp = cPickle.load( open( SSD_HOME+"pickle/positive_rel_degree_hyp", "rb" ) )
    print "positive_rel_degree_hyp values"

    positive_rel_out_degree_hyp = cPickle.load( open( SSD_HOME+"pickle/positive_rel_out_degree_hyp", "rb" ) )
    print "positive_rel_out_degree_hyp values"


    positive_rel_in_degree_hyp = cPickle.load( open( SSD_HOME+"pickle/positive_rel_in_degree_hyp", "rb" ) )
    print "positive_rel_out_degree_hyp values"

    positive_rel_hits_hub_hyp = cPickle.load( open( SSD_HOME+"pickle/positive_rel_hits_hub_hyp", "rb" ) )
    print "positive_rel_hits_hub_hyp values"

    positive_rel_hits_authority_hyp = cPickle.load( open( SSD_HOME+"pickle/positive_rel_hits_authority_hyp", "rb" ) )
    print "positive_rel_hits_authority_hyp values"

    positive_rel_eigen_centr_hyp = cPickle.load( open( SSD_HOME+"pickle/positive_rel_eigen_centr_hyp", "rb" ) )
    print "positive_rel_eigen_centr_hyp values"

    positive_rel_kcore_hyp = cPickle.load( open( SSD_HOME+"pickle/positive_rel_kcore_hyp", "rb" ) )
    print "positive_rel_kcore_hyp values"

    positive_rel_local_clust_hyp = cPickle.load( open( SSD_HOME+"pickle/positive_rel_local_clust_hyp", "rb" ) )
    print "positive_rel_local_clust_hyp values"

    positive_rel_page_rank_hyp = cPickle.load( open( SSD_HOME+"pickle/positive_rel_page_rank_hyp", "rb" ) )
    print "positive_rel_page_rank_hyp values"


    if inverted:
        positive_rel_degree_hyp = [1.0/x if x >0 else 0 for x in positive_rel_degree_hyp]
        positive_rel_out_degree_hyp = [1.0/x if x >0 else 0 for x in positive_rel_out_degree_hyp]
        positive_rel_in_degree_hyp = [1.0/x if x >0 else 0 for x in positive_rel_in_degree_hyp]
        positive_rel_hits_hub_hyp = [1.0/x if x >0 else 0 for x in positive_rel_hits_hub_hyp]
        positive_rel_hits_authority_hyp = [1.0/x if x >0 else 0 for x in positive_rel_hits_authority_hyp]
        positive_rel_eigen_centr_hyp = [1.0/x if x >0 else 0 for x in positive_rel_eigen_centr_hyp]
        positive_rel_kcore_hyp = [1.0/x if x >0 else 0 for x in positive_rel_kcore_hyp]
        positive_rel_local_clust_hyp = [1.0/x if x >0 else 0 for x in positive_rel_local_clust_hyp]
        positive_rel_page_rank_hyp = [1.0/x if x >0 else 0 for x in positive_rel_page_rank_hyp]


    vocab = cPickle.load( open( SSD_HOME+"pickle/vocab", "rb" ) )
    print "loaded vocab"



    state_count = len(vocab)
    states = vocab.keys()
    shape = (state_count, state_count)

    # we can use an empty matrix here as the HypTrails class then
    # properly distributes the chips for elicitation
    hyp_uniform = csr_matrix((state_count,state_count))



    # structural hypothesis
    hyp_structural = csr_matrix((values, (graph[0], graph[1])),
                                shape=shape, dtype=np.float)

    del graph


    print "after delete"

    transitions = csr_matrix((transition_matrix[2], (transition_matrix[0], transition_matrix[1])),
                             shape=shape)

    del transition_matrix


    #delete all zero rows from all  see  http://stackoverflow.com/questions/31188141/scipy-sparse-matrix-remove-the-rows-whose-all-elements-are-zero
    print transitions.shape
    nonzero_row_indice, _ = transitions.nonzero()
    unique_nonzero_indice = np.unique(nonzero_row_indice)
    transitions = transitions[unique_nonzero_indice]
    print transitions.shape

    hyp_structural = hyp_structural[unique_nonzero_indice]
    print hyp_structural.shape

    hyp_uniform = hyp_uniform[unique_nonzero_indice]
    print hyp_uniform.shape

    hyp_data = csr_matrix(transitions, copy=True)
    print hyp_data.shape



    hyp_rel_degree_positive = csr_matrix((positive_rel_degree_hyp[2], (positive_rel_degree_hyp[0], positive_rel_degree_hyp[1])),
                                         shape=hyp_data.shape, dtype=np.float)



    hyp_rel_out_degree_positive = csr_matrix((positive_rel_out_degree_hyp[2], (positive_rel_out_degree_hyp[0], positive_rel_out_degree_hyp[1])),
                                         shape=hyp_data.shape, dtype=np.float)


    hyp_rel_in_degree_positive = csr_matrix((positive_rel_in_degree_hyp[2], (positive_rel_in_degree_hyp[0], positive_rel_in_degree_hyp[1])),
                                             shape=hyp_data.shape, dtype=np.float)



    hyp_rel_hits_hub_positive = csr_matrix((positive_rel_hits_hub_hyp[2], (positive_rel_hits_hub_hyp[0], positive_rel_hits_hub_hyp[1])),
                                            shape=hyp_data.shape, dtype=np.float)



    hyp_rel_hits_authority_positive = csr_matrix((positive_rel_hits_authority_hyp[2], (positive_rel_hits_authority_hyp[0], positive_rel_hits_authority_hyp[1])),
                                           shape=hyp_data.shape, dtype=np.float)

    hyp_rel_eigen_centr_positive = csr_matrix((positive_rel_eigen_centr_hyp[2], (positive_rel_eigen_centr_hyp[0], positive_rel_eigen_centr_hyp[1])),
                                                 shape=hyp_data.shape, dtype=np.float)


    hyp_rel_kcore_positive = csr_matrix((positive_rel_kcore_hyp[2], (positive_rel_kcore_hyp[0], positive_rel_kcore_hyp[1])),
                                              shape=hyp_data.shape, dtype=np.float)



    hyp_rel_local_clust_positive = csr_matrix((positive_rel_local_clust_hyp[2], (positive_rel_local_clust_hyp[0], positive_rel_local_clust_hyp[1])),
                                        shape=hyp_data.shape, dtype=np.float)



    hyp_rel_page_rank_positive = csr_matrix((positive_rel_page_rank_hyp[2], (positive_rel_page_rank_hyp[0], positive_rel_page_rank_hyp[1])),
                                              shape=hyp_data.shape, dtype=np.float)



    del positive_rel_degree_hyp
    del positive_rel_out_degree_hyp
    del positive_rel_in_degree_hyp
    del positive_rel_hits_hub_hyp
    del positive_rel_hits_authority_hyp
    del positive_rel_eigen_centr_hyp
    del positive_rel_kcore_hyp
    del positive_rel_local_clust_hyp
    del positive_rel_page_rank_hyp

    ht = HypTrails(vocab)
    ht.fit(transitions)
    print "after fit"

    fig = plt.figure()
    ax = fig.add_subplot(111)

    r_first = 0.0001
    r = np.logspace(np.log10(r_first), np.log10(10000), 6)

    evidences_dict = {}
    evidences_dict['r'] = r
    evidences_dict['r_first'] = r_first

    #norm
    print "in norm each "

    hyp_structural = norm_hyp(hyp_structural)
    hyp_positive_rel_degree = norm_hyp(hyp_positive_rel_degree)
    hyp_positive_in_rel_degree = norm_hyp(hyp_positive_in_rel_degree)
    hyp_positive_out_rel_degree = norm_hyp(hyp_positive_out_rel_degree)
    hyp_positive_rel_hits_hub = norm_hyp(hyp_positive_rel_hits_hub)
    hyp_positive_rel_hits_authority = norm_hyp(hyp_positive_rel_hits_authority)
    hyp_positive_rel_eigen_centr = norm_hyp(hyp_positive_rel_eigen_centr)
    hyp_positive_rel_kcore = norm_hyp(hyp_positive_rel_kcore)
    hyp_positive_rel_local_clust = norm_hyp(hyp_positive_rel_local_clust)
    hyp_positive_rel_page_rank = norm_hyp(hyp_positive_rel_page_rank)



    # uniform hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix((hyp_data.shape)),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_uniform, hyp_structural, k=i, norm=True ))
    ax.plot(r, evidences, marker='o', clip_on = False, label="uniform", color='#FF3333', linestyle='--')
    print "uniform done"
    print evidences
    evidences_dict['uniform']=evidences

    # structural hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_structural,hyp_structural,k=i, norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="structural", color='#FF8D33', linestyle='--')
    print "structural done"
    print evidences
    evidences_dict['structural']=evidences

    # data hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_data,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="data", color='#A8FF33', linestyle='--')
    print "data done"
    print evidences
    evidences_dict['data']=evidences

    # positive rel degree hypothesis
    if additive == True:
        hyp_rel_degree_positive = hyp_rel_degree_positive + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_rel_degree_positive,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="+ rel. degree", color='#FE8680', linestyle='--')
    print "rel_degree_positive  done"
    print evidences
    evidences_dict['rel_degree_positive']=evidences



    # positive rel in degree hypothesis
    if additive == True:
        hyp_rel_in_degree_positive = hyp_rel_in_degree_positive + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_rel_in_degree_positive,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="+ rel. in-degree", color='#FEA880', linestyle='--')
    print "rel_in_degree_positive  done"
    print evidences
    evidences_dict['rel_in_degree_positive']=evidences


    # positive rel out degree hypothesis
    evidences = []
    if additive == True:
        hyp_rel_out_degree_positive = hyp_rel_out_degree_positive + hyp_structural
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_rel_out_degree_positive,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="+ rel. out-degree", color='#FEC380', linestyle='--')
    print "rel_out_degree_positive  done"
    print evidences
    evidences_dict['rel_out_degree_positive']=evidences



    # positive rel hub hypothesis
    if additive == True:
        hyp_rel_hits_hub_positive = hyp_rel_hits_hub_positive + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_rel_hits_hub_positive,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="+ rel. hub", color='#FEE180', linestyle='--')
    print "hyp_rel_hits_hub_positive  done"
    print evidences
    evidences_dict['hyp_rel_hits_hub_positive']=evidences


    # positive rel authority hypothesis
    if additive == True:
        hyp_rel_hits_authority_positive = hyp_rel_hits_authority_positive + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_rel_hits_authority_positive,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="+ rel. authority", color='#F3FE80', linestyle='--')
    print "hyp_rel_hits_authority_positive  done"
    print evidences
    evidences_dict['hyp_rel_hits_authority_positive']=evidences



    # positive rel eigen centr hypothesis
    if additive == True:
        hyp_rel_eigen_centr_positive = hyp_rel_eigen_centr_positive + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_rel_eigen_centr_positive,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="+ rel. eigen. centr.", color='#C9FE80', linestyle='--')
    print "hyp_rel_eigen_centr_positive  done"
    print evidences
    evidences_dict['hyp_rel_eigen_centr_positive']=evidences


    # positive rel kcore hypothesis
    if additive == True:
        hyp_rel_kcore_positive = hyp_rel_kcore_positive + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_rel_kcore_positive,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="+ rel. kcore", color='#93FE80', linestyle='--')
    print "hyp_rel_kcore_positive  done"
    print evidences
    evidences_dict['hyp_rel_kcore_positive']=evidences



    # positive rel local clust hypothesis
    if additive == True:
        hyp_rel_local_clust_positive = hyp_rel_local_clust_positive + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_rel_local_clust_positive,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="+ rel. clust.", color='#80FEAC', linestyle='--')
    print "hyp_rel_local_clust_positive  done"
    print evidences
    evidences_dict['hyp_rel_local_clust_positive']=evidences


    # positive rel page rank hypothesis
    evidences = []
    if additive == True:
        hyp_rel_page_rank_positive = hyp_rel_page_rank_positive + hyp_structural
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_rel_page_rank_positive,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="+ rel. page rank", color='#80FCFE', linestyle='--')
    print "hyp_rel_page_rank_positive  done"
    print evidences
    evidences_dict['hyp_rel_page_rank_positive']=evidences



    # further plotting
    ax.set_xlabel("hypothesis weighting factor k")
    ax.set_ylabel("marginal likelihood / evidence (log)")
    # if we use log space for k then we need to set x also to log and improve the labels
    ax.set_xscale("log")

    plt.grid(False)
    ax.xaxis.grid(True)
    handles, labels = ax.get_legend_handles_labels()
    lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,-0.1), ncol=4)


    if additive == False:
        if inverted:
            plt.savefig('output/compare_relative_positive_inverted_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_relative_positive_inverted_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)
        else:
            plt.savefig('output/compare_relative_positive_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_relative_positive_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)
    else:
        if inverted:
            plt.savefig('output/compare_relative_positive_additive_inverted_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_relative_positive_additive_inverted_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)
        else:
            plt.savefig('output/compare_relative_positive_additive_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_relative_positive_additive_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)


    print "relative_positive_evidences"



def compare_relative_negative(additive, inverted):
    #read vocab, graph, transitions
    #transitions = cPickle.load( open( SSD_HOME+"pickle/transitions", "rb" ) )
    transition_matrix = cPickle.load( open( SSD_HOME+"pickle/transition_matrix", "rb" ) )
    print "loaded transitions"
    graph = cPickle.load( open( SSD_HOME+"pickle/graph", "rb" ) )
    print "loaded graph"
    values = cPickle.load( open( SSD_HOME+"pickle/values", "rb" ) )
    print "loaded values"

    negative_rel_degree_hyp = cPickle.load( open( SSD_HOME+"pickle/negative_rel_degree_hyp", "rb" ) )
    print "negative_rel_degree_hyp values"
    negative_rel_degree_hyp = absolute_value_negative_rel_hyp(negative_rel_degree_hyp)



    negative_rel_out_degree_hyp = cPickle.load( open( SSD_HOME+"pickle/negative_rel_out_degree_hyp", "rb" ) )
    print "negative_rel_out_degree_hyp values"

    negative_rel_in_degree_hyp = cPickle.load( open( SSD_HOME+"pickle/negative_rel_in_degree_hyp", "rb" ) )
    print "negative_rel_in_degree_hyp values"

    negative_rel_hits_hub_hyp = cPickle.load( open( SSD_HOME+"pickle/negative_rel_hits_hub_hyp", "rb" ) )
    print "negative_rel_hits_hub_hyp values"

    negative_rel_hits_authority_hyp = cPickle.load( open( SSD_HOME+"pickle/negative_rel_hits_authority_hyp", "rb" ) )
    print "negative_rel_hits_authority_hyp values"

    negative_rel_eigen_centr_hyp = cPickle.load( open( SSD_HOME+"pickle/negative_rel_eigen_centr_hyp", "rb" ) )
    print "negative_rel_eigen_centr_hyp values"

    negative_rel_kcore_hyp = cPickle.load( open( SSD_HOME+"pickle/negative_rel_kcore_hyp", "rb" ) )
    print "negative_rel_kcore_hyp values"

    negative_rel_local_clust_hyp = cPickle.load( open( SSD_HOME+"pickle/negative_rel_local_clust_hyp", "rb" ) )
    print "negative_rel_local_clust_hyp values"

    negative_rel_page_rank_hyp = cPickle.load( open( SSD_HOME+"pickle/negative_rel_page_rank_hyp", "rb" ) )
    print "negative_rel_page_rank_hyp values"



    vocab = cPickle.load( open( SSD_HOME+"pickle/vocab", "rb" ) )
    print "loaded vocab"



    state_count = len(vocab)
    states = vocab.keys()
    shape = (state_count, state_count)

    # we can use an empty matrix here as the HypTrails class then
    # properly distributes the chips for elicitation
    hyp_uniform = csr_matrix((state_count,state_count))



    # structural hypothesis
    hyp_structural = csr_matrix((values, (graph[0], graph[1])),
                                shape=shape, dtype=np.float)

    del graph

    transitions = csr_matrix((transition_matrix[2], (transition_matrix[0], transition_matrix[1])),
                             shape=shape)

    del transition_matrix


    #delete all zero rows from all  see  http://stackoverflow.com/questions/31188141/scipy-sparse-matrix-remove-the-rows-whose-all-elements-are-zero
    print transitions.shape
    nonzero_row_indice, _ = transitions.nonzero()
    unique_nonzero_indice = np.unique(nonzero_row_indice)
    transitions = transitions[unique_nonzero_indice]
    print transitions.shape

    hyp_structural = hyp_structural[unique_nonzero_indice]
    print hyp_structural.shape

    hyp_uniform = hyp_uniform[unique_nonzero_indice]
    print hyp_uniform.shape

    hyp_data = csr_matrix(transitions, copy=True)
    print hyp_data.shape



    hyp_rel_degree_negative = csr_matrix((absolute_value_negative_rel_hyp(negative_rel_degree_hyp[2]), (negative_rel_degree_hyp[0], negative_rel_degree_hyp[1])),
                                         shape=hyp_data.shape, dtype=np.float)


    hyp_rel_out_degree_negative = csr_matrix((absolute_value_negative_rel_hyp(negative_rel_out_degree_hyp[2]), (negative_rel_out_degree_hyp[0], negative_rel_out_degree_hyp[1])),
                                             shape=hyp_data.shape, dtype=np.float)


    hyp_rel_in_degree_negative = csr_matrix((absolute_value_negative_rel_hyp(negative_rel_in_degree_hyp[2]), (negative_rel_in_degree_hyp[0], negative_rel_in_degree_hyp[1])),
                                            shape=hyp_data.shape, dtype=np.float)


    hyp_rel_hits_hub_negative = csr_matrix((absolute_value_negative_rel_hyp(negative_rel_hits_hub_hyp[2]), (negative_rel_hits_hub_hyp[0], negative_rel_hits_hub_hyp[1])),
                                           shape=hyp_data.shape, dtype=np.float)


    hyp_rel_hits_authority_negative = csr_matrix((absolute_value_negative_rel_hyp(negative_rel_hits_authority_hyp[2]), (negative_rel_hits_authority_hyp[0], negative_rel_hits_authority_hyp[1])),
                                                 shape=hyp_data.shape, dtype=np.float)

    hyp_rel_eigen_centr_negative = csr_matrix((absolute_value_negative_rel_hyp(negative_rel_eigen_centr_hyp[2]), (negative_rel_eigen_centr_hyp[0], negative_rel_eigen_centr_hyp[1])),
                                              shape=hyp_data.shape, dtype=np.float)

    hyp_rel_kcore_negative = csr_matrix((absolute_value_negative_rel_hyp(negative_rel_kcore_hyp[2]), (negative_rel_kcore_hyp[0], negative_rel_kcore_hyp[1])),
                                        shape=hyp_data.shape, dtype=np.float)


    hyp_rel_local_clust_negative = csr_matrix((absolute_value_negative_rel_hyp(negative_rel_local_clust_hyp[2]), (negative_rel_local_clust_hyp[0], negative_rel_local_clust_hyp[1])),
                                              shape=hyp_data.shape, dtype=np.float)


    hyp_rel_page_rank_negative = csr_matrix((absolute_value_negative_rel_hyp(negative_rel_page_rank_hyp[2]), (negative_rel_page_rank_hyp[0], negative_rel_page_rank_hyp[1])),
                                            shape=hyp_data.shape, dtype=np.float)



    del negative_rel_degree_hyp
    del negative_rel_out_degree_hyp
    del negative_rel_in_degree_hyp
    del negative_rel_hits_hub_hyp
    del negative_rel_hits_authority_hyp
    del negative_rel_eigen_centr_hyp
    del negative_rel_kcore_hyp
    del negative_rel_local_clust_hyp
    del negative_rel_page_rank_hyp

    ht = HypTrails(vocab)
    ht.fit(transitions)
    print "after fit"

    fig = plt.figure()
    ax = fig.add_subplot(111)

    r_first = 0.0001
    r = np.logspace(np.log10(r_first), np.log10(10000), 6)

    evidences_dict = {}
    evidences_dict['r'] = r
    evidences_dict['r_first'] = r_first

    #norm
    print "in norm each "

    hyp_structural = norm_hyp(hyp_structural)
    hyp_rel_degree_negative =  norm_hyp(hyp_rel_degree_negative)
    hyp_in_rel_degree_negative =  norm_hyp(hyp_in_rel_degree_negative)
    hyp_out_rel_degree_negative =  norm_hyp(hyp_out_rel_degree_negative)
    hyp_rel_hits_hub_negative =  norm_hyp(hyp_rel_hits_hub_negative)
    hyp_rel_hits_authority_negative =  norm_hyp(hyp_rel_hits_authority_negative)
    hyp_rel_eigen_centr_negative =  norm_hyp(hyp_rel_eigen_centr_negative)
    hyp_rel_kcore_negative =  norm_hyp(hyp_rel_kcore_negative)
    hyp_rel_local_clust_negative =  norm_hyp(hyp_rel_local_clust_negative)
    hyp_rel_page_rank_negative =  norm_hyp(hyp_rel_page_rank_negative)


    # uniform hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix((hyp_data.shape)),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_uniform, hyp_structural, k=i, norm=True ))
    ax.plot(r, evidences, marker='o', clip_on = False, label="uniform", color='#FF3333', linestyle='--')
    print "uniform done"
    print evidences
    evidences_dict['uniform']=evidences

    # structural hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_structural,hyp_structural,k=i, norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="structural", color='#FF8D33', linestyle='--')
    print "structural done"
    print evidences
    evidences_dict['structural']=evidences

    # data hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_data,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="data", color='#A8FF33', linestyle='--')
    print "data done"
    print evidences
    evidences_dict['data']=evidences


    # negative rel degree hypothesis
    if additive == True:
        hyp_rel_degree_negative = hyp_rel_degree_negative + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_rel_degree_negative,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="- rel. degree", color='#FE8680', linestyle='--')
    print "rel_degree_negative  done"
    print evidences
    evidences_dict['rel_degree_negative']=evidences



    # negative rel in degree hypothesis
    if additive == True:
        hyp_rel_in_degree_negative = hyp_rel_in_degree_negative + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_rel_in_degree_negative,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="- rel. in-degree", color='#FEA880', linestyle='--')
    print "rel_in_degree_negative  done"
    print evidences
    evidences_dict['rel_in_degree_negative']=evidences

    # negative rel out degree hypothesis
    evidences = []
    if additive == True:
        hyp_rel_out_degree_negative = hyp_rel_out_degree_negative + hyp_structural
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_rel_out_degree_negative,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="- rel. out-degree", color='#FEC380', linestyle='--')
    print "rel_out_degree_negative  done"
    print evidences
    evidences_dict['rel_out_degree_negative']=evidences



    # negative rel hub hypothesis
    if additive == True:
        hyp_rel_hits_hub_negative = hyp_rel_hits_hub_negative + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_rel_hits_hub_negative,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="- rel. hub", color='#FEE180', linestyle='--')
    print "hyp_rel_hits_hub_negative  done"
    print evidences
    evidences_dict['hyp_rel_hits_hub_negative']=evidences


    # negative rel authority hypothesis
    if additive == True:
        hyp_rel_hits_authority_negative = hyp_rel_hits_authority_negative + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_rel_hits_authority_negative,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="- rel. authority", color='#F3FE80', linestyle='--')
    print "hyp_rel_hits_authority_negative  done"
    print evidences
    evidences_dict['hyp_rel_hits_authority_negative']=evidences



    # negative rel eigen centr hypothesis
    if additive == True:
        hyp_rel_eigen_centr_negative = hyp_rel_eigen_centr_negative + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_rel_eigen_centr_negative,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="- rel. eigen. centr.", color='#C9FE80', linestyle='--')
    print "hyp_rel_eigen_centr_negative  done"
    print evidences
    evidences_dict['hyp_rel_eigen_centr_negative']=evidences


    # negative rel kcore hypothesis
    if additive == True:
        hyp_rel_kcore_negative = hyp_rel_kcore_negative + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_rel_kcore_negative,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="- rel. kcore", color='#93FE80', linestyle='--')
    print "hyp_rel_kcore_negative  done"
    print evidences
    evidences_dict['hyp_rel_kcore_negative']=evidences


    # negative rel local clust hypothesis
    if additive == True:
        hyp_rel_local_clust_negative = hyp_rel_local_clust_negative + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_rel_local_clust_negative,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="- rel. clust", color='#80FEAC', linestyle='--')
    print "hyp_rel_local_clust_negative  done"
    print evidences
    evidences_dict['hyp_rel_local_clust_negative']=evidences

    # negative rel page rank hypothesis
    if additive == True:
        hyp_rel_page_rank_negative = hyp_rel_page_rank_negative + hyp_structural
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_rel_page_rank_negative,hyp_structural,k=i,norm=False))
    ax.plot(r, evidences, marker='o', clip_on = False, label="- rel. page rank", color='#80FCFE', linestyle='--')
    print "hyp_rel_page_rank_negative  done"
    print evidences
    evidences_dict['hyp_rel_page_rank_negative']=evidences


    # further plotting
    ax.set_xlabel("hypothesis weighting factor k")
    ax.set_ylabel("marginal likelihood / evidence (log)")
    # if we use log space for k then we need to set x also to log and improve the labels
    ax.set_xscale("log")

    plt.grid(False)
    ax.xaxis.grid(True)
    handles, labels = ax.get_legend_handles_labels()
    lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,-0.1), ncol=4)
    if additive == False:
        if inverted:
            plt.savefig('output/compare_relative_negative_inverted_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_relative_negative_inverted_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)
        else:
            plt.savefig('output/compare_relative_negative_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_relative_negative_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)
    else:
        if inverted:
            plt.savefig('output/compare_relative_negative_additive_inverted_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_relative_negative_additive_inverted_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)
        else:
            plt.savefig('output/compare_relative_negative_additive_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
            cPickle.dump(evidences_dict, open("output/compare_relative_negative_additive_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)


    print "relative_negative_evidences"

def absolute_value_negative_rel_hyp(values):
    return np.absolute(np.array(values))

def compare_structural_additive_nomred(linkocc):
    #read vocab, graph, transitions
    #transitions = cPickle.load( open( SSD_HOME+"pickle/transitions", "rb" ) )
    transition_matrix = cPickle.load( open( SSD_HOME+"pickle/transition_matrix", "rb" ) )
    print "loaded transitions"
    graph = cPickle.load( open( SSD_HOME+"pickle/graph", "rb" ) )
    print "loaded graph"
    values = cPickle.load( open( SSD_HOME+"pickle/values", "rb" ) )
    values_m = cPickle.load( open( SSD_HOME+"pickle/values_m", "rb" ) )
    velues_out_deg = cPickle.load( open( SSD_HOME+"pickle/velues_out_deg", "rb" ) )
    velues_in_deg = cPickle.load( open( SSD_HOME+"pickle/velues_in_deg", "rb" ) )
    velues_deg = cPickle.load( open( SSD_HOME+"pickle/velues_deg", "rb" ) )
    values_page_rank = cPickle.load( open( SSD_HOME+"pickle/values_page_rank", "rb" ) )
    values_local_clust = cPickle.load( open( SSD_HOME+"pickle/values_local_clust", "rb" ) )
    values_kcore = cPickle.load( open( SSD_HOME+"pickle/values_kcore", "rb" ) )
    values_eigenvector_centr = cPickle.load( open( SSD_HOME+"pickle/values_eigenvector_centr", "rb" ) )
    values_hubs = cPickle.load( open( SSD_HOME+"pickle/values_hubs", "rb" ) )
    values_authority = cPickle.load( open( SSD_HOME+"pickle/values_authority", "rb" ) )

    sem_sim_hyp = cPickle.load( open( SSD_HOME+"pickle/sem_sim_hyp", "rb" ) )
    print "sem_sim_hyp values"


    vocab = cPickle.load( open( SSD_HOME+"pickle/vocab", "rb" ) )
    print "loaded vocab"

    state_count = len(vocab)
    states = vocab.keys()
    shape = (state_count, state_count)

    # we can use an empty matrix here as the HypTrails class then
    # properly distributes the chips for elicitation
    hyp_uniform = csr_matrix((state_count,state_count))



    # structural hypothesises
    hyp_structural = csr_matrix((values, (graph[0], graph[1])),
                                shape=shape, dtype=np.float)



    hyp_structural_m = csr_matrix((values_m, (graph[0], graph[1])),
                                  shape=shape, dtype=np.float)


    hyp_out_degree = csr_matrix((velues_out_deg, (graph[0], graph[1])),
                                shape=shape, dtype=np.float)

    hyp_in_degree = csr_matrix((velues_in_deg, (graph[0], graph[1])),
                               shape=shape, dtype=np.float)

    hyp_degree = csr_matrix((velues_deg, (graph[0], graph[1])),
                            shape=shape, dtype=np.float)


    hyp_page_rank = csr_matrix((values_page_rank, (graph[0], graph[1])),
                               shape=shape, dtype=np.float)

    hyp_local_clust = csr_matrix((values_local_clust, (graph[0], graph[1])),
                                 shape=shape, dtype=np.float)

    hyp_kcore = csr_matrix((values_kcore, (graph[0], graph[1])),
                           shape=shape, dtype=np.float)

    hyp_eigenvector_centr = csr_matrix((values_eigenvector_centr, (graph[0], graph[1])),
                                       shape=shape, dtype=np.float)

    hyp_hubs = csr_matrix((values_hubs, (graph[0], graph[1])),
                          shape=shape, dtype=np.float)

    hyp_authority = csr_matrix((values_authority, (graph[0], graph[1])),
                               shape=shape, dtype=np.float)




    del graph
    del values
    del values_m
    del velues_in_deg
    del velues_out_deg
    del velues_deg
    del values_local_clust
    del values_kcore
    del values_eigenvector_centr
    del values_hubs
    del values_authority
    del values_page_rank


    # i_indices = array.array(str("l"))
    # j_indices = array.array(str("l"))
    # values = array.array(str("d"))
    #
    # for s, targets in transitions.iteritems():
    #     for t, v in targets.iteritems():
    #         i_indices.append(vocab[s])
    #         j_indices.append(vocab[t])
    #         values.append(v)
    #
    # i_indices = np.frombuffer(i_indices, dtype=np.int_)
    # j_indices = np.frombuffer(j_indices, dtype=np.int_)
    # values = np.frombuffer(values, dtype=np.float64)

    #transitions = csr_matrix((values, (i_indices, j_indices)),
    #                         shape=shape)

    transitions = csr_matrix((transition_matrix[2], (transition_matrix[0], transition_matrix[1])),
                             shape=shape)

    del transition_matrix

    #delete all zero rows from all  see  http://stackoverflow.com/questions/31188141/scipy-sparse-matrix-remove-the-rows-whose-all-elements-are-zero
    print transitions.shape
    nonzero_row_indice, _ = transitions.nonzero()
    unique_nonzero_indice = np.unique(nonzero_row_indice)
    transitions = transitions[unique_nonzero_indice]
    print transitions.shape

    hyp_data = csr_matrix(transitions, copy=True)
    print hyp_data.shape

    hyp_structural = hyp_structural[unique_nonzero_indice]

    hyp_uniform = hyp_uniform[unique_nonzero_indice]

    hyp_structural_m = hyp_structural_m[unique_nonzero_indice]

    hyp_out_degree = hyp_out_degree[unique_nonzero_indice]

    hyp_in_degree = hyp_in_degree[unique_nonzero_indice]

    hyp_degree = hyp_degree[unique_nonzero_indice]

    hyp_page_rank = hyp_page_rank[unique_nonzero_indice]

    hyp_local_clust = hyp_local_clust[unique_nonzero_indice]

    hyp_kcore = hyp_kcore[unique_nonzero_indice]

    hyp_eigenvector_centr = hyp_eigenvector_centr[unique_nonzero_indice]

    hyp_hubs= hyp_hubs[unique_nonzero_indice]

    hyp_authority = hyp_authority[unique_nonzero_indice]

    hyp_sem_sim = csr_matrix((sem_sim_hyp[2], (sem_sim_hyp[0], sem_sim_hyp[1])),
                             shape=hyp_data.shape, dtype=np.float)


    #norm
    if linkocc == False:

        hyp_structural_nomred = norm_hyp(hyp_structural)

        hyp_structural_m = hyp_structural_nomred + norm_hyp(hyp_structural_m)
        hyp_in_degree = hyp_structural_nomred + norm_hyp(hyp_in_degree)
        hyp_out_degree = hyp_structural_nomred + norm_hyp(hyp_out_degree)
        hyp_degree = hyp_structural_nomred + norm_hyp(hyp_degree)
        hyp_page_rank = hyp_structural_nomred + norm_hyp(hyp_page_rank)
        hyp_local_clust = hyp_structural_nomred + norm_hyp(hyp_local_clust)
        hyp_kcore = hyp_structural_nomred + norm_hyp(hyp_kcore)
        hyp_eigenvector_centr = hyp_structural_nomred + norm_hyp(hyp_eigenvector_centr)
        hyp_hubs = hyp_structural_nomred + norm_hyp(hyp_hubs)
        hyp_authority = hyp_structural_nomred + norm_hyp(hyp_authority)
        hyp_sem_sim = hyp_structural_nomred + norm_hyp(hyp_sem_sim)
    else:
        hyp_structural_m_nomred = norm_hyp(hyp_structural_m)

        hyp_structural = hyp_structural_m_nomred + norm_hyp(hyp_structural)
        hyp_in_degree = hyp_structural_m_nomred + norm_hyp(hyp_in_degree)
        hyp_out_degree = hyp_structural_m_nomred + norm_hyp(hyp_out_degree)
        hyp_degree = hyp_structural_m_nomred + norm_hyp(hyp_degree)
        hyp_page_rank = hyp_structural_m_nomred + norm_hyp(hyp_page_rank)
        hyp_local_clust = hyp_structural_m_nomred + norm_hyp(hyp_local_clust)
        hyp_kcore = hyp_structural_m_nomred + norm_hyp(hyp_kcore)
        hyp_eigenvector_centr = hyp_structural_m_nomred + norm_hyp(hyp_eigenvector_centr)
        hyp_hubs = hyp_structural_m_nomred + norm_hyp(hyp_hubs)
        hyp_authority = hyp_structural_m_nomred + norm_hyp(hyp_authority)
        hyp_sem_sim = hyp_structural_m_nomred + norm_hyp(hyp_sem_sim)





    ht = HypTrails(vocab)
    ht.fit(transitions)
    print "after fit"

    fig = plt.figure()
    ax = fig.add_subplot(111)

    r_first = 0.0001
    r = np.logspace(np.log10(r_first), np.log10(10000), 10)

    evidences_dict = {}
    evidences_dict['r'] = r
    evidences_dict['r_first'] = r_first

    # uniform hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_uniform,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="uniform", color='#FF3333', linestyle='--')
    print "uniform done"
    evidences_dict['uniform'] = evidences

    # structural hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_structural,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="structural", color='#FF8D33', linestyle='--')
    print "structural done"
    evidences_dict['structural'] = evidences

    # data hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_data,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="data", color='#A8FF33', linestyle='--')
    print "data done"
    evidences_dict['data'] = evidences

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_structural_m,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="link occ.",  color='#33FF36', linestyle='--')
    print "structural_m done"
    evidences_dict['link occ.'] = evidences

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_out_degree,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="out-degree",  color='#33FF96', linestyle='--')
    print "out degree done"
    evidences_dict['out degree'] = evidences


    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_in_degree,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="in-degree", color='#33FFE0', linestyle='--')
    print "in degree done"
    evidences_dict['in degree'] = evidences

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_degree,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="degree", color='#33F3FF', linestyle='--')
    print "degree done"
    evidences_dict['degree'] = evidences

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_page_rank,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="page rank", color='#33CAFF', linestyle='--')
    print "page_rank done"
    evidences_dict['page_rank'] = evidences

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_local_clust,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="clust.", color='#339CFF', linestyle='--')
    print "clust done"
    evidences_dict['clust'] = evidences

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_kcore,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="kcore", color='#3358FF', linestyle='--')
    print "kcore done"
    evidences_dict['kcore'] = evidences

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_eigenvector_centr,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="eigen. centr.", color='#7133FF', linestyle='--')
    print "eigen done"
    evidences_dict['eigen'] = evidences

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_hubs,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="hub", color='#D733FF', linestyle='--')
    print "hubs done"
    evidences_dict['hubs'] = evidences

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_authority,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="authority", color='#FF33CE', linestyle='--')
    print "authority done"
    evidences_dict['authority'] = evidences

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_sem_sim,hyp_structural,k=i,norm=True))
    ax.plot(r, evidences, marker='o', clip_on = False, label="sem. sim.", color='#FE0000', linestyle='--')
    print "sem sim done"
    evidences_dict['sem_sim'] = evidences


    # further plotting
    ax.set_xlabel("hypothesis weighting factor k")
    ax.set_ylabel("marginal likelihood / evidence (log)")
    # if we use log space for k then we need to set x also to log and improve the labels
    ax.set_xscale("log")

    plt.grid(False)
    ax.xaxis.grid(True)
    handles, labels = ax.get_legend_handles_labels()
    lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,-0.1), ncol=4)
    if linkocc==False:
        plt.savefig('output/compare_structural_additive_normed_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
        cPickle.dump(evidences_dict, open("output/structural_additive_normed_evidences", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)
    else:
        plt.savefig('output/compare_structural_linkocc_additive_normed_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
        cPickle.dump(evidences_dict, open("output/structural_linkocc_additive_normed_evidences", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)

    print "structural_evidences"


def compare_structural_additive_mult_nomred(linkocc, max_k):
    #read vocab, graph, transitions
    #transitions = cPickle.load( open( SSD_HOME+"pickle/transitions", "rb" ) )
    transition_matrix = cPickle.load( open( SSD_HOME+"pickle/transition_matrix", "rb" ) )
    print "loaded transitions"
    graph = cPickle.load( open( SSD_HOME+"pickle/graph", "rb" ) )
    print "loaded graph"
    values = cPickle.load( open( SSD_HOME+"pickle/values", "rb" ) )
    values_m = cPickle.load( open( SSD_HOME+"pickle/values_m", "rb" ) )
    velues_out_deg = cPickle.load( open( SSD_HOME+"pickle/velues_out_deg", "rb" ) )
    velues_in_deg = cPickle.load( open( SSD_HOME+"pickle/velues_in_deg", "rb" ) )
    velues_deg = cPickle.load( open( SSD_HOME+"pickle/velues_deg", "rb" ) )
    values_page_rank = cPickle.load( open( SSD_HOME+"pickle/values_page_rank", "rb" ) )
    values_local_clust = cPickle.load( open( SSD_HOME+"pickle/values_local_clust", "rb" ) )
    values_kcore = cPickle.load( open( SSD_HOME+"pickle/values_kcore", "rb" ) )
    values_eigenvector_centr = cPickle.load( open( SSD_HOME+"pickle/values_eigenvector_centr", "rb" ) )
    values_hubs = cPickle.load( open( SSD_HOME+"pickle/values_hubs", "rb" ) )
    values_authority = cPickle.load( open( SSD_HOME+"pickle/values_authority", "rb" ) )

    sem_sim_hyp = cPickle.load( open( SSD_HOME+"pickle/sem_sim_hyp", "rb" ) )
    print "sem_sim_hyp values"


    vocab = cPickle.load( open( SSD_HOME+"pickle/vocab", "rb" ) )
    print "loaded vocab"

    state_count = len(vocab)
    states = vocab.keys()
    shape = (state_count, state_count)

    # we can use an empty matrix here as the HypTrails class then
    # properly distributes the chips for elicitation
    hyp_uniform = csr_matrix((state_count,state_count))



    # structural hypothesises
    hyp_structural = csr_matrix((values, (graph[0], graph[1])),
                                shape=shape, dtype=np.float)



    hyp_structural_m = csr_matrix((values_m, (graph[0], graph[1])),
                                  shape=shape, dtype=np.float)

    print "hyp_structural_m"
    hyp_out_degree = csr_matrix((velues_out_deg, (graph[0], graph[1])),
                                shape=shape, dtype=np.float)

    hyp_in_degree = csr_matrix((velues_in_deg, (graph[0], graph[1])),
                               shape=shape, dtype=np.float)

    hyp_degree = csr_matrix((velues_deg, (graph[0], graph[1])),
                            shape=shape, dtype=np.float)

    print "hyp_degree"
    hyp_page_rank = csr_matrix((values_page_rank, (graph[0], graph[1])),
                               shape=shape, dtype=np.float)

    hyp_local_clust = csr_matrix((values_local_clust, (graph[0], graph[1])),
                                 shape=shape, dtype=np.float)

    hyp_kcore = csr_matrix((values_kcore, (graph[0], graph[1])),
                           shape=shape, dtype=np.float)

    hyp_eigenvector_centr = csr_matrix((values_eigenvector_centr, (graph[0], graph[1])),
                                       shape=shape, dtype=np.float)
    print "hyp_eigenvector_centr"
    hyp_hubs = csr_matrix((values_hubs, (graph[0], graph[1])),
                          shape=shape, dtype=np.float)

    hyp_authority = csr_matrix((values_authority, (graph[0], graph[1])),
                               shape=shape, dtype=np.float)

    print "hyp_authority"


    del graph
    del values
    del values_m
    del velues_in_deg
    del velues_out_deg
    del velues_deg
    del values_local_clust
    del values_kcore
    del values_eigenvector_centr
    del values_hubs
    del values_authority
    del values_page_rank

    print "del"
    # i_indices = array.array(str("l"))
    # j_indices = array.array(str("l"))
    # values = array.array(str("d"))
    #
    # for s, targets in transitions.iteritems():
    #     for t, v in targets.iteritems():
    #         i_indices.append(vocab[s])
    #         j_indices.append(vocab[t])
    #         values.append(v)
    #
    # i_indices = np.frombuffer(i_indices, dtype=np.int_)
    # j_indices = np.frombuffer(j_indices, dtype=np.int_)
    # values = np.frombuffer(values, dtype=np.float64)

    #transitions = csr_matrix((values, (i_indices, j_indices)),
    #                         shape=shape)

    transitions = csr_matrix((transition_matrix[2], (transition_matrix[0], transition_matrix[1])),
                             shape=shape)

    del transition_matrix

    #delete all zero rows from all  see  http://stackoverflow.com/questions/31188141/scipy-sparse-matrix-remove-the-rows-whose-all-elements-are-zero
    print transitions.shape
    nonzero_row_indice, _ = transitions.nonzero()
    unique_nonzero_indice = np.unique(nonzero_row_indice)
    transitions = transitions[unique_nonzero_indice]
    print transitions.shape

    hyp_data = csr_matrix(transitions, copy=True)
    print hyp_data.shape

    hyp_structural = hyp_structural[unique_nonzero_indice]

    hyp_uniform = hyp_uniform[unique_nonzero_indice]

    hyp_structural_m = hyp_structural_m[unique_nonzero_indice]

    hyp_out_degree = hyp_out_degree[unique_nonzero_indice]

    hyp_in_degree = hyp_in_degree[unique_nonzero_indice]

    hyp_degree = hyp_degree[unique_nonzero_indice]

    hyp_page_rank = hyp_page_rank[unique_nonzero_indice]

    hyp_local_clust = hyp_local_clust[unique_nonzero_indice]

    hyp_kcore = hyp_kcore[unique_nonzero_indice]

    hyp_eigenvector_centr = hyp_eigenvector_centr[unique_nonzero_indice]

    hyp_hubs= hyp_hubs[unique_nonzero_indice]

    hyp_authority = hyp_authority[unique_nonzero_indice]

    hyp_sem_sim = csr_matrix((sem_sim_hyp[2], (sem_sim_hyp[0], sem_sim_hyp[1])),
                             shape=hyp_data.shape, dtype=np.float)


    #norm
    evidences_max_k={}
    for x in range(1,max_k+1):
        print "max_k"
        print x
        if linkocc == False:

            hyp_structural_nomred = norm_hyp(hyp_structural)
            print hyp_structural_nomred.shape
            print norm_hyp(hyp_structural_m).shape
            hyp_structural_m = hyp_structural_nomred.multiply(x*norm_hyp(hyp_structural_m))
            hyp_in_degree = hyp_structural_nomred.multiply(x*norm_hyp(hyp_in_degree))
            hyp_out_degree = hyp_structural_nomred.multiply(x*norm_hyp(hyp_out_degree))
            hyp_degree = hyp_structural_nomred.multiply(x*norm_hyp(hyp_degree))
            hyp_page_rank = hyp_structural_nomred.multiply(x*norm_hyp(hyp_page_rank))
            hyp_local_clust = hyp_structural_nomred.multiply(x*norm_hyp(hyp_local_clust))
            hyp_kcore = hyp_structural_nomred.multiply(x*norm_hyp(hyp_kcore))
            hyp_eigenvector_centr = hyp_structural_nomred.multiply(x*norm_hyp(hyp_eigenvector_centr))
            hyp_hubs = hyp_structural_nomred.multiply(x*norm_hyp(hyp_hubs))
            hyp_authority = hyp_structural_nomred.multiply(x*norm_hyp(hyp_authority))
            hyp_sem_sim = hyp_structural_nomred.multiply(x*norm_hyp(hyp_sem_sim))

        else:
            hyp_structural_m_nomred = norm_hyp(hyp_structural_m)


            hyp_structural = hyp_structural_m_nomred.multiply(x*norm_hyp(hyp_structural))
            hyp_in_degree = hyp_structural_m_nomred.multiply(x*norm_hyp(hyp_in_degree))
            hyp_out_degree = hyp_structural_m_nomred.multiply(x*norm_hyp(hyp_out_degree))
            hyp_degree = hyp_structural_m_nomred.multiply(x*norm_hyp(hyp_degree))
            hyp_page_rank = hyp_structural_m_nomred.multiply(x*norm_hyp(hyp_page_rank))
            hyp_local_clust = hyp_structural_m_nomred.multiply(x*norm_hyp(hyp_local_clust))
            hyp_kcore = hyp_structural_m_nomred.multiply(x*norm_hyp(hyp_kcore))
            hyp_eigenvector_centr = hyp_structural_m_nomred.multiply(x*norm_hyp(hyp_eigenvector_centr))
            hyp_hubs = hyp_structural_m_nomred.multiply(x*norm_hyp(hyp_hubs))
            hyp_authority = hyp_structural_m_nomred.multiply(x*norm_hyp(hyp_authority))
            hyp_sem_sim = hyp_structural_m_nomred.multiply(x*norm_hyp(hyp_sem_sim))




        ht = HypTrails(vocab)
        ht.fit(transitions)
        print "after fit"

        fig = plt.figure()
        ax = fig.add_subplot(111)

        r_first = 0.0001
        r = np.logspace(np.log10(r_first), np.log10(10000), 10)

        evidences_dict = {}
        evidences_dict['r'] = r
        evidences_dict['r_first'] = r_first

        # uniform hypothesis
        evidences = []
        for i in r:
            if i == r_first:
                evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
            else:
                evidences.append(ht.evidence(hyp_uniform,hyp_structural,k=i,norm=True))
        ax.plot(r, evidences, marker='o', clip_on = False, label="uniform", color='#FF3333', linestyle='--')
        print "uniform done"
        evidences_dict['uniform'] = evidences

        # structural hypothesis
        evidences = []
        for i in r:
            if i == r_first:
                evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
            else:
                evidences.append(ht.evidence(hyp_structural,hyp_structural,k=i,norm=True))
        ax.plot(r, evidences, marker='o', clip_on = False, label="structural", color='#FF8D33', linestyle='--')
        print "structural done"
        evidences_dict['structural'] = evidences

        # data hypothesis
        evidences = []
        for i in r:
            if i == r_first:
                evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
            else:
                evidences.append(ht.evidence(hyp_data,hyp_structural,k=i,norm=True))
        ax.plot(r, evidences, marker='o', clip_on = False, label="data", color='#A8FF33', linestyle='--')
        print "data done"
        evidences_dict['data'] = evidences

        evidences = []
        for i in r:
            if i == r_first:
                evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
            else:
                evidences.append(ht.evidence(hyp_structural_m,hyp_structural,k=i,norm=True))
        ax.plot(r, evidences, marker='o', clip_on = False, label="link occ.",  color='#33FF36', linestyle='--')
        print "structural_m done"
        evidences_dict['link occ.'] = evidences

        evidences = []
        for i in r:
            if i == r_first:
                evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
            else:
                evidences.append(ht.evidence(hyp_out_degree,hyp_structural,k=i,norm=True))
        ax.plot(r, evidences, marker='o', clip_on = False, label="out-degree",  color='#33FF96', linestyle='--')
        print "out degree done"
        evidences_dict['out degree'] = evidences


        evidences = []
        for i in r:
            if i == r_first:
                evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
            else:
                evidences.append(ht.evidence(hyp_in_degree,hyp_structural,k=i,norm=True))
        ax.plot(r, evidences, marker='o', clip_on = False, label="in-degree", color='#33FFE0', linestyle='--')
        print "in degree done"
        evidences_dict['in degree'] = evidences

        evidences = []
        for i in r:
            if i == r_first:
                evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
            else:
                evidences.append(ht.evidence(hyp_degree,hyp_structural,k=i,norm=True))
        ax.plot(r, evidences, marker='o', clip_on = False, label="degree", color='#33F3FF', linestyle='--')
        print "degree done"
        evidences_dict['degree'] = evidences

        evidences = []
        for i in r:
            if i == r_first:
                evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
            else:
                evidences.append(ht.evidence(hyp_page_rank,hyp_structural,k=i,norm=True))
        ax.plot(r, evidences, marker='o', clip_on = False, label="page rank", color='#33CAFF', linestyle='--')
        print "page_rank done"
        evidences_dict['page_rank'] = evidences

        evidences = []
        for i in r:
            if i == r_first:
                evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
            else:
                evidences.append(ht.evidence(hyp_local_clust,hyp_structural,k=i,norm=True))
        ax.plot(r, evidences, marker='o', clip_on = False, label="clust.", color='#339CFF', linestyle='--')
        print "clust done"
        evidences_dict['clust'] = evidences

        evidences = []
        for i in r:
            if i == r_first:
                evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
            else:
                evidences.append(ht.evidence(hyp_kcore,hyp_structural,k=i,norm=True))
        ax.plot(r, evidences, marker='o', clip_on = False, label="kcore", color='#3358FF', linestyle='--')
        print "kcore done"
        evidences_dict['kcore'] = evidences

        evidences = []
        for i in r:
            if i == r_first:
                evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
            else:
                evidences.append(ht.evidence(hyp_eigenvector_centr,hyp_structural,k=i,norm=True))
        ax.plot(r, evidences, marker='o', clip_on = False, label="eigen. centr.", color='#7133FF', linestyle='--')
        print "eigen done"
        evidences_dict['eigen'] = evidences

        evidences = []
        for i in r:
            if i == r_first:
                evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
            else:
                evidences.append(ht.evidence(hyp_hubs,hyp_structural,k=i,norm=True))
        ax.plot(r, evidences, marker='o', clip_on = False, label="hub", color='#D733FF', linestyle='--')
        print "hubs done"
        evidences_dict['hubs'] = evidences

        evidences = []
        for i in r:
            if i == r_first:
                evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
            else:
                evidences.append(ht.evidence(hyp_authority,hyp_structural,k=i,norm=True))
        ax.plot(r, evidences, marker='o', clip_on = False, label="authority", color='#FF33CE', linestyle='--')
        print "authority done"
        evidences_dict['authority'] = evidences

        evidences = []
        for i in r:
            if i == r_first:
                evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
            else:
                evidences.append(ht.evidence(hyp_sem_sim,hyp_structural,k=i,norm=True))
        ax.plot(r, evidences, marker='o', clip_on = False, label="sem. sim.", color='#FE0000', linestyle='--')
        print "sem sim done"
        evidences_dict['sem_sim'] = evidences
        evidences_max_k[x]=evidences_dict

    if linkocc==False:
        cPickle.dump(evidences_max_k, open("output/structural_additive_mult_normed_evidences_max_k", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)
    else:
        cPickle.dump(evidences_max_k, open("output/structural_linkocc_additive_mult_normed_evidences_max_k", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)


    # # further plotting
    # ax.set_xlabel("hypothesis weighting factor k")
    # ax.set_ylabel("marginal likelihood / evidence (log)")
    # # if we use log space for k then we need to set x also to log and improve the labels
    # ax.set_xscale("log")
    #
    # plt.grid(False)
    # ax.xaxis.grid(True)
    # handles, labels = ax.get_legend_handles_labels()
    # lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,-0.1), ncol=4)
    # if linkocc==False:
    #     plt.savefig('output/compare_structural_additive_mult_normed_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    #     cPickle.dump(evidences_dict, open("output/structural_additive_mult_normed_evidences", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)
    # else:
    #     plt.savefig('output/compare_structural_linkocc_additive_mult_normed_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    #     cPickle.dump(evidences_dict, open("output/structural_linkocc_additive_mult_normed_evidences", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)

    print "structural_evidences"


def norm_hyp(matrix):
    print "in norm_hyp"
    tmp = csr_matrix(matrix, copy=True)
    norm_h = tmp.sum(axis=1)
    n_nzeros = np.where(norm_h > 0)
    norm_h[n_nzeros] = 1.0 / norm_h[n_nzeros]
    norm_h = np.array(norm_h).T[0]
    print "in place mod"
    # modify sparse_csc_matrix in place
    csr_scale_rows(tmp.shape[0],
                   tmp.shape[1],
                   tmp.indptr,
                   tmp.indices,
                   tmp.data, norm_h)
    return tmp


def compare_engineered():
    #read vocab, graph, transitions
    #transitions = cPickle.load( open( SSD_HOME+"pickle/transitions", "rb" ) )
    transition_matrix = cPickle.load( open( SSD_HOME+"pickle/transition_matrix", "rb" ) )
    print "loaded transitions"
    graph = cPickle.load( open( SSD_HOME+"pickle/graph", "rb" ) )
    print "loaded graph"
    values = cPickle.load( open( SSD_HOME+"pickle/values", "rb" ) )
    values_kcore = cPickle.load( open( SSD_HOME+"pickle/values_kcore", "rb" ) )

    # transform kcore values to model going out of the kcore
    values_kcore = [1./np.sqrt(float(x)) for x in values_kcore]
    print 'kcore values tranfsormation'

    sem_sim_hyp = cPickle.load( open( SSD_HOME+"pickle/sem_sim_hyp", "rb" ) )
    print "sem_sim_hyp values"

    lead_hyp = cPickle.load( open( SSD_HOME+"pickle/lead_hyp", "rb" ) )
    infobox_hyp = cPickle.load( open( SSD_HOME+"pickle/infobox_hyp", "rb" ) )
    left_body_hyp = cPickle.load( open( SSD_HOME+"pickle/left-body_hyp", "rb" ) )
    print "gamma values"

    vocab = cPickle.load( open( SSD_HOME+"pickle/vocab", "rb" ) )
    print "loaded vocab"

    state_count = len(vocab)
    states = vocab.keys()
    shape = (state_count, state_count)

    # we can use an empty matrix here as the HypTrails class then
    # properly distributes the chips for elicitation
    hyp_uniform = csr_matrix((state_count,state_count))
    print "hyp uniform"

    hyp_structural = csr_matrix((values, (graph[0], graph[1])),
                                shape=shape, dtype=np.float)


    hyp_kcore = csr_matrix((values_kcore, (graph[0], graph[1])),
                           shape=shape, dtype=np.float)
    print "hyp_kcore"

    del graph
    del values_kcore

    print "after delete"

    transitions = csr_matrix((transition_matrix[2], (transition_matrix[0], transition_matrix[1])),
                             shape=shape)
    print "transitions"

    del transition_matrix
    print " delete transitions"

    #delete all zero rows from all  see  http://stackoverflow.com/questions/31188141/scipy-sparse-matrix-remove-the-rows-whose-all-elements-are-zero
    print transitions.shape
    nonzero_row_indice, _ = transitions.nonzero()
    unique_nonzero_indice = np.unique(nonzero_row_indice)
    transitions = transitions[unique_nonzero_indice]
    print transitions.shape

    hyp_data = csr_matrix(transitions, copy=True)
    print hyp_data.shape

    hyp_structural = hyp_structural[unique_nonzero_indice]

    hyp_kcore = hyp_kcore[unique_nonzero_indice]


    hyp_sem_sim = csr_matrix((sem_sim_hyp[2], (sem_sim_hyp[0], sem_sim_hyp[1])),
                             shape=hyp_data.shape, dtype=np.float)
    print hyp_sem_sim.shape
    del sem_sim_hyp


    hyp_lead = csr_matrix((lead_hyp[2], (lead_hyp[0], lead_hyp[1])),
                          shape=hyp_data.shape, dtype=np.float)
    print hyp_lead.shape

    hyp_infobox = csr_matrix((infobox_hyp[2], (infobox_hyp[0], infobox_hyp[1])),
                             shape=hyp_data.shape, dtype=np.float)
    print hyp_infobox.shape


    hyp_left_body = csr_matrix((left_body_hyp[2], (left_body_hyp[0], left_body_hyp[1])),
                               shape=hyp_data.shape, dtype=np.float)
    print hyp_left_body.shape

    del lead_hyp
    del infobox_hyp
    del left_body_hyp

    #add the visual hyps to one matrix and set all non zero fields to 1.0
    print 'before gamma'
    hyp_gamma = hyp_left_body + hyp_infobox + hyp_lead
    hyp_gamma.data = np.ones_like(hyp_gamma.data, dtype=np.float)
    print 'after gamma'




    ht = HypTrails(vocab)
    ht.fit(transitions)
    print "after fit"

    fig = plt.figure()
    ax = fig.add_subplot(111)

    r_first = 0.0001
    r = np.logspace(np.log10(r_first), np.log10(10000), 9)

    evidences_dict = {}
    evidences_dict['r'] = r
    evidences_dict['r_first'] = r_first

    #norm
    print "in norm each "
    hyp_structural = norm_hyp(hyp_structural)
    hyp_kcore = norm_hyp(hyp_kcore)
    hyp_sem_sim = norm_hyp(hyp_sem_sim)
    hyp_gamma = norm_hyp(hyp_gamma)

    #engineering of hypos
    hyp_kcore_struct = hyp_structural + hyp_kcore
    hyp_sem_sim_struct = hyp_structural + hyp_sem_sim
    hyp_visual_struct = hyp_structural + hyp_gamma

    hyp_mix_semsim_kcore = hyp_kcore + hyp_sem_sim
    hyp_mix_semsim_visual = hyp_sem_sim + hyp_gamma
    hyp_mix_kcore_visual= hyp_kcore + hyp_gamma


    hyp_all = hyp_kcore + hyp_sem_sim + hyp_gamma
    hyp_all_struct =  hyp_kcore + hyp_sem_sim + hyp_gamma + hyp_structural

    print 'test hypos'

    # structural hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_structural,hyp_structural,k=i,norm=True))
    evidences_dict['structural'] = evidences
    evidences = list(np.array(evidences).astype(float) - evidences)
    evidences_dict['structural_rel'] = evidences
    ax.plot(r, evidences, marker='o', clip_on = False, label="structural", color='b', linestyle='--')
    print "structural done"


    # evidences = []
    # for i in r:
    #     if i == r_first:
    #         evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
    #     else:
    #         evidences.append(ht.evidence(hyp_sem_sim,hyp_structural,k=i,norm=True))
    # evidences_dict['sem_sim'] = evidences
    # evidences = list(np.array(evidences).astype(float) - evidences_dict['structural'])
    # evidences_dict['sem_sim_rel'] = evidences
    # ax.plot(r, evidences, marker='o', clip_on = False, label="sem_sim", color='g', linestyle='--')
    # print "sem_sim done"

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_sem_sim_struct,hyp_structural,k=i,norm=True))
    evidences_dict['sem_sim_struct'] = evidences
    evidences = list(np.array(evidences).astype(float) - evidences_dict['structural'])
    evidences_dict['sem_sim_struct_rel'] = evidences
    ax.plot(r, evidences, marker='d', clip_on = False, label="sem_sim_struct", color='r', linestyle='--')
    print "sem_sim_struct done"

    # evidences = []
    # for i in r:
    #     if i == r_first:
    #         evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
    #     else:
    #         evidences.append(ht.evidence(hyp_kcore,hyp_structural,k=i,norm=True))
    # evidences_dict['kcore'] = evidences
    # evidences = list(np.array(evidences).astype(float) - evidences_dict['structural'])
    # evidences_dict['kcore_rel'] = evidences
    # ax.plot(r, evidences, marker='o', clip_on = False, label="kcore", color='r', linestyle='--')
    # print "kcore done"

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_kcore_struct,hyp_structural,k=i,norm=True))
    evidences_dict['kcore_struct'] = evidences
    evidences = list(np.array(evidences).astype(float) - evidences_dict['structural'])
    evidences_dict['kcore_struct_rel'] = evidences
    ax.plot(r, evidences, marker='o', clip_on = False, label="kcore_struct", color='r', linestyle='--')
    print "kcore_struct done"

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_visual_struct,hyp_structural,k=i,norm=True))
    evidences_dict['visual_struct'] = evidences
    evidences = list(np.array(evidences).astype(float) - evidences_dict['structural'])
    evidences_dict['visual_struct_rel'] = evidences
    ax.plot(r, evidences, marker='o', clip_on = False, label="visual_struct", color='c', linestyle='--')
    print "visual_struct done"

    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_mix_semsim_kcore,hyp_structural,k=i,norm=True))
    evidences_dict['mix_semsim_kcore'] = evidences
    evidences = list(np.array(evidences).astype(float) - evidences_dict['structural'])
    evidences_dict['mix_semsim_kcore_rel'] = evidences
    ax.plot(r, evidences, marker='o', clip_on = False, label="mix_semsim_kcore", color='m', linestyle='--')
    print "mix_semsim_kcore done"


    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_mix_semsim_visual,hyp_structural,k=i,norm=True))
    evidences_dict['mix_semsim_visual'] = evidences
    evidences = list(np.array(evidences).astype(float) - evidences_dict['structural'])
    evidences_dict['mix_semsim_visual_rel'] = evidences
    ax.plot(r, evidences, marker='o', clip_on = False, label="mix_semsim_visual", color='y', linestyle='--')
    print "mix_semsim_visual done"




    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_mix_kcore_visual,hyp_structural,k=i,norm=True))
    evidences_dict['mix_kcore_visual'] = evidences
    evidences = list(np.array(evidences).astype(float) - evidences_dict['structural'])
    evidences_dict['mix_kcore_visual_rel'] = evidences
    ax.plot(r, evidences, marker='o', clip_on = False, label="mix_kcore_visual", color='k', linestyle='--')
    print "mix_kcore_visual done"



    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_all,hyp_structural,k=i,norm=True))
    evidences_dict['all'] = evidences
    evidences = list(np.array(evidences).astype(float) - evidences_dict['structural'])
    evidences_dict['all_rel'] = evidences
    ax.plot(r, evidences, marker='d', clip_on = False, label="all", color='b', linestyle='--')
    print "all done"


    #
    # evidences = []
    # for i in r:
    #     if i == r_first:
    #         evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
    #     else:
    #         evidences.append(ht.evidence(hyp_all_struct,hyp_structural,k=i,norm=True))
    # evidences_dict['all_struct'] = evidences
    # evidences = list(np.array(evidences).astype(float) - evidences_dict['structural'])
    # evidences_dict['all_struct_rel'] = evidences
    # ax.plot(r, evidences, marker='d', clip_on = False, label="all_struct", color='g', linestyle='--')
    # print "all_struct done"




    # further plotting
    ax.set_xlabel("hypothesis weighting factor k")
    ax.set_ylabel("marginal likelihood / evidence (log)")
    # if we use log space for k then we need to set x also to log and improve the labels
    ax.set_xscale("log")

    plt.grid(False)
    ax.xaxis.grid(True)
    handles, labels = ax.get_legend_handles_labels()
    lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,-0.1), ncol=4)

    plt.savefig('output/compare_engineered_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    cPickle.dump(evidences_dict, open("output/compare_engineered_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)


    print "engineered_evidences"


def compare_engineered_struct():
    #read vocab, graph, transitions
    #transitions = cPickle.load( open( SSD_HOME+"pickle/transitions", "rb" ) )
    transition_matrix = cPickle.load( open( SSD_HOME+"pickle/transition_matrix", "rb" ) )
    print "loaded transitions"
    graph = cPickle.load( open( SSD_HOME+"pickle/graph", "rb" ) )
    print "loaded graph"
    values = cPickle.load( open( SSD_HOME+"pickle/values", "rb" ) )
    values_kcore = cPickle.load( open( SSD_HOME+"pickle/values_kcore", "rb" ) )

    # transform kcore values to model going out of the kcore
    values_kcore = [1./np.sqrt(float(x)) for x in values_kcore]
    print 'kcore values tranfsormation'

    sem_sim_hyp = cPickle.load( open( SSD_HOME+"pickle/sem_sim_hyp", "rb" ) )
    print "sem_sim_hyp values"

    lead_hyp = cPickle.load( open( SSD_HOME+"pickle/lead_hyp", "rb" ) )
    infobox_hyp = cPickle.load( open( SSD_HOME+"pickle/infobox_hyp", "rb" ) )
    left_body_hyp = cPickle.load( open( SSD_HOME+"pickle/left-body_hyp", "rb" ) )
    print "gamma values"

    vocab = cPickle.load( open( SSD_HOME+"pickle/vocab", "rb" ) )
    print "loaded vocab"

    state_count = len(vocab)
    states = vocab.keys()
    shape = (state_count, state_count)

    # we can use an empty matrix here as the HypTrails class then
    # properly distributes the chips for elicitation
    hyp_uniform = csr_matrix((state_count,state_count))
    print "hyp uniform"

    hyp_structural = csr_matrix((values, (graph[0], graph[1])),
                                shape=shape, dtype=np.float)


    hyp_kcore = csr_matrix((values_kcore, (graph[0], graph[1])),
                           shape=shape, dtype=np.float)
    print "hyp_kcore"

    del graph
    del values_kcore

    print "after delete"

    transitions = csr_matrix((transition_matrix[2], (transition_matrix[0], transition_matrix[1])),
                             shape=shape)
    print "transitions"

    del transition_matrix
    print " delete transitions"

    #delete all zero rows from all  see  http://stackoverflow.com/questions/31188141/scipy-sparse-matrix-remove-the-rows-whose-all-elements-are-zero
    print transitions.shape
    nonzero_row_indice, _ = transitions.nonzero()
    unique_nonzero_indice = np.unique(nonzero_row_indice)
    transitions = transitions[unique_nonzero_indice]
    print transitions.shape

    hyp_data = csr_matrix(transitions, copy=True)
    print hyp_data.shape

    hyp_structural = hyp_structural[unique_nonzero_indice]

    hyp_kcore = hyp_kcore[unique_nonzero_indice]


    hyp_sem_sim = csr_matrix((sem_sim_hyp[2], (sem_sim_hyp[0], sem_sim_hyp[1])),
                             shape=hyp_data.shape, dtype=np.float)
    print hyp_sem_sim.shape
    del sem_sim_hyp


    hyp_lead = csr_matrix((lead_hyp[2], (lead_hyp[0], lead_hyp[1])),
                          shape=hyp_data.shape, dtype=np.float)
    print hyp_lead.shape

    hyp_infobox = csr_matrix((infobox_hyp[2], (infobox_hyp[0], infobox_hyp[1])),
                             shape=hyp_data.shape, dtype=np.float)
    print hyp_infobox.shape


    hyp_left_body = csr_matrix((left_body_hyp[2], (left_body_hyp[0], left_body_hyp[1])),
                               shape=hyp_data.shape, dtype=np.float)
    print hyp_left_body.shape

    del lead_hyp
    del infobox_hyp
    del left_body_hyp

    #add the visual hyps to one matrix and set all non zero fields to 1.0
    print 'before gamma'
    hyp_gamma = hyp_left_body + hyp_infobox + hyp_lead
    hyp_gamma.data = np.ones_like(hyp_gamma.data, dtype=np.float)
    print 'after gamma'




    ht = HypTrails(vocab)
    ht.fit(transitions)
    print "after fit"

    fig = plt.figure()
    ax = fig.add_subplot(111)

    r_first = 0.0001
    r = np.logspace(np.log10(r_first), np.log10(10000), 9)


    evidences_dict = {}
    evidences_dict['r'] = r
    evidences_dict['r_first'] = r_first

    #norm
    print "in norm each "
    hyp_structural = norm_hyp(hyp_structural)
    hyp_kcore = norm_hyp(hyp_kcore)
    hyp_sem_sim = norm_hyp(hyp_sem_sim)
    hyp_gamma = norm_hyp(hyp_gamma)

    #engineering of hypos
    hyp_mix_semsim_kcore = hyp_structural+hyp_kcore + hyp_sem_sim
    hyp_mix_semsim_visual = hyp_structural+hyp_sem_sim + hyp_gamma
    hyp_mix_kcore_visual= hyp_structural+hyp_kcore + hyp_gamma



    print 'test hypos'

    # structural hypothesis
    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_structural,hyp_structural,k=i,norm=True))
    evidences_dict['structural'] = evidences
    evidences = list(np.array(evidences).astype(float) - evidences)
    evidences_dict['structural_rel'] = evidences
    ax.plot(r, evidences, marker='o', clip_on = False, label="structural", color='b', linestyle='--')
    print "structural done"



    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_mix_semsim_kcore,hyp_structural,k=i,norm=True))
    evidences_dict['mix_semsim_kcore'] = evidences
    evidences = list(np.array(evidences).astype(float) - evidences_dict['structural'])
    evidences_dict['mix_semsim_kcore_rel'] = evidences
    ax.plot(r, evidences, marker='o', clip_on = False, label="mix_semsim_kcore", color='m', linestyle='--')
    print "mix_semsim_kcore done"


    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_mix_semsim_visual,hyp_structural,k=i,norm=True))
    evidences_dict['mix_semsim_visual'] = evidences
    evidences = list(np.array(evidences).astype(float) - evidences_dict['structural'])
    evidences_dict['mix_semsim_visual_rel'] = evidences
    ax.plot(r, evidences, marker='o', clip_on = False, label="mix_semsim_visual", color='y', linestyle='--')
    print "mix_semsim_visual done"




    evidences = []
    for i in r:
        if i == r_first:
            evidences.append(ht.evidence(csr_matrix(hyp_data.shape),hyp_structural,i))
        else:
            evidences.append(ht.evidence(hyp_mix_kcore_visual,hyp_structural,k=i,norm=True))
    evidences_dict['mix_kcore_visual'] = evidences
    evidences = list(np.array(evidences).astype(float) - evidences_dict['structural'])
    evidences_dict['mix_kcore_visual_rel'] = evidences
    ax.plot(r, evidences, marker='o', clip_on = False, label="mix_kcore_visual", color='k', linestyle='--')
    print "mix_kcore_visual done"





    # further plotting
    ax.set_xlabel("hypothesis weighting factor k")
    ax.set_ylabel("marginal likelihood / evidence (log)")
    # if we use log space for k then we need to set x also to log and improve the labels
    ax.set_xscale("log")

    plt.grid(False)
    ax.xaxis.grid(True)
    handles, labels = ax.get_legend_handles_labels()
    lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,-0.1), ncol=4)

    plt.savefig('output/compare_engineered_struct_hypothesises.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    cPickle.dump(evidences_dict, open("output/compare_engineered_struct_hypothesises.obj", "wb"), protocol=cPickle.HIGHEST_PROTOCOL)


    print "engineered_evidences_struct"


def generate_plot():
    evidences_dict = cPickle.load( open( "output/compare_engineered_hypothesises.obj", "rb" ) )
    print evidences_dict
    #evidences_dict_struct = cPickle.load( open( "output/compare_engineered_struct_hypothesises.obj", "rb" ) )
    #evidences_dict.update(evidences_dict_struct)
    #print evidences_dict
    fig = plt.figure()
    ax = fig.add_subplot(111)

    r_first = 0.0001
    r = np.logspace(np.log10(r_first), np.log10(10000), 9)

    markers = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd']
    i=0
    last_evidences={}


    print evidences_dict.keys()
    labels = {'visual_struct_rel':'visual',  'all_rel':'kcore+visual+text_sim', 'structural_rel':'baseline', 'mix_semsim_kcore_rel':'text_sim+kcore',  'kcore_struct_rel':'kcore', 'mix_kcore_visual_rel':'kcore+visual',   'mix_semsim_visual_rel':'text_sim+visual', 'sem_sim_struct_rel':'text_sim'}
    for key, evidences in evidences_dict.iteritems():
        if  key in ['visual_struct_rel',  'all_rel', 'structural_rel', 'mix_semsim_kcore_rel',  'kcore_struct_rel', 'mix_kcore_visual_rel',   'mix_semsim_visual_rel', 'sem_sim_struct_rel']:
            last_evidences[key] = evidences[-1]



    print last_evidences
    sorted_x = sorted(last_evidences.items(), key=operator.itemgetter(1))
    for key in sorted_x:
        if 'structural' in  key[0]:
            ax.plot(r, evidences_dict[key[0]],  markersize=3, markeredgecolor='none', clip_on = False,
                    label=labels[key[0]], marker=markers[i], color='black', linestyle='-')
            i+=1
        elif 'all_rel' in key[0]:
            ax.plot(r, evidences_dict[key[0]],  markersize=3, markeredgecolor='none', clip_on = False,
                    label=labels[key[0]],  marker=markers[i], linestyle='-')
            i+=1
        else:
            ax.plot(r, evidences_dict[key[0]],  markersize=3, markeredgecolor='none', clip_on = False,
                    label=labels[key[0]],  marker=markers[i], linestyle='-')
            i+=1

    # further plotting
    ax.set_xlabel(r'Hypothesis weighting factor $\kappa$')
    ax.set_ylabel(r'Bayes factor')
    # if we use log space for k then we need to set x also to log and improve the labels
    ax.set_xscale("log")

    x_ticks_labels = ['0', '0', r'$10^{-3}$', r'$10^{-2}$', r'$10^{-1}$', r'$10^0$', r'$10^1$', r'$10^2$', r'$10^3$', r'$10^4$', r'$10^5$']
    print x_ticks_labels
    #labels=range(1,12)

    ax.set_xticklabels(x_ticks_labels)


    plt.grid(False)
    ax.xaxis.grid(True)
    handles, labels = ax.get_legend_handles_labels()
    lgd = ax.legend(handles[::-1], labels[::-1], fancybox=True,loc=3,bbox_to_anchor=(0., 1.1, 1., .11), ncol=3, mode="expand",
                   borderaxespad=0., prop={'size':5})
    #ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
    #           ncol=2, mode="expand", borderaxespad=0.)
    #reverse labels order
    #lgd = ax.legend(handles[::-1], labels[::-1], fancybox=True, loc=2, bbox_to_anchor=(1.05, 1), ncol=1, borderaxespad=0., prop={'size':5})
    ylim = ax.get_ylim()
    print ylim
    ax.set_ylim((-20000000.0, 510000000.0))


    plt.savefig('output/compare_engineered_hypothesises_labels.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')


if __name__ == '__main__':
    #compare_structural(False, False)
    #compare_structural(False, True)
    #compare_structural(True, False)
    #compare_structural(True, True)
    #compare_sem_sim(False, False)
    #compare_sem_sim(False, True)
    #compare_sem_sim(True, False)
    #compare_sem_sim(True, True)
    #compare_relative_positive(False, False)
    #compare_relative_positive(False, Treu)
    #compare_relative_positive(True, False)
    #compare_relative_positive(True, True)
    #compare_relative_negative(False, False)
    #compare_relative_negative(False, True)
    #compare_relative_negative(True, False)
    #compare_relative_negative(True, True)
    #compare_vusual(False, False)
    #compare_vusual(False, True)
    #compare_vusual(True, False)
    #compare_vusual(True, True)

    #compare_engineered()
    #compare_engineered_struct()

    #compare_structural_page_rank(False, False)
    #compare_structural_page_rank(False, True)
    #compare_structural_page_rank(True, False)
    #compare_structural_page_rank(True, True)


    #compare_structural_additive_nomred(False)
    #compare_structural_additive_nomred(True)
    #compare_structural_additive_mult_nomred(False, 5)
    #compare_structural_additive_mult_nomred(True, 5)

    generate_plot()

