'''
This experiment will test the qualitative differences in
measures of word similarity (assessed by a human) made by
a system which creates word vectors from co-occurrences.

Fixed parameters across experiments:
- Lexicon: 10,000 most frequent words
- Corpus: American National Corpus
- Dim redux: SVD (200 singular values)
- Test set of words to gather similar words to

Variable parameters across experiments: distance co-occurrences
are made between words.
1.) bigrams (forward only), i.e. dist = 1
2.) bigrams (forward and backward), i.e. dist = -1,1
3.) trigrams (forward and back), i.e. dist = -2,-1,1,2

================================================================
RESULTS:

You seem to get a lot of mileage out of just the forward bigrams.
Adding backwards directions improved some and made others worse.

Adding co-occurrences farther away seems to yield more abstract
meaning and improves the bigram results slightly but noticeably.
================================================================
'''
from data_preprocess import *
from similarity import *


def write_query(q_list, out_f):
    '''print the query results nicely'''
    out_f.write('='*50)
    out_f.write('\n')
    out_f.write('Query results for: %s\n' % q_list[0][0])
    for q in q_list[1:]:
        out_f.write('%s, %s\n' % (q[0],q[1]))
    out_f.write('='*50)
    out_f.write('\n')
    
def exper(occurs_pickle,num_svs,test_words,out_f,forward_only):
    print 'loading data...'
    NO = pickle.load(open(occurs_pickle,'rb'))
    L = NO.lex
    #del sys.modules['lexicon']
    
    print 'transforming data...'
    if not forward_only:
        occurs = NO.get_occurs(concat=True)
    else:
        occurs = NO.get_occurs(concat=False)
        for i in range(len(occurs)/2):
            del occurs[-i-1]
        occurs = NgramOccurs.concat_occurs(occurs)      
    S = SVDSim(occurs,L,d=num_svs,norm_ss=True)
    
    print 'Querying...'
    f = open(out_f,'w')
    for w in test_words:
        results = S.query(w,6,'dot')
        if results is not None:
            write_query(results,f)
    
    print 'Finished experiment.'
    
if __name__ == '__main__':
    test_words = ['week','january','blue','monday','pakistan','mexican',
                  'robert','paper','train','fast','huge','feel','could',
                  'dog','is','loves','attacked','urged','defeated','however',
                  'extremely','stupid']
    data = ['/var/wordsim/10000_bigrams/ngram_occurs.p',
            '/var/wordsim/10000_trigrams/ngram_occurs.p']
    
    exper('/var/wordsim/10000_bigrams/ngram_occurs.p',200,test_words,
          '/var/wordsim/10000_bigrams/results/forward_only.txt',True)
    exper('/var/wordsim/10000_bigrams/ngram_occurs.p',200,test_words,
          '/var/wordsim/10000_bigrams/results/both.txt',False)
    exper('/var/wordsim/10000_trigrams/ngram_occurs.p',200,test_words,
          '/var/wordsim/10000_trigrams/results/forward_only.txt',True)
    exper('/var/wordsim/10000_trigrams/ngram_occurs.p',200,test_words,
          '/var/wordsim/10000_trigrams/results/both.txt',False)