'''
Created on Aug 2, 2012

@author: bill

WARNING: This takes about 20 minutes
'''
import pylab as pl
from matplotlib import cm
from feature_encoding import *
import scipy as sp


if __name__ == '__main__':
    # create filterbank
    GJ = GaborJets(px_scales=[10],px_width=20)
    fb = GJ.fb
    
    # load image
    I = np.asarray(Image.open('/home/bill/python_packages/PIL/Images/lena.ppm'))
    I = np.mean(I,axis=2) # gray scale
    I_ = I[32:96,32:96]
    #pl.imshow(I_,cmap=cm.gray)
    #pl.show()
    
    # convert fb into linear transformation
    mats = []
    for i in range(fb.shape[2]):
        mats.append(conv_as_mat(fb[:,:,i], I_.shape))
    M = sp.sparse.vstack(mats)
    print M.shape
    M = M.tocsr()
    x_range = np.arange(0,M.shape[0],8)
    M_ = M[x_range,:]
    del M      
    M = M_.todense()
    del M_
    
    
    # transform image
    print M.shape, I_.flatten().shape
    I_star = np.dot(M,I_.flatten())
    print I_star.shape
    
    # inverse transform image by least squares on fb linear transform matrix
    #P,D,Qt = sp.sparse.linalg.svds(M_,200)    
    I__ = np.dot(np.linalg.pinv(M), I_star.T)
    
    # display original and reconstructed images -- should be similar
    I__ = I__.reshape(I_.shape)
    pl.imshow(I__,cmap=cm.gray)
    pl.show()
