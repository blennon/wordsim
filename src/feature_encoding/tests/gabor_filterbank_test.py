'''
Created on Aug 2, 2012

@author: bill
'''
import unittest
from feature_encoding import *

class Test(unittest.TestCase):

    def setUp(self):
        self.n_ang, self.px_scales, self.px_width = 3, [1,2], 20
        self.fb = gabor_filterbank(self.n_ang,self.px_scales,self.px_width)
        
    def test_filterbank_shape(self):
        '''
        makes sure the filterbank has the right sized filters and the right
        number of them
        '''
        self.assertEqual(self.fb.shape,(self.px_width,self.px_width,
                                        2*self.n_ang*len(self.px_scales)))
        
    def test_filterbank_filterlocation(self):
        '''
        checks to make sure the gabor filter is placed in the right location in
        the array returned by the filter bank
        '''
        gb, _, _ = gabor(self.px_scales[1],self.px_width,0.0,0.0,lamda=3*np.pi/2,
                   gamma=(5./8.))

        self.assertEqual(np.linalg.norm(gb - self.fb[:,:,6]),0.0)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()