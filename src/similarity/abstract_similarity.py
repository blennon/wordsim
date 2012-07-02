class Similarity(object):
    '''
    an interface class
    
    performs some transformation on the co-occurrence data
    and allows for similarity measures
    '''
    
    def __init__(self, occurs, lexicon):
        '''init the similarity space'''
        pass
    
    def transform_data(self):
        '''transform the data into a useful similarity space'''
        raise Exception("Not implemented")
    
    def query(self, item, N):
        '''
        query the similarity space for the 'N' nearest things
        to 'item'
        
        item can be a row/col index (int) or a word (str)
        '''
        raise Exception("Not implemented")