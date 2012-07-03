import numpy as np
import scipy as sp
from scipy.sparse import *

def counts_to_probs(count_mat):
    '''
    convert a sparse co-occur matrix to a sparse
    probability matrix (normalized by column sum)
    '''
    colsums = count_mat.sum(axis=0)
    colsums = np.squeeze(np.asarray(colsums))
    for i in xrange(len(colsums)):
        if colsums[i] > 0: colsums[i] = 1/float(colsums[i])
    diag = lil_matrix((np.shape(count_mat)[1],np.shape(count_mat)[1]))
    diag.setdiag(colsums)
    
    return sp.dot(count_mat,diag)

def prune_counts(counts):
    pass

def prune_probs(probs):
    pass

def prune_by_MI():
    'prune by mutual information'
    pass
