'''
Created on Jul 1, 2012

@author: bill
'''
import operator


class Lexicon(object):
    '''
    builds the lexicon from text file on disk
    '''

    def __init__(self, lex_file, max_words, min_count):
        '''
        lex_file: location of text file on disk with lexicon
        max_words: maximum number of words in lexicon
        min_count: minimum number of times the words must have
                   appeared in the lexicon
        '''
        self.lex_file = lex_file
        self.max_words = max_words
        self.min_count = min_count
        self.lex = self.build_lex()
        self.w2i, self.i2w = self.build_index()
    
    def build_lex(self):
        '''returns a list of the top N most frequent words'''
        f = open(self.lex_file,'r')
        f.readline()
        d = {}
        for l in f:
            word,count = l.strip().split(' ')
            count = int(count)
            if count < self.min_count: 
                continue
            d[word] = count
        sorted_d = sorted(d.iteritems(), key=operator.itemgetter(1))
        sorted_d.reverse()

        if len(d) < self.max_words:
            n = len(d)
        else:
            n = self.max_words

        return [sorted_d[i][0] for i in xrange(n)]
    
    def build_index(self):
        '''build word-to-int and int-to-word dicts'''
        w2i, i2w = {}, {}
        i = 0
        for w in self.lex:
            w2i[w] = i
            i2w[i] = w
            i += 1
        return w2i, i2w
    
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
    L = Lexicon('/var/wordsim/written-lexicon.txt',10,5)
