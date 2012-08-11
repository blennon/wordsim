'''
This is a more general class than lexicon (specific for words) but accomplishes
similar things.
'''
from pylab import *

class Tokens(object):
    '''Tokens are unique identifiers for things (e.g. words, user names, user IDs, etc)'''
    
    def tokenize_flat_file(self, flat_file, token_column, delim='\t', header=True,
                           token_as_int = True):
        '''
        Creates dictionaries mapping from tokens to IDs and vice versa.  IDs are formatted
        to be used as vector indices

        This assumes the flat file has a unique list (i.e. the token never appears twice)
        '''
        f = open(flat_file)
        if header: 
            f.readline()
        self.tokens2ids = {}
        self.ids2tokens = {}
        i = 0
        for l in f:
            l = l.strip().split(delim)
            token = l[token_column]
            if token_as_int:
                token = int(token)
            self.tokens2ids[token] = i
            self.ids2tokens[i] = token
            i += 1
    
    def token2id(self, token):
        return self.tokens2ids[token]
    
    def id2token(self, id):
        return self.ids2tokens[id]
    
    def save(self, outfile, delim='\t'):
        f = open(outfile,'w')
        for token,id in self.tokens2ids.iteritems():
            f.write('%s%s%s\n' % (token,delim,id))
        
    def token_count(self):
        return len(self.tokens2ids)