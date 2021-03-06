import sys
sys.path.append('../')
from similarity import *
from data_preprocess import *

def print_query(query, q_list):
    '''print the query results nicely'''
    print '='*50
    print 'Query results for: %s\n' % query
    for q in q_list:
        print q[0], q[1]
    print '='*50
    print ''

if __name__ == '__main__':

    if len(sys.argv) < 2:
        raise Exception('Two arguments needed: location of pickled data and dimension')
        
    print 'testing with data from %s using %s dimensions' % (sys.argv[1],sys.argv[2])
    print 'loading data...'
    NO = pickle.load(open(sys.argv[1],'rb'))
    L = NO.lex

    print 'transforming data...'
    S = SVDSim(NO.get_occurs(concat=True),L,d=int(sys.argv[2]),norm_ss=True)

    print 'Ready for queries.'
    while True:
        q = raw_input('enter word to query for: ')
        results = S.phrase_query(q,6,'dot')
        if results is not None:
            print_query(q,results)