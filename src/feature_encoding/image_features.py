import numpy as np
import matplotlib.pyplot as plt
from gabor import *

def image_grid(im_size,filt_size,n_pts):
    '''
    given image size 'im_size', return the coordinates of
    n_pts (must be a square number) evenly spaced across the image with enough
    room left on edges for the filter
    
    returns a list of tuples of grid pts, i.e. [(i,j),...]
    '''
    a,b = np.ceil(filt_size[0]/2.), np.ceil(filt_size[1]/2.)
    m,n = im_size
    
    i = int(n_pts ** .5)
    if i**2 != n_pts:
        raise Exception('n_pts must be a square number')
    
    x = np.linspace(a,m-a,i)
    y = np.linspace(b,n-b,i)
    grid_pts = []
    for i in x:
        for j in y:
            grid_pts.append((int(i),int(j)))
    return grid_pts

def feature_vector(im,grid_pt,fb):
    '''
    generate a feature vector (aka "jet") at pt 'grid_pt' (a tuple) by
    taking the dot product of the image surrounding that point with each filter
    in the filter bank 'fb'.  the filters are along the third axis
    '''
    m,n,p = fb.shape
    a,b = np.ceil(m/2.), np.ceil(n/2.)
    i,j = grid_pt

    return (im[i-a:i+a,j-b:j+b,None]*fb).sum(axis=0).sum(axis=0)

def image2features(im,fb,n_features):
    '''
    im: image (np array)
    fb: filter bank (np array)
    n_features: number of feature vectors to extract (must be a square number)
    
    return feature vectors of an image at regularly spaced points on a
    grid over the image in the form of an ndarray
    '''
    k = n_features ** .5
    if int(k)**2 != n_features:
        raise Exception('n_features must be a square number')
    filt_width,filt_height,n_filters = fb.shape
    feat_array = np.zeros((k,k,n_filters))
    i,j = 0,0
    for pt in image_grid(im.shape,(filt_width,filt_height),n_features):
        feat_array[i,j,:] = feature_vector(im,pt,fb)
        i += 1
        if i == k:
            i,j = 0, j+1
    return feat_array
    
    
if __name__ == "__main__":
    im = np.zeros((128,128))   
    fb = np.zeros((32,32,3))
    fs = image2features(im,fb,4)
    print fs