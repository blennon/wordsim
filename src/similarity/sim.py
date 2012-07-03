'''
Created on Jul 1, 2012

@author: bill
'''
import sys
sys.path.append('../')
import numpy as np
from scipy.sparse.linalg import svds
import cPickle as pickle
from data_preprocess import *
sys.modules['lexicon'] = lexicon
from similarity import *

class Similarity(AbstractSimilarity):
    
    def __init__(self, occurs, lexicon, d=200, norm_ss=True):
        '''
        d: number of singular values to compute
        '''
        self.lex = lexicon
        self.norm_ss = norm_ss
        self.SS = self.transform_data(occurs,d)
        del occurs
    
    def query(self, item, N, metric='dot'):
        if isinstance(item,str):
            try:
                ind = self.lex[item]
            except KeyError:
                print '%s does not exist in lexicon' % (item)
                return
        elif isinstance(item,int):
            ind = item
        else:
            print 'Need either a string or int as input'
            return
        
        vec = self.SS[ind,:]
        sims, sort_index = self.order_similarity(vec, N, metric)

        v = []
        for ind,sim in zip(sort_index,sims[sort_index]):
            v.append((self.lex[ind],sim))
            
        return v
    
    def order_similarity(self, vec, N, metric):
        '''return a list of similarity values and their indices in the SimSpace'''
        if metric == 'dot':
            sims = np.dot(self.SS,vec)
            sort_index = np.argsort(sims)[::-1][0:N] #descend order, N of them
        elif metric == 'euclidean':
            sims = Similarity.euclid_dist(self.SS,vec)
            sort_index = np.argsort(sims)[0:N]
        else:
            raise Exception('metric must be either euclidean or dot')
        
        return sims, sort_index
        
    @staticmethod
    def euclid_dist(mat,vec):
        '''
        computes the cos distance between 'vec' and each row
        in 'mat' (smaller is better)
        '''
        diff = mat - vec
        return (diff**2).sum(axis=1)**.5
    
    @staticmethod
    def _norm_mat(mat):
        '''normalizes each row in 'mat' by their l2 norm'''
        norm = (mat**2).sum(axis=1)**.5
        return mat / norm[...,None]


