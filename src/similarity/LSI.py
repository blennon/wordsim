'''
Generalized implementation of LSI for co-occurrence matrices where each
dimension can have a different set of tokens it represents
'''
from pylab import *
from scipy.sparse.linalg import svds

class LSI(object):
    
    def __init__(self, occurs,tokens1,tokens2, n_sing):
        '''tokens are instances of Tokens class'''
        self.tokens1, self.tokens2 = tokens1, tokens2
        
        print 'performing sparse svd...'
        P,D,Qt = svds(occurs,n_sing)
        
        print 'building token spaces...'
        self.T1, self.T2 = LSI._norm_mat(P*D), LSI._norm_mat((D*Qt).T)
        del P,D,Qt
        
    def query(self, token, token_type, N):
        '''query for N tokens similar to token of type token_type'''
        if token_type == 1:
            id = self.tokens1.token2id(token)
            T,tokens = self.T1,self.tokens1
        elif token_type ==2:
            id = self.tokens2.token2id(token)
            T,tokens = self.T2, self.tokens2
        else:
            raise Exception('token_type specifies which token space (matrix, i.e. T1/T2) to use')
            
        t = T[id,:]
        sims = np.dot(T,t)
        sort_index = np.argsort(sims)[::-1][0:N] #descend order, N of them
        
        v = []
        for ind,sim in zip(sort_index,sims[sort_index]):
            v.append((tokens.id2token(ind),sim))     
        return v
        
    @staticmethod
    def _norm_mat(mat):
        '''normalizes each row in 'mat' by their l2 norm'''
        norm = (mat**2).sum(axis=1)**.5
        return mat / norm[...,None]