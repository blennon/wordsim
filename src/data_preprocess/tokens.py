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
            try:
                self.tokens2ids[token]
            except KeyError:
                self.tokens2ids[token] = i
                self.ids2tokens[i] = token
                i += 1
    
    def token2id(self, token):
        return self.tokens2ids[token]
    
    def id2token(self, id):
        return self.ids2tokens[id]
    
    def save(self, outfile, delim='\t'):
        f = open(outfile,'w')
        for id,token in self.ids2tokens.iteritems():
            f.write('%s%s%s\n' % (token,delim,id))
    
    def load_tokens_flat(self, token_f, delim='\t', token_int=True):
        self.tokens2ids = {}
        self.ids2tokens = {}
        for l in open(token_f):
            token,id = l.strip().split(delim)
            if token_int:
                token = int(token)
            id = int(id)
            self.tokens2ids[token] = id
            self.ids2tokens[id] = token
        
    def token_count(self):
        return len(self.tokens2ids)
    
    def get_token_list(self):
        return self.tokens2ids.keys()
    
    
class ZipsTokens(Tokens):
    
    def __init__(self):
        Z = Zips()
        self.tokenize_zips(Z)
        del Z
        
    def tokenize_zips(self,Zips):
        self.tokens2ids = {}
        self.ids2tokens = {}
        i=0
        for z in Zips.zips.iterkeys():
            self.tokens2ids[z] = i
            self.ids2tokens[i] = z
            i += 1   