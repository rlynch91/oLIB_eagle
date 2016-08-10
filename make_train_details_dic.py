import sys
sys.path.insert(1,'/home/ryan.lynch/numpy/numpy-1.8.2-INSTALL/lib64/python2.7/site-packages')
import numpy as np
import pickle

###
dictionary = {}

###
dictionary['calc info'] = {}
dictionary['calc_info']['interp method'] = 'Grid Linear'
dictionary['calc_info']['extrap method'] = 'Grid Nearest'

###
dictionary['param info'] = {}
dictionary['param info']['low f'] = {}
dictionary['param info']['low f']['logBSN_and_BCI'] = {}
dictionary['param info']['low f']['logBSN_and_BCI']['dimension'] = 2
dictionary['param info']['low f']['logBSN_and_BCI']['param names'] = ['logBSN','BCI']
dictionary['param info']['low f']['logBSN_and_BCI']['interp range'] = np.array([[0., 6.],[0., 30.]])

###
dictionary['optimize signal training'] = {}
dictionary['optimize signal training']['low f'] = {}
dictionary['optimize signal training']['low f']['logBSN_and_BCI'] = {}
dictionary['optimize signal training']['low f']['logBSN_and_BCI']['optimization method'] = 'BFGS'
dictionary['optimize signal training']['low f']['logBSN_and_BCI']['optimization initial coords'] = np.array([np.nan,np.nan])

###
dictionary['optimize noise training'] = {}
dictionary['optimize noise training']['low f'] = {}
dictionary['optimize noise training']['low f']['logBSN_and_BCI'] = {}
dictionary['optimize noise training']['low f']['logBSN_and_BCI']['optimization method'] = 'BFGS'
dictionary['optimize noise training']['low f']['logBSN_and_BCI']['optimization initial coords'] = np.array([np.nan,np.nan])

###
dictionary['train signal data'] = {}
dictionary['train signal data']['low f'] = {}
dictionary['train signal data']['low f']['logBSN'] = {}
dictionary['train signal data']['low f']['logBSN']['data'] = np.transpose(np.array([np.nan]))
dictionary['train signal data']['low f']['logBSN']['KDE ranges'] = np.array([[0., 6.]])
dictionary['train signal data']['low f']['logBSN']['KDE bandwidths'] = np.array([np.nan])
dictionary['train signal data']['low f']['logBSN']['KDE points'] = np.array([100])
dictionary['train signal data']['low f']['BCI'] = {}
dictionary['train signal data']['low f']['BCI']['data'] = np.transpose(np.array([np.nan]))
dictionary['train signal data']['low f']['BCI']['KDE ranges'] = np.array([[0., 30.]])
dictionary['train signal data']['low f']['BCI']['KDE bandwidths'] = np.array([np.nan])
dictionary['train signal data']['low f']['BCI']['KDE points'] = np.array([100])

###
dictionary['train noise data'] = {}
dictionary['train noise data']['low f'] = {}
dictionary['train noise data']['low f']['logBSN'] = {}
dictionary['train noise data']['low f']['logBSN']['data'] = np.transpose(np.array([np.nan]))
dictionary['train noise data']['low f']['logBSN']['KDE ranges'] = np.array([[0., 6.]])
dictionary['train noise data']['low f']['logBSN']['KDE bandwidths'] = np.array([np.nan])
dictionary['train noise data']['low f']['logBSN']['KDE points'] = np.array([100])
dictionary['train noise data']['low f']['BCI'] = {}
dictionary['train noise data']['low f']['BCI']['data'] = np.transpose(np.array([np.nan]))
dictionary['train noise data']['low f']['BCI']['KDE ranges'] = np.array([[0., 30.]])
dictionary['train noise data']['low f']['BCI']['KDE bandwidths'] = np.array([np.nan])
dictionary['train noise data']['low f']['BCI']['KDE points'] = np.array([100])

###
pickle.dump(dictionary, open('???.pkl','wt'))
