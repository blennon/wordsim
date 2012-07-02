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

        return v
        
    @staticmethod
    def _norm_mat(mat):
        norm = (mat**2).sum(axis=1)**.5
        return mat / norm[...,None]


def print_query(q_list):
    '''print the query results nicely'''
    print '='*50
    print 'Query results for: %s' % q_list[0][0]
    for q in q_list[1:]:
        print q[0], q[1]
    print '='*50
    print ''

if __name__ == '__main__':

    print 'loading data...'
    NO = pickle.load(open(sys.argv[1],'rb'))
    L = NO.lex
    del sys.modules['lexicon']

    print 'transforming data...'
    S = SVDSim(NO.get_occurs(concat=True),L,d=200)

    print 'Ready for queries.'
    while True:
        q = raw_input('enter word to query for:')
        print_query(S.query(q,5))
