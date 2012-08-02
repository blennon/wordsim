'''
Created on Aug 2, 2012

@author: bill
'''
import unittest
import numpy as np
from feature_encoding import *

class Test(unittest.TestCase):


    def setUp(self):
        self.fb = np.ones((3,3,2))
        self.fb[:,:,0] *= 1
        self.fb[:,:,1] *= 2
        self.im = np.zeros((5,5))
        self.im[1:4,1:4] = .1
        self.im[2,2] = .33
    
    def test_feature_vector(self):
        '''make sure the feature vector has the appropriate values'''
        
        # tests for odd length filters
        fv = feature_vector(self.im,(2,2),self.fb)
        self.assertEquals(fv[0],self.im[1:4,1:4].sum())
        self.assertEquals(fv[1],2*self.im[1:4,1:4].sum())
        
        # tests for even length filters
        fv = feature_vector(self.im,(2,2),self.fb[0:2,0:2,:])
        self.assertEquals(fv[0],self.im[1:3,1:3].sum())
        self.assertEquals(fv[1],2*self.im[1:3,1:3].sum())
        
    def test_image2features_shape(self):
        im = np.zeros((127,127))   
        fb = np.zeros((33,32,3))
        fs = image2features(im,fb,4)
        self.assertEquals((2,2,3), fs.shape)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()