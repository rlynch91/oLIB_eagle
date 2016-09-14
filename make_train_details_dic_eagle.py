import sys
sys.path.insert(1,'/home/ryan.lynch/numpy/numpy-1.8.2-INSTALL/lib64/python2.7/site-packages')
import numpy as np
import pickle
import os

###
dictionary = {}

###
dictionary['calc info'] = {}
dictionary['calc info']['interp method'] = 'Grid Linear'
dictionary['calc info']['extrap method'] = 'Grid Nearest'

###
dictionary['param info'] = {}
dictionary['param info']['low_f'] = {}
dictionary['param info']['low_f']['logBSN_and_BCI'] = {}
dictionary['param info']['low_f']['logBSN_and_BCI']['dimension'] = 2
dictionary['param info']['low_f']['logBSN_and_BCI']['param names'] = ['logBSN','BCI']
dictionary['param info']['low_f']['logBSN_and_BCI']['interp range'] = np.array([[0., 6.],[0., 30.]])

###
dictionary['optimize signal training'] = {}
dictionary['optimize signal training']['low_f'] = {}
dictionary['optimize signal training']['low_f']['logBSN_and_BCI'] = {}
dictionary['optimize signal training']['low_f']['logBSN_and_BCI']['optimization method'] = 'BFGS'
dictionary['optimize signal training']['low_f']['logBSN_and_BCI']['optimization initial coords'] = np.array([np.nan,np.nan])

###
dictionary['optimize noise training'] = {}
dictionary['optimize noise training']['low_f'] = {}
dictionary['optimize noise training']['low_f']['logBSN_and_BCI'] = {}
dictionary['optimize noise training']['low_f']['logBSN_and_BCI']['optimization method'] = 'BFGS'
dictionary['optimize noise training']['low_f']['logBSN_and_BCI']['optimization initial coords'] = np.array([np.nan,np.nan])

###
dictionary['train signal data'] = {}
dictionary['train signal data']['low_f'] = {}
dictionary['train signal data']['low_f']['logBSN'] = {}
dictionary['train signal data']['low_f']['logBSN']['data'] = np.transpose(np.array([np.nan]))
dictionary['train signal data']['low_f']['logBSN']['KDE ranges'] = np.array([[0., 6.]])
dictionary['train signal data']['low_f']['logBSN']['KDE bandwidths'] = np.array([np.nan])
dictionary['train signal data']['low_f']['logBSN']['KDE points'] = np.array([100])
dictionary['train signal data']['low_f']['BCI'] = {}
dictionary['train signal data']['low_f']['BCI']['data'] = np.transpose(np.array([np.nan]))
dictionary['train signal data']['low_f']['BCI']['KDE ranges'] = np.array([[0., 30.]])
dictionary['train signal data']['low_f']['BCI']['KDE bandwidths'] = np.array([np.nan])
dictionary['train signal data']['low_f']['BCI']['KDE points'] = np.array([100])

###
dictionary['train noise data'] = {}
dictionary['train noise data']['low_f'] = {}
dictionary['train noise data']['low_f']['logBSN'] = {}
dictionary['train noise data']['low_f']['logBSN']['data'] = np.transpose(np.array([np.nan]))
dictionary['train noise data']['low_f']['logBSN']['KDE ranges'] = np.array([[0., 6.]])
dictionary['train noise data']['low_f']['logBSN']['KDE bandwidths'] = np.array([np.nan])
dictionary['train noise data']['low_f']['logBSN']['KDE points'] = np.array([100])
dictionary['train noise data']['low_f']['BCI'] = {}
dictionary['train noise data']['low_f']['BCI']['data'] = np.transpose(np.array([np.nan]))
dictionary['train noise data']['low_f']['BCI']['KDE ranges'] = np.array([[0., 30.]])
dictionary['train noise data']['low_f']['BCI']['KDE bandwidths'] = np.array([np.nan])
dictionary['train noise data']['low_f']['BCI']['KDE points'] = np.array([100])

###
dictionary['search bins'] = {}
dictionary['search bins']['bin names'] = ['low_f']
dictionary['search bins']['low_f'] = {}
dictionary['search bins']['low_f']['low logBSN cut'] = 0
dictionary['search bins']['low_f']['high logBSN cut'] = 6
dictionary['search bins']['low_f']['low BCI cut'] = 1
dictionary['search bins']['low_f']['high BCI cut'] = np.inf
dictionary['search bins']['low_f']['low freq cut'] = 48
dictionary['search bins']['low_f']['high freq cut'] = 1024
dictionary['search bins']['low_f']['low quality cut'] = 2
dictionary['search bins']['low_f']['high quality cut'] = 108

###
if not os.path.exists('/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/'):
	os.makedirs('/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/')
pickle.dump(dictionary, open('/home/ryan.lynch/2nd_pipeline/pipeline_eagle/test_LLRT_info/training_details_dictionary.pkl','wt'))
