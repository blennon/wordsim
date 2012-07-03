'''
Created on Jul 1, 2012

@author: bill
'''
import sys
sys.path.append('../')
from sklearn.decomposition import RandomizedPCA as PCA
from similarity import SVDSim

class PCASim(SVDSim):

    def transform_data(self, occurs, d):
        '''
        perform PCA on probability matrix with d PCs
        
        return data transformed into similarity space
        '''
        pca = PCA(n_components=d)
        probs = counts_to_probs(occurs).tocsr()
        pca_mat = pca.fit_transform(probs)
        return SVDSim._norm_mat(pca_mat)
