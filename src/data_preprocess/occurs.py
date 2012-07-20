'''
Created on Jul 1, 2012

@author: bill
'''
import numpy as np
from scipy.sparse import *
from scipy.io import mmwrite, mmread
from lexicon import *
import time
import cPickle as pickle
import os

class NgramOccurs(object):
    '''
    build co-occurrence matrices from ngram files
    '''

    def __init__(self, ngram_file, max_dist, lexicon, delim=' '):
        '''
        read a text file with ngrams and counts delimited by
        'delim' and count co-occurs up to distance 'max dist'
        
        only words in lexicon (class) are permitted
        
        stored as scipy sparse matrices
        '''
        self.lex = lexicon
        self.ngram_file = ngram_file
        self.max_dist = max_dist
        self.delim = delim
        
        self.occurs = self.setup_occur_mats()
        
    def occur(self):
        '''count co-occurs'''
        for l in open(self.ngram_file):
            l = l.strip().split(self.delim)
            ngram,count = l[:-1], l[-1]
            n_ind = self._wordlist_to_indices(ngram)
            for i in range(len(n_ind)):
                for j in range(len(n_ind)):
                    if n_ind[i] is None or n_ind[j] is None or i==j:
                        continue
                    dist = j-i
                    # don't count out of range
                    # dist < 0 is just the transpose of dist > 0
                    if abs(dist) > self.max_dist or dist < 0:
                        continue
                    self.occurs[dist][n_ind[i],n_ind[j]] += float(count)
        
        # dist < 0 is just the transpose of dist > 0
        for i in range(self.max_dist):
            d = i + 1
            self.occurs[-d] = self.occurs[d].T.copy()
            
    def setup_occur_mats(self):
        '''create a dictionary of sparse co-occur matrices'''
        N = len(self.lex)
        occurs = {}
        for i in range(self.max_dist):
            occurs[i+1] = dok_matrix((N,N))
            occurs[-i-1] = dok_matrix((N,N))
        return occurs
    
    def _wordlist_to_indices(self, word_list):
        '''convert a list of words to lexicon indices'''
        inds = []
        for w in word_list:
            try:
                inds.append(self.lex[w])
            except KeyError:
                inds.append(None)
        return inds
    
    def get_occurs(self, concat=False):
        '''
        returns the occurs either as a concatentated single matrix
        or as a dictionary of matrices
        '''
        if concat:
            return NgramOccurs.concat_occurs(self.occurs)
        else:
            return self.occurs

    def save_occurs(self, out_dir):
        '''save the occurs to directory as individual files'''
        for d,m in self.occurs.iteritems():
            try:
                mmwrite(out_dir+'/d'+str(d),m)
            except IOError:
                os.makedirs(out_dir)
                mmwrite(out_dir+'/d'+str(d),m)

    @staticmethod
    def concat_occurs(occurs):
        '''
        return a single sparse matrix with all of the sparse
        co-occur matrices concatenated horizonally
        '''
        inds = sorted([i for i in occurs.iterkeys()])
        mats = [occurs[i].tocoo() for i in inds]
        return hstack(mats)


if __name__ == '__main__':
    in_dir = '/var/wordsim/'
    out_dir = in_dir + '10000_bigrams/'
    try:
        os.makedirs(out_dir)
    except:
        pass

    print 'building lexicon...'
    L = Lexicon()
    L.build_lex(in_dir+'written-lexicon.txt',10000,5)
    O = NgramOccurs(in_dir+'written-trigrams-freq.txt',1,L)
    
    print 'counting co-occurrences...'
    O.occur()
    print O.occurs

    print 'pickling data...'
    pickle.dump(O,open(out_dir+'ngram_occurs.p','wb'))
    pickle.dump(L,open(out_dir+'lex.p','wb'))

    print 'done.'

    
