import sys
sys.path.append('../')
from data_preprocess import *
from similarity import *

class CVSim(Similarity):

    def __init__(self, CV, lexicon):
        self.lex = lexicon
        self.SS = CV
