# further implementations can be found:
# Python: https://github.com/psinger/hyptrails
# Java: https://bitbucket.org/florian_lemmerich/hyptrails4j
# Apache spark: http://dmir.org/sparktrails/
# also see: http://www.philippsinger.info/hyptrails/

from __future__ import division

import itertools
from scipy.sparse import csr_matrix
from scipy.special import gammaln
from collections import defaultdict
from sklearn.preprocessing import normalize
from scipy.sparse.sparsetools import csr_scale_rows
import numpy as np

class HypTrails():
    """
    HypTrails
    """

    def __init__(self, vocab=None):
        """
        Constructor for class HypTrails

        Args:
            vocab: optional vocabulary mapping states to indices
        """

        self.vocab = vocab
        self.state_count = len(vocab)

    def fit(self, transitions_matrix):
        """
        Function for fitting the Markov Chain model given data

        Args:
            sequences: Data of sequences, list of lists
        """


        self.transitions = transitions_matrix

        #print "fit done"

    def evidence(self, hypothesis, structur, k=1, prior=1., norm=True):
        """
        Determines Bayesian evidence given fitted model and hypothesis

        Args:
            hypothesis: Hypothesis csr matrix,
                        indices need to map those of transition matrix
            k: Concentration parameter k
            prior: proto Dirichlet prior
            norm: Flag for normalizing hypothesis matrix
        Returns
            evidence
        """

        # care with copy here
        hypothesis = csr_matrix(hypothesis, copy=True)

        structur = csr_matrix(structur, copy=True)

        pseudo_counts = k * self.state_count

        if hypothesis.size != 0:
            # in case of memory issues set copy to False but then care about changed hypothesis matrix
            if norm == True:
                #print "in norm"
                norm_h = hypothesis.sum(axis=1)
                n_nzeros = np.where(norm_h > 0)
                norm_h[n_nzeros] = 1.0 / norm_h[n_nzeros]
                norm_h = np.array(norm_h).T[0]
                #print "in place mod"
                # modify sparse_csc_matrix in place
                csr_scale_rows(hypothesis.shape[0],
                                  hypothesis.shape[1],
                                  hypothesis.indptr,
                                  hypothesis.indices,
                                  hypothesis.data, norm_h)


                # distribute pseudo counts to matrix, row-based approach
                hypothesis = hypothesis * pseudo_counts
                #print "after pseude counts"
                # also consider those rows which only include zeros
                norma = hypothesis.sum(axis=1)
                n_zeros,_ = np.where(norma == 0)
                hypothesis[n_zeros,:] = pseudo_counts / self.state_count
            else:
                #print "in norm"
                norm_h = hypothesis.sum(axis=1)
                n_nzeros = np.where(norm_h > 0)
                norm_h[n_nzeros] = 1.0 / norm_h[n_nzeros]
                norm_h = np.array(norm_h).T[0]
                #print "in place mod"
                # modify sparse_csc_matrix in place
                csr_scale_rows(hypothesis.shape[0],
                               hypothesis.shape[1],
                               hypothesis.indptr,
                               hypothesis.indices,
                               hypothesis.data, norm_h)


                # distribute pseudo counts to matrix, row-based approach
                #TODO check if this line should be placed after the zero_rows_norm() call????
                hypothesis = hypothesis * pseudo_counts

                #self.zero_rows_norm(hypothesis, structur,k)
                self.zero_rows_norm_eff1(hypothesis, structur, k)

        else:
            # if hypothesis matrix is empty, we can simply increase the proto prior parameter
            prior += k

        # transition matrix with additional Dirichlet prior
        # not memory efficient
        transitions_prior = self.transitions.copy()
        transitions_prior = transitions_prior + hypothesis
        #print "after copy"
        # elegantly calculate evidence
        evidence = 0
        evidence += gammaln(hypothesis.sum(axis=1)+self.state_count*prior).sum()
        evidence -= gammaln(self.transitions.sum(axis=1)+hypothesis.sum(axis=1)+self.state_count*prior).sum()
        evidence += gammaln(transitions_prior.data+prior).sum()
        evidence -= gammaln(hypothesis.data+prior).sum() + (len(transitions_prior.data)-len(hypothesis.data)) * gammaln(prior)
        return evidence

    def zero_rows_norm(self, hypothesis, structur,k):
        norma = hypothesis.sum(axis=1)
        n_zeros = np.where(norma == 0)
        print 'n_zeros'
        print len(n_zeros[0])
        for x, i in enumerate(n_zeros[0]):
            if x % 1000 == 0:
                print x, len(n_zeros[0])
            links = np.where(structur[i,:]!=0)
            hypothesis[i,links[0]] = k / len(links[0])
        print 'n_zeros done'


    # def zero_rows_norm_eff(self,hypothesis, structur):
    #     #find zero sum rows in hypothesis
    #     print 'sum hyp'
    #     norma = hypothesis.sum(axis=1)
    #     n_zeros = np.where(norma == 0)
    #     # norm the structure matrix
    #     print 'sum structure'
    #     tmp = structur[n_zeros]
    #     norm_s = tmp.sum(axis=1)
    #     norm_s = np.array(norm_s).T[0]
    #     tmp = tmp/norm_s[:,None]
    #     #replece the zero rows in hypothesis with the corresponding rows in the normed strcuture matrix
    #     print 'replace'
    #     hypotheis[n_zeros,:]=tmp[n_zeros,:]

    def zero_rows_norm_eff1(self,hypothesis, structur, k):
        #find zero sum rows in hypothesis
        #print 'sum hyp'
        norma = hypothesis.sum(axis=1)
        n_zeros = np.where(norma == 0)
        # norm the structure matrix
        i_index = list()
        j_index = list()
        values = list()
        for x, i in enumerate(n_zeros[0]):
            #if x % 1000 == 0:
            #    print x, len(n_zeros[0])
            links = np.where(structur[i,:]!=0)
            value = k / len(links[0])
            for j in links[0]:
                i_index.append(i)
                j_index.append(j)
                values.append(value)
        hypothesis= hypothesis+csr_matrix((values, (i_index, j_index)),
                                          shape=hypothesis.shape, dtype=np.float)
