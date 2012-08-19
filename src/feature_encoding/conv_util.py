'''
Created on Aug 2, 2012

@author: bill
'''
import numpy as np
from scipy.sparse import coo_matrix, vstack

def conv_as_mat(filt,im_size):
    '''
    returns a sparse matrix representing a full convolution transform, i.e when the
    image is flattened to a vector and left multiplied by the matrix, the
    result will be a vector representation of the convolved image by the
    filter
    '''
    m,n = filt.shape
    if m > im_size[0] or n > im_size[1]:
        raise Exception('Filter is larger than image')
    
    filt_mat = []
    for i in range(im_size[0]+int(np.ceil(m/2.))):
        for j in range(im_size[1]+int(np.ceil(n/2.))):
            # i,j represents the lower right corner of filter placement
            a,b = max(0,i-m+1), max(0,j-n+1)
            c,d = min(im_size[0]+1,i+1), min(im_size[1]+1,j+1)
            imfilt = np.zeros(im_size)
            if i < im_size[0]:
                e = m-(c-a)
                g = m+1
            else:
                e = 0
                g = im_size[0] - a
            if j < im_size[1]:
                f = n-(d-b)
                h = n+1
            else:
                f = 0
                h = im_size[1] - b
            imfilt[a:c,b:d] = filt[e:g,f:h]
            filt_mat.append(coo_matrix(imfilt.flatten()))            
    return vstack(filt_mat)
        
if __name__ == '__main__':
    filt = np.asarray([[1,2],[4,5]])
    M = conv_as_mat(filt,(4,4))
    print M.shape