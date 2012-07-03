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

    def transform_data(self, occurs, d):
        '''
        perform sparse svd on the data with d SVs
        
        return data transformed into similarity space
        '''
        probs = counts_to_probs(occurs)
        P,D,Qt = svds(occurs,d)
        return SVDSim._norm_mat(P*D)

