import logging
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
import pdb
import time
import sys
import scipy.linalg as lng
#import scipy.sparse as sp

sys.path.append('../..')

from pyMRA.MRATree import MRATree
import pyMRA.MRATools as mt
#import models.diffusion


"""
This script is used to make predictions on a data set supplied in a csv
file with each row corresponding to one observation. The first two columns
represent the x and y coordinate, the third is the measurement and the
fourth is the truth - if available
"""



if __name__=='__main__':

    np.random.seed(11)

    #filename = '/home/marcin/MRF/data/Exp_Theta0.1_X100_Y100.csv'
    #filename = '/home/marcin/MRF/data/Exp_Theta0.1_X100_Y100_missing_all.csv'
    #filename = '/home/marcin/MRF/data/sat_temps.csv'
    filename = '/home/marcin/temp/test'
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%H:%M:%S',level=logging.INFO)
    
    M=2; J=4; r0=2
    me_scale=1e-4
    critDepth = M+1

    
    with open(filename, 'r') as ipFile:
        csv = [line.strip().split(',') for line in ipFile.readlines()][1:]

    N = len(csv)

    locs=np.zeros((N, 2))
    y_obs = np.zeros((N, 1))
    y = np.zeros((N, 1))

    
    for idx, line in enumerate(csv):

        locs[idx, 1] = float(line[0])
        locs[idx, 0] = float(line[1])
        y_obs[idx, 0] = float(line[2]) if line[2]!='NA' else np.NAN
        if len(line)>3:
            y[idx, 0] = float(line[3])

    locs[:,0] = locs[:,0] - np.min(locs[:,0])
    locs[:,1] = locs[:,1] - np.min(locs[:,1])

    locs[:,0] = locs[:,0]/np.max(locs[:,0])
    locs[:,1] = locs[:,1]/np.max(locs[:,1])

    Nx = len(np.unique(locs[:,0])); Ny = len(np.unique(locs[:,1]))
    
    obs_mean = np.nanmean(y_obs)
    y_obs = y_obs - obs_mean
    y = y - obs_mean
    
    obs_inds = np.isfinite(y_obs).flatten()
    R = me_scale

    y_disp = y_obs.reshape((Nx, Ny))
    mt.dispMat(y_disp, cmap="Spectral", title="observations")

    sys.exit()


    
    logging.info("MRA started")
    start = time.time()
    cov = lambda _locs1, _locs2: mt.ExpCovFun(_locs1, _locs2, l=0.3)


    start = time.time()
    mraTree = MRATree(locs, M, J, r0, critDepth, cov, y_obs, R)
       
    yP, sdP = mraTree.predict()
    sdP = sdP.reshape((Nx, Ny))
    #sdP = np.flipud(sdP.reshape((Nx, Ny)))
    yP = yP.reshape((Nx, Ny))

    mraTime = time.time()-start
    logging.info( "MRA finished in {:.2}s".format(mraTime) )
    
    np.save("y-pred.npy", yP)


   
    
    ### compare results


    mt.dispMat(yP, cmap="Spectral", title="prediction")
    mt.dispMat(sdP, cmap="coolwarm", title="standard deviation", vmin=0.05, vmax=0.36)
    if np.any(y):
        y = y.reshape((Nx, Ny), order='A')
        mt.dispMat(y, cmap="Spectral", title="truth")
        mt.dispMat(yP - y, cmap="coolwarm", title="difference")

        


