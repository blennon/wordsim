'''
Created on Jul 1, 2012

@author: bill
'''
import sys
import numpy as np
from scipy.sparse.linalg import svds
import cPickle as pickle
from data_preprocess import *
sys.modules['lexicon'] = lexicon
from similarity import *

class SVDSim(Similarity):
    
    def __init__(self, occurs, lexicon, d=200):
        '''
        d: number of singular values to compute
        '''
        self.lex = lexicon
        self.SS = self.transform_data(occurs,d)
        del occurs

    def transform_data(self, occurs, d):
        '''
        perform sparse svd on the data with d SVs
        
        return data transformed into similarity space
        '''
        probs = counts_to_probs(occurs)
        P,D,Qt = svds(occurs,d)
        return SVDSim._norm_mat(P*D)
    
    def query(self, item, N):
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
        sims = np.dot(self.SS,vec)
        sort_index = np.argsort(sims)
        sort_index = sort_index[::-1][0:N] #descending order, N of them

        v = []
        for ind,sim in zip(sort_index,sims[sort_index]):
            v.append((self.lex[ind],sim))
        print v
        return v
        
    @staticmethod
    def _norm_mat(mat):
        norm = (mat**2).sum(axis=1)**.5
        return mat / norm[...,None]
        
if __name__ == '__main__':
    NO = pickle.load(open('/var/wordsim/preprocessed_7.2.12/ngram_occurs.p','rb'))
    L = NO.lex
    del sys.modules['lexicon']
    S = SVDSim(NO.get_occurs(concat=True),L,d=100)
    S.query('is',6)
        