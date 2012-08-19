import numpy as np
import matplotlib.pyplot as plt
from gabor import *

def image_grid_space(im_size,filt_size,px_space):
    '''
    given image size 'im_size', return the coordinates of points of an evenly
    spaced grid with px_space between each point over the image with enough
    room left on edges for the filter
    
    returns a list of tuples of grid pts, i.e. [(i,j),...]
    '''
    a,b = np.ceil(filt_size[0]/2.), np.ceil(filt_size[1]/2.)
    m,n = im_size
    
    x = np.linspace(a,m-a,int((m-2*a)/px_space))
    y = np.linspace(b,n-b,int((n-2*b)/px_space))
    shape = (len(x),len(y))
    grid_pts = []
    for i in x:
        for j in y:
            grid_pts.append((int(i),int(j)))
    return grid_pts, shape

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
    a,b = np.floor(m/2.), np.floor(n/2.)
    if m % 2 != 0:
        a1,a2 = a, a+1
    else:
        a1,a2 = a, a
    if n % 2 != 0:
        b1,b2 = b, b+1
    else:
        b1,b2 = b, b
        
    i,j = grid_pt

    return (im[i-a1:i+a2,j-b1:j+b2,None]*fb).sum(axis=0).sum(axis=0)

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

def image2features_space(im,fb,feat_space):
    '''
    same as image2features but uses image_grid_space and feat_space to 
    generate the grid
    
    im: image (np array)
    fb: filter bank (np array)
    feat_space: number of pixels between each grid pt
    
    return feature vectors of an image at regularly spaced points on a
    grid over the image in the form of an ndarray
    '''

    filt_width,filt_height,n_filters = fb.shape
    pts, shape = image_grid_space(im.shape,(filt_width,filt_height),feat_space)
    feat_array = np.zeros((shape[0],shape[1],n_filters))
    i,j = 0,0
    for pt in pts:
        feat_array[i,j,:] = feature_vector(im,pt,fb)
        i += 1
        if i == shape[0]:
            i,j = 0, j+1
    return feat_array

    
if __name__ == "__main__":
    #grid,shape = image_grid_space((128,128),(32,32),8)
    #im = np.zeros((128,128))
    #for i,j in grid:
    #    im[i,j] = 1.0
    #plt.imshow(im)
    #plt.show()
    
    im = np.zeros((128,128))   
    fb = np.zeros((32,32,3))
    fs = image2features_space(im,fb,4)
    print fs.shape
