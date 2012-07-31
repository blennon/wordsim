'''
Created on Jul 1, 2012

@author: bill
'''
import operator


class Lexicon(object):
    '''
    build or load lexicon from file
    '''
       
    def load_lex(self, lex_file, max_words=None, delim=None):
        '''
        load lexicon from disk.  formatted text files as 'index\tcount'
        '''
        w2i, i2w = {}, {}
        for l in open(lex_file):
            i, w = l.strip().split(delim)
            i = int(i)
            if max_words is not None:
                if i >= max_words:
                    break
            w2i[w] = i
            i2w[i] = w
        self.w2i, self.i2w =  w2i, i2w
    
    def build_lex(self, lex_file, max_words, min_count):
        '''
        builds the lexicon of the top max_words about min_count threshold.

        lex_file: location of text file on disk with lexicon
        min_count: minimum number of times the words must have
                   appeared in the lexicon
        '''
        f = open(lex_file,'r')
        f.readline()
        d = {}
        for l in f:
            word,count = l.strip().split(' ')
            count = int(count)
            if count < min_count: 
                continue
            d[word] = count
        sorted_d = sorted(d.iteritems(), key=operator.itemgetter(1))
        sorted_d.reverse()

        if len(d) < max_words:
            n = len(d)
        else:
            n = max_words

        self.lex = [sorted_d[i][0] for i in xrange(n)]
        self.build_index()
    
    def build_index(self):
        '''build word-to-int and int-to-word dicts'''
        w2i, i2w = {}, {}
        i = 0
        for w in self.lex:
            w2i[w] = i
            i2w[i] = w
            i += 1
        self.w2i, self.i2w =  w2i, i2w
        
    def get_vocab(self):
        '''return a list of the words in the lexicon'''
        return [self.i2w[i] for i in self.i2w.iterkeys()]
    
    def __len__(self):
        return self.max_words
    
    def __getitem__(self, item):
        '''
        returns the index (row/col) if given a word string,
        words the word if given an int (row/col index)
        '''
        if isinstance(item, str):
            return self.w2i[item]
        elif isinstance(item, int):
            return self.i2w[item]
        else:
            raise Exception('item should be an int or string')
        

if __name__ == '__main__':
    L = Lexicon()
    #L.build_lex('/var/wordsim/written-lexicon.txt',10,5)
    L.load_lex('/var/wordsim/confab_occurs/wordlist10k75M.txt',5)
    print L[3]
