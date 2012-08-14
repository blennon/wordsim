'''
Created on Jul 1, 2012

@author: bill
'''
import sys
sys.path.append('../')
import numpy as np
from scipy.sparse.linalg import svds
#from sparsesvd import sparsesvd as svds
import cPickle as pickle
from data_preprocess import *
#sys.modules['lexicon'] = lexicon
from similarity import *

class SVDSim(Similarity):

    def transform_data(self, occurs, d, min_prob=1e-3):
        '''
        perform sparse svd on the data with d SVs
        
        return data transformed into similarity space
        '''
        probs = counts_to_probs(occurs)
        probs = prune_by_min(probs,min_prob)
        P,D,Qt = svds(probs,d)
        if self.norm_ss:
            return SVDSim._norm_mat(P*D)
        else:
            return P*D
