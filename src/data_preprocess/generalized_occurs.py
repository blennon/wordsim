'''
This is a general occurrence class where each dimension of the co-occurrence
matrix can have a different set of tokens (mapped to their unique row/col number)

It currently supports making co-occurrences from a flat file
'''
from pylab import *
from scipy.sparse import dok_matrix
from scipy.io import mmwrite

class Occurs(object):
    '''An object for storing and counting co-occurrence between tokens'''
    
    def __init__(self,tokens1,tokens2):
        '''tokens are instances of Tokens class'''
        self.tokens1 = tokens1
        self.tokens2 = tokens2
        self.occurs = dok_matrix((tokens1.token_count(),tokens2.token_count()))
    
    def co_occur_flat_file(self, flat_file, token1_column, token2_column, delim='\t',
                           header=True, token_as_int = True):
        '''Iterates through a flat file and co-occurs the tokens in their respective columns'''
        f = open(flat_file)
        if header: 
            f.readline()
        for l in f:
            l = l.strip().split(delim)
            token1, token2 = l[token1_column], l[token2_column]
            if token_as_int:
                token1, token2 = int(token1), int(token2)
            id1, id2 = self.tokens1.token2id(token1), self.tokens2.token2id(token2)
            self.occurs[id1,id2] += 1
            
    def get_occurs(self):
        return self.occurs
        
    def save_occurs(self,outfile,format='mm'):
        '''save the occurs to disk'''
        if format == 'mm':
            mmwrite(outfile,self.occurs)
        elif format == 'graphlab':
            f = open(outfile,'w')
            occurs = self.occurs.tocoo()
            for i in range(occurs.row.shape[0]):
                # GL likes 1-indexing
                f.write('%s %s  %s\n' % (occurs.row[i]+1,occurs.col[i]+1,occurs.data[i]))
            f.close()
        else:
            raise Exception('format must be mm or graphlab')