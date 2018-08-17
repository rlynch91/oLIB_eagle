#!/usr/bin/python

import sys
sys.path.insert(1,'/home/ryan.lynch/numpy/numpy-1.8.2-INSTALL/lib64/python2.7/site-packages')
import numpy as np
import os
import pickle

#=======================================================================

#Config file for launching the oLIB pipeline

#Initialize the run dictionary that will hold all info about run
run_dic = {}

#=======================================================================

###
run_dic['version'] = {}
run_dic['version']['oLIB'] = 'ER10_code_freeze'
run_dic['version']['omicron'] ='v2r1'
run_dic['version']['LIB'] = '80a31deb98600444739e22f7b232ca5c9fe94603'
run_dic['version']['calibration'] = 'C00'

###
run_dic['config'] = {}
run_dic['config']['wait'] = 5
run_dic['config']['max wait'] = 2000
run_dic['config']['run dir'] = '/home/ryan.lynch/public_html/ER10_back_train/'
run_dic['config']['info dir'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/'
run_dic['config']['LIB bin dir'] = '/home/salvatore.vitale/lalsuites/burst_dev/o2_lib_20160720/bin/'
run_dic['config']['stride'] = 1002
run_dic['config']['overlap'] = 2
run_dic['config']['sample freq'] = 2048
run_dic['config']['oSNR thresh'] = 5.0
run_dic['config']['dt clust'] = 0.1
run_dic['config']['initial start'] = None
run_dic['config']['run label'] = 'ER10_back_train'
run_dic['config']['username'] = 'ryan.lynch'

###
run_dic['run mode'] = {}
run_dic['run mode']['line'] = 'Online'
run_dic['run mode']['inj runmode'] = 'NonInj'
run_dic['run mode']['DQ runmode'] = 'NonDQV'
run_dic['run mode']['train runmode'] = "Train"
run_dic['run mode']['gdb flag'] = True
run_dic['run mode']['gdb server'] = 'Production'
run_dic['run mode']['email flag'] = True
run_dic['run mode']['email addresses'] = ['rlynch@mit.edu','8476930667@vtext.com']
run_dic['run mode']['email throttle'] = 3600.
run_dic['run mode']['LIB flag'] = True
run_dic['run mode']['tar results'] = True

###
run_dic['ifos'] = {}
run_dic['ifos']['names'] = ['H1','L1']
run_dic['ifos']['H1'] = {}
run_dic['ifos']['H1']['channel type'] = 'H1_llhoft'
run_dic['ifos']['H1']['channel name'] = 'GDS-CALIB_STRAIN'
run_dic['ifos']['H1']['state channel name'] = 'GDS-CALIB_STATE_VECTOR'
run_dic['ifos']['H1']['run bitmask'] = 3
run_dic['ifos']['H1']['inj bitmask'] = 480
run_dic['ifos']['H1']['DQ'] = {}
run_dic['ifos']['H1']['DQ']['DQ channel names'] = [] #['DMT-DQ_VECTOR']
run_dic['ifos']['H1']['DQ']['DQ bitmasks'] = []  #[???]
run_dic['ifos']['L1'] = {}
run_dic['ifos']['L1']['channel type'] = 'L1_llhoft'
run_dic['ifos']['L1']['channel name'] = 'GDS-CALIB_STRAIN'
run_dic['ifos']['L1']['state channel name'] = 'GDS-CALIB_STATE_VECTOR'
run_dic['ifos']['L1']['run bitmask'] = 3
run_dic['ifos']['L1']['inj bitmask'] = 480
run_dic['ifos']['L1']['DQ'] = {}
run_dic['ifos']['L1']['DQ']['DQ channel names'] = [] #['DMT-DQ_VECTOR']
run_dic['ifos']['L1']['DQ']['DQ bitmasks'] = []  #[???]
#run_dic['ifos']['V1'] = {}
#run_dic['ifos']['V1']['channel type'] = 'V1_S6_llhoft'
#run_dic['ifos']['V1']['channel name'] = 'h_16384Hz'
#run_dic['ifos']['V1']['state channel name'] = 'Hrec_Flag_Quality'
#run_dic['ifos']['V1']['run bitmask'] = 1
#run_dic['ifos']['V1']['inj bitmask'] = 1  #448  #480
#run_dic['ifos']['V1']['DQ'] = {}
#run_dic['ifos']['V1']['DQ']['DQ channel names'] = ['Hrec_Flag_Quality']  #[???]
#run_dic['ifos']['V1']['DQ']['DQ bitmasks'] = [1]  #[???]

###
run_dic['coincidence'] = {}

run_dic['coincidence']['H1L1'] = {}
run_dic['coincidence']['H1L1']['ifos'] = ['H1','L1']
run_dic['coincidence']['H1L1']['coincidence window'] = 0.015
run_dic['coincidence']['H1L1']['coincidence snr thresh'] = 5.0
run_dic['coincidence']['H1L1']['analyze 0lag'] = True
run_dic['coincidence']['H1L1']['analyze back'] = True
run_dic['coincidence']['H1L1']['analyze noise training'] = True
run_dic['coincidence']['H1L1']['analyze signal training'] = True
run_dic['coincidence']['H1L1']['back timeslides'] = {}
run_dic['coincidence']['H1L1']['back timeslides']['H1'] = np.zeros(1000)
run_dic['coincidence']['H1L1']['back timeslides']['L1'] = np.arange(1,1001,1)
run_dic['coincidence']['H1L1']['training timeslides'] = {}
run_dic['coincidence']['H1L1']['training timeslides']['H1'] = np.zeros(1000)
run_dic['coincidence']['H1L1']['training timeslides']['L1'] = np.arange(-1000,0,1)

#run_dic['coincidence']['H1V1'] = {}
#run_dic['coincidence']['H1V1']['ifos'] = ['H1','V1']
#run_dic['coincidence']['H1V1']['coincidence window'] = 0.025
#run_dic['coincidence']['H1V1']['coincidence snr thresh'] = 5.0
#run_dic['coincidence']['H1V1']['analyze 0lag'] = True
#run_dic['coincidence']['H1V1']['analyze back'] = True
#run_dic['coincidence']['H1V1']['analyze noise training'] = True
#run_dic['coincidence']['H1V1']['analyze signal training'] = True
#run_dic['coincidence']['H1V1']['back timeslides'] = {}
#run_dic['coincidence']['H1V1']['back timeslides']['H1'] = np.zeros(50)
#run_dic['coincidence']['H1V1']['back timeslides']['V1'] = np.arange(1,51,1)
#run_dic['coincidence']['H1V1']['training timeslides'] = {}
#run_dic['coincidence']['H1V1']['training timeslides']['H1'] = np.zeros(50)
#run_dic['coincidence']['H1V1']['training timeslides']['V1'] = np.arange(-50,0,1)

#run_dic['coincidence']['L1V1'] = {}
#run_dic['coincidence']['L1V1']['ifos'] = ['L1','V1']
#run_dic['coincidence']['L1V1']['coincidence window'] = 0.025
#run_dic['coincidence']['L1V1']['coincidence snr thresh'] = 5.0
#run_dic['coincidence']['L1V1']['analyze 0lag'] = True
#run_dic['coincidence']['L1V1']['analyze back'] = True
#run_dic['coincidence']['L1V1']['analyze noise training'] = True
#run_dic['coincidence']['L1V1']['analyze signal training'] = True
#run_dic['coincidence']['L1V1']['back timeslides'] = {}
#run_dic['coincidence']['L1V1']['back timeslides']['L1'] = np.zeros(50)
#run_dic['coincidence']['L1V1']['back timeslides']['V1'] = np.arange(1,51,1)
#run_dic['coincidence']['L1V1']['training timeslides'] = {}
#run_dic['coincidence']['L1V1']['training timeslides']['L1'] = np.zeros(50)
#run_dic['coincidence']['L1V1']['training timeslides']['V1'] = np.arange(-50,0,1)

#run_dic['coincidence']['H1L1V1'] = {}
#run_dic['coincidence']['H1L1V1']['ifos'] = ['H1','L1','V1']
#run_dic['coincidence']['H1L1V1']['coincidence window'] = 0.025
#run_dic['coincidence']['H1L1V1']['coincidence snr thresh'] = 5.0
#run_dic['coincidence']['H1L1V1']['analyze 0lag'] = True
#run_dic['coincidence']['H1L1V1']['analyze back'] = True
#run_dic['coincidence']['H1L1V1']['analyze noise training'] = True
#run_dic['coincidence']['H1L1V1']['analyze signal training'] = True
#run_dic['coincidence']['H1L1V1']['back timeslides'] = {}
#run_dic['coincidence']['H1L1V1']['back timeslides']['H1'] = np.zeros(50)
#run_dic['coincidence']['H1L1V1']['back timeslides']['L1'] = np.arange(1,51,1)
#run_dic['coincidence']['H1L1V1']['back timeslides']['V1'] = np.arange(-50,0,1)
#run_dic['coincidence']['H1L1V1']['training timeslides'] = {}
#run_dic['coincidence']['H1L1V1']['training timeslides']['H1'] = np.zeros(50)
#run_dic['coincidence']['H1L1V1']['training timeslides']['L1'] = np.arange(-50,0,1)
#run_dic['coincidence']['H1L1V1']['training timeslides']['V1'] = np.arange(1,51,1)

###
run_dic['LLRT'] = {}
run_dic['LLRT']['FAR thresh'] = 1.e-4 #1.e-6
run_dic['LLRT']['trials factor'] = 3

run_dic['LLRT']['calc info'] = {}
run_dic['LLRT']['calc info']['interp method'] = 'Grid Linear'
run_dic['LLRT']['calc info']['extrap method'] = 'Grid Nearest'

run_dic['LLRT']['param info'] = {}
run_dic['LLRT']['param info']['high_Q'] = {}
run_dic['LLRT']['param info']['high_Q']['logBSN_and_BCI'] = {}
run_dic['LLRT']['param info']['high_Q']['logBSN_and_BCI']['dimension'] = 2
run_dic['LLRT']['param info']['high_Q']['logBSN_and_BCI']['param names'] = ['logBSN','BCI']
run_dic['LLRT']['param info']['high_Q']['logBSN_and_BCI']['interp range'] = np.array([[0., 6.],[0., 30.]])
run_dic['LLRT']['param info']['low_Q'] = {}
run_dic['LLRT']['param info']['low_Q']['logBSN_and_BCI'] = {}
run_dic['LLRT']['param info']['low_Q']['logBSN_and_BCI']['dimension'] = 2
run_dic['LLRT']['param info']['low_Q']['logBSN_and_BCI']['param names'] = ['logBSN','BCI']
run_dic['LLRT']['param info']['low_Q']['logBSN_and_BCI']['interp range'] = np.array([[0., 6.],[0., 30.]])

run_dic['LLRT']['optimize signal training'] = {}
run_dic['LLRT']['optimize signal training']['high_Q'] = {}
run_dic['LLRT']['optimize signal training']['high_Q']['logBSN_and_BCI'] = {}
run_dic['LLRT']['optimize signal training']['high_Q']['logBSN_and_BCI']['optimization method'] = 'BFGS'
run_dic['LLRT']['optimize signal training']['high_Q']['logBSN_and_BCI']['optimization initial coords'] = np.array([np.nan,np.nan])
run_dic['LLRT']['optimize signal training']['low_Q'] = {}
run_dic['LLRT']['optimize signal training']['low_Q']['logBSN_and_BCI'] = {}
run_dic['LLRT']['optimize signal training']['low_Q']['logBSN_and_BCI']['optimization method'] = 'BFGS'
run_dic['LLRT']['optimize signal training']['low_Q']['logBSN_and_BCI']['optimization initial coords'] = np.array([np.nan,np.nan])

run_dic['LLRT']['optimize noise training'] = {}
run_dic['LLRT']['optimize noise training']['high_Q'] = {}
run_dic['LLRT']['optimize noise training']['high_Q']['logBSN_and_BCI'] = {}
run_dic['LLRT']['optimize noise training']['high_Q']['logBSN_and_BCI']['optimization method'] = 'BFGS'
run_dic['LLRT']['optimize noise training']['high_Q']['logBSN_and_BCI']['optimization initial coords'] = np.array([np.nan,np.nan])
run_dic['LLRT']['optimize noise training']['low_Q'] = {}
run_dic['LLRT']['optimize noise training']['low_Q']['logBSN_and_BCI'] = {}
run_dic['LLRT']['optimize noise training']['low_Q']['logBSN_and_BCI']['optimization method'] = 'BFGS'
run_dic['LLRT']['optimize noise training']['low_Q']['logBSN_and_BCI']['optimization initial coords'] = np.array([np.nan,np.nan])

run_dic['LLRT']['train signal data'] = {}
run_dic['LLRT']['train signal data']['high_Q'] = {}
run_dic['LLRT']['train signal data']['high_Q']['logBSN'] = {}
run_dic['LLRT']['train signal data']['high_Q']['logBSN']['data'] = np.transpose(np.array([np.nan]))
run_dic['LLRT']['train signal data']['high_Q']['logBSN']['KDE ranges'] = np.array([[0., 6.]])
run_dic['LLRT']['train signal data']['high_Q']['logBSN']['KDE bandwidths'] = np.array([np.nan])
run_dic['LLRT']['train signal data']['high_Q']['logBSN']['KDE points'] = np.array([100])
run_dic['LLRT']['train signal data']['high_Q']['BCI'] = {}
run_dic['LLRT']['train signal data']['high_Q']['BCI']['data'] = np.transpose(np.array([np.nan]))
run_dic['LLRT']['train signal data']['high_Q']['BCI']['KDE ranges'] = np.array([[0., 30.]])
run_dic['LLRT']['train signal data']['high_Q']['BCI']['KDE bandwidths'] = np.array([np.nan])
run_dic['LLRT']['train signal data']['high_Q']['BCI']['KDE points'] = np.array([100])
run_dic['LLRT']['train signal data']['low_Q'] = {}
run_dic['LLRT']['train signal data']['low_Q']['logBSN'] = {}
run_dic['LLRT']['train signal data']['low_Q']['logBSN']['data'] = np.transpose(np.array([np.nan]))
run_dic['LLRT']['train signal data']['low_Q']['logBSN']['KDE ranges'] = np.array([[0., 6.]])
run_dic['LLRT']['train signal data']['low_Q']['logBSN']['KDE bandwidths'] = np.array([np.nan])
run_dic['LLRT']['train signal data']['low_Q']['logBSN']['KDE points'] = np.array([100])
run_dic['LLRT']['train signal data']['low_Q']['BCI'] = {}
run_dic['LLRT']['train signal data']['low_Q']['BCI']['data'] = np.transpose(np.array([np.nan]))
run_dic['LLRT']['train signal data']['low_Q']['BCI']['KDE ranges'] = np.array([[0., 30.]])
run_dic['LLRT']['train signal data']['low_Q']['BCI']['KDE bandwidths'] = np.array([np.nan])
run_dic['LLRT']['train signal data']['low_Q']['BCI']['KDE points'] = np.array([100])

run_dic['LLRT']['train noise data'] = {}
run_dic['LLRT']['train noise data']['high_Q'] = {}
run_dic['LLRT']['train noise data']['high_Q']['logBSN'] = {}
run_dic['LLRT']['train noise data']['high_Q']['logBSN']['data'] = np.transpose(np.array([np.nan]))
run_dic['LLRT']['train noise data']['high_Q']['logBSN']['KDE ranges'] = np.array([[0., 6.]])
run_dic['LLRT']['train noise data']['high_Q']['logBSN']['KDE bandwidths'] = np.array([np.nan])
run_dic['LLRT']['train noise data']['high_Q']['logBSN']['KDE points'] = np.array([100])
run_dic['LLRT']['train noise data']['high_Q']['BCI'] = {}
run_dic['LLRT']['train noise data']['high_Q']['BCI']['data'] = np.transpose(np.array([np.nan]))
run_dic['LLRT']['train noise data']['high_Q']['BCI']['KDE ranges'] = np.array([[0., 30.]])
run_dic['LLRT']['train noise data']['high_Q']['BCI']['KDE bandwidths'] = np.array([np.nan])
run_dic['LLRT']['train noise data']['high_Q']['BCI']['KDE points'] = np.array([100])
run_dic['LLRT']['train noise data']['low_Q'] = {}
run_dic['LLRT']['train noise data']['low_Q']['logBSN'] = {}
run_dic['LLRT']['train noise data']['low_Q']['logBSN']['data'] = np.transpose(np.array([np.nan]))
run_dic['LLRT']['train noise data']['low_Q']['logBSN']['KDE ranges'] = np.array([[0., 6.]])
run_dic['LLRT']['train noise data']['low_Q']['logBSN']['KDE bandwidths'] = np.array([np.nan])
run_dic['LLRT']['train noise data']['low_Q']['logBSN']['KDE points'] = np.array([100])
run_dic['LLRT']['train noise data']['low_Q']['BCI'] = {}
run_dic['LLRT']['train noise data']['low_Q']['BCI']['data'] = np.transpose(np.array([np.nan]))
run_dic['LLRT']['train noise data']['low_Q']['BCI']['KDE ranges'] = np.array([[0., 30.]])
run_dic['LLRT']['train noise data']['low_Q']['BCI']['KDE bandwidths'] = np.array([np.nan])
run_dic['LLRT']['train noise data']['low_Q']['BCI']['KDE points'] = np.array([100])

run_dic['LLRT']['H1L1'] = {}
run_dic['LLRT']['H1L1']['back dic path'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/background_info/H1L1/ts_-2000.0_2000.0_noise_back_events.pkl_Cat1Cat4Cat2Cat3'
run_dic['LLRT']['H1L1']['back livetime'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/background_info/H1L1/Cat1Cat4Cat2Cat3_total_livetime.txt'
run_dic['LLRT']['H1L1']['high_Q'] = {}
run_dic['LLRT']['H1L1']['high_Q']['logBSN_and_BCI'] = {}
run_dic['LLRT']['H1L1']['high_Q']['logBSN_and_BCI']['oLIB signal kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/high_Q/H1L1/BSN_and_BCI_Signal_log_KDE_coords.npy'
run_dic['LLRT']['H1L1']['high_Q']['logBSN_and_BCI']['oLIB signal kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/high_Q/H1L1/BSN_and_BCI_Signal_log_KDE_values.npy'
run_dic['LLRT']['H1L1']['high_Q']['logBSN_and_BCI']['oLIB noise kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/high_Q/H1L1/BSN_and_BCI_Noise_log_KDE_coords.npy'
run_dic['LLRT']['H1L1']['high_Q']['logBSN_and_BCI']['oLIB noise kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/high_Q/H1L1/BSN_and_BCI_Noise_log_KDE_values.npy'
run_dic['LLRT']['H1L1']['low_Q'] = {}
run_dic['LLRT']['H1L1']['low_Q']['logBSN_and_BCI'] = {}
run_dic['LLRT']['H1L1']['low_Q']['logBSN_and_BCI']['oLIB signal kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/low_Q/H1L1/BSN_and_BCI_Signal_log_KDE_coords.npy'
run_dic['LLRT']['H1L1']['low_Q']['logBSN_and_BCI']['oLIB signal kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/low_Q/H1L1/BSN_and_BCI_Signal_log_KDE_values.npy'
run_dic['LLRT']['H1L1']['low_Q']['logBSN_and_BCI']['oLIB noise kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/low_Q/H1L1/BSN_and_BCI_Noise_log_KDE_coords.npy'
run_dic['LLRT']['H1L1']['low_Q']['logBSN_and_BCI']['oLIB noise kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/low_Q/H1L1/BSN_and_BCI_Noise_log_KDE_values.npy'

#run_dic['LLRT']['H1V1'] = {}
#run_dic['LLRT']['H1V1']['back dic path'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/background_info/H1L1/ts_-2000.0_2000.0_noise_back_events.pkl_Cat1Cat4Cat2Cat3'
#run_dic['LLRT']['H1V1']['back livetime'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/background_info/H1L1/Cat1Cat4Cat2Cat3_total_livetime.txt'
#run_dic['LLRT']['H1V1']['low_f'] = {}
#run_dic['LLRT']['H1V1']['low_f']['logBSN_and_BCI'] = {}
#run_dic['LLRT']['H1V1']['low_f']['logBSN_and_BCI']['oLIB signal kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Signal_log_KDE_coords.npy'
#run_dic['LLRT']['H1V1']['low_f']['logBSN_and_BCI']['oLIB signal kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Signal_log_KDE_values.npy'
#run_dic['LLRT']['H1V1']['low_f']['logBSN_and_BCI']['oLIB noise kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Noise_log_KDE_coords.npy'
#run_dic['LLRT']['H1V1']['low_f']['logBSN_and_BCI']['oLIB noise kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Noise_log_KDE_values.npy'

#run_dic['LLRT']['L1V1'] = {}
#run_dic['LLRT']['L1V1']['back dic path'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/background_info/H1L1/ts_-2000.0_2000.0_noise_back_events.pkl_Cat1Cat4Cat2Cat3'
#run_dic['LLRT']['L1V1']['back livetime'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/background_info/H1L1/Cat1Cat4Cat2Cat3_total_livetime.txt'
#run_dic['LLRT']['L1V1']['low_f'] = {}
#run_dic['LLRT']['L1V1']['low_f']['logBSN_and_BCI'] = {}
#run_dic['LLRT']['L1V1']['low_f']['logBSN_and_BCI']['oLIB signal kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Signal_log_KDE_coords.npy'
#run_dic['LLRT']['L1V1']['low_f']['logBSN_and_BCI']['oLIB signal kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Signal_log_KDE_values.npy'
#run_dic['LLRT']['L1V1']['low_f']['logBSN_and_BCI']['oLIB noise kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Noise_log_KDE_coords.npy'
#run_dic['LLRT']['L1V1']['low_f']['logBSN_and_BCI']['oLIB noise kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Noise_log_KDE_values.npy'

#run_dic['LLRT']['H1L1V1'] = {}
#run_dic['LLRT']['H1L1V1']['back dic path'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/background_info/H1L1/ts_-2000.0_2000.0_noise_back_events.pkl_Cat1Cat4Cat2Cat3'
#run_dic['LLRT']['H1L1V1']['back livetime'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/background_info/H1L1/Cat1Cat4Cat2Cat3_total_livetime.txt'
#run_dic['LLRT']['H1L1V1']['low_f'] = {}
#run_dic['LLRT']['H1L1V1']['low_f']['logBSN_and_BCI'] = {}
#run_dic['LLRT']['H1L1V1']['low_f']['logBSN_and_BCI']['oLIB signal kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Signal_log_KDE_coords.npy'
#run_dic['LLRT']['H1L1V1']['low_f']['logBSN_and_BCI']['oLIB signal kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Signal_log_KDE_values.npy'
#run_dic['LLRT']['H1L1V1']['low_f']['logBSN_and_BCI']['oLIB noise kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Noise_log_KDE_coords.npy'
#run_dic['LLRT']['H1L1V1']['low_f']['logBSN_and_BCI']['oLIB noise kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Noise_log_KDE_values.npy'

###
run_dic['training'] = {}
run_dic['training']['asd files'] = {}
run_dic['training']['asd files']['H1'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/training_info/O1-H1-ASD.dat'
run_dic['training']['asd files']['L1'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/training_info/O1-H1-ASD.dat'
#run_dic['training']['asd files']['V1'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/training_info/S6-V1-ASD.dat'

###
run_dic['prior ranges'] = {}
run_dic['prior ranges']['LIB window'] = 0.1
run_dic['prior ranges']['LIB stride'] = 4.0
run_dic['prior ranges']['min hrss'] = 3.0e-23
run_dic['prior ranges']['max hrss'] = 1.0e-15
run_dic['prior ranges']['min freq'] = 32
run_dic['prior ranges']['max freq'] = 1024
run_dic['prior ranges']['min quality'] = 0.1
run_dic['prior ranges']['max quality'] = 110

###
run_dic['search bins'] = {}
run_dic['search bins']['bin names'] = ['high_Q','low_Q']
run_dic['search bins']['high_Q'] = {}
run_dic['search bins']['high_Q']['low logBSN cut'] = 0
run_dic['search bins']['high_Q']['high logBSN cut'] = 6
run_dic['search bins']['high_Q']['low BCI cut'] = 0.
run_dic['search bins']['high_Q']['high BCI cut'] = np.inf
run_dic['search bins']['high_Q']['low freq cut'] = 48
run_dic['search bins']['high_Q']['high freq cut'] = 1024
run_dic['search bins']['high_Q']['low quality cut'] = 2.
run_dic['search bins']['high_Q']['high quality cut'] = 108.
run_dic['search bins']['high_Q']['BSN ratio cuts'] = [ ('H1','L1',9), ('H1','V1',np.inf), ('L1','V1',np.inf) ]
run_dic['search bins']['low_Q'] = {}
run_dic['search bins']['low_Q']['low logBSN cut'] = 0
run_dic['search bins']['low_Q']['high logBSN cut'] = 6
run_dic['search bins']['low_Q']['low BCI cut'] = 0.
run_dic['search bins']['low_Q']['high BCI cut'] = np.inf
run_dic['search bins']['low_Q']['low freq cut'] = 32
run_dic['search bins']['low_Q']['high freq cut'] = 1024
run_dic['search bins']['low_Q']['low quality cut'] = 0.1
run_dic['search bins']['low_Q']['high quality cut'] = 2.
run_dic['search bins']['low_Q']['BSN ratio cuts'] = [ ('H1','L1',9), ('H1','V1',np.inf), ('L1','V1',np.inf) ]

###
run_dic['collection and retraining'] = {}
run_dic['collection and retraining']['collect delay'] = 10000  #seconds
run_dic['collection and retraining']['retrain delay'] = 1  #days
run_dic['collection and retraining']['collect dir'] = '/home/ryan.lynch/public_html/ER10_back_train/test_results/'
run_dic['collection and retraining']['max back size'] = 5000
run_dic['collection and retraining']['min sig train size'] = 10
run_dic['collection and retraining']['max sig train size'] = 5000
run_dic['collection and retraining']['min noise train size'] = 10
run_dic['collection and retraining']['max noise train size'] = 5000
run_dic['collection and retraining']['back dir'] = '/home/ryan.lynch/public_html/ER10_back_train/test_background_info/'
run_dic['collection and retraining']['high_Q'] = {}
run_dic['collection and retraining']['high_Q']['retrain dir'] = '/home/ryan.lynch/public_html/ER10_back_train/test_LLRT_info/high_Q/'
run_dic['collection and retraining']['low_Q'] = {}
run_dic['collection and retraining']['low_Q']['retrain dir'] = '/home/ryan.lynch/public_html/ER10_back_train/test_LLRT_info/low_Q/'

###
run_dic['summary page'] = {}
run_dic['summary page']['user name'] = 'ryan.lynch'

run_dic['summary page']['H1L1'] = {}
run_dic['summary page']['H1L1']['label'] = 'low_frequency'
run_dic['summary page']['H1L1']['outdir'] = '/home/ryan.lynch/public_html/ER10_back_train/summary/H1L1_page/'

#=======================================================================

#Save the run dictionary to the run directory
if not os.path.exists(run_dic['config']['run dir']):
	os.makedirs(run_dic['config']['run dir'])
pickle.dump(run_dic,open(run_dic['config']['run dir']+'/main_run_dic.pkl','wt'))
