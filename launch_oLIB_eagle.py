#!/usr/bin/python

import sys
sys.path.insert(1,'/home/ryan.lynch/numpy/numpy-1.8.2-INSTALL/lib64/python2.7/site-packages')
import numpy as np
import os
import commands
import run_oLIB_eagle

#=======================================================================

#Config file for launching the oLIB pipeline

#initialize the run dictionary that will hold all info about run
run_dic = {}

###
run_dic['config'] = {}
run_dic['config']['wait'] = 5
run_dic['config']['max wait'] = 600
run_dic['config']['run dir'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/test_runs'
run_dic['config']['info dir'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/'
run_dic['config']['LIB bin dir'] = '/home/salvatore.vitale/lalsuites/burst_dev/o2_lib_20160720/bin/'
run_dic['config']['stride'] = 32
run_dic['config']['overlap'] = 2
run_dic['config']['sample freq'] = 2048
run_dic['config']['oSNR thresh'] = 5.0
run_dic['config']['dt clust'] = 0.1

###
run_dic['run mode'] = {}
run_dic['run mode']['line'] = 'Online'
run_dic['run mode']['inj runmode'] = 'NonInj'
run_dic['run mode']['DQ runmode'] = 'NonDQV'
run_dic['run mode']['train runmode'] = "Train"
run_dic['run mode']['gdb flag'] = True
run_dic['run mode']['email flag'] = True
run_dic['run mode']['email addresses'] = ['rlynch@mit.edu','8476930667@vtext.com']
run_dic['run mode']['LIB flag'] = True
run_dic['run mode']['tar results'] = False

###
run_dic['ifos'] = {}
run_dic['ifos']['names'] = ['H1','L1','V1']
run_dic['ifos']['H1'] = {}
run_dic['ifos']['H1']['channel type'] = 'H1_S6_llhoft'
run_dic['ifos']['H1']['channel name'] = 'LDAS-STRAIN'
run_dic['ifos']['H1']['state channel name'] = 'LSC-DATA_QUALITY_VECTOR'
run_dic['ifos']['H1']['run bitmask'] = 1
run_dic['ifos']['H1']['inj bitmask'] = 1  #448  #480
run_dic['ifos']['H1']['DQ'] = {}
run_dic['ifos']['H1']['DQ']['DQ channel names'] = ['LSC-DATA_QUALITY_VECTOR'] #[???]
run_dic['ifos']['H1']['DQ']['DQ bitmasks'] = [1]  #[???]
run_dic['ifos']['L1'] = {}
run_dic['ifos']['L1']['channel type'] = 'L1_S6_llhoft'
run_dic['ifos']['L1']['channel name'] = 'LDAS-STRAIN'
run_dic['ifos']['L1']['state channel name'] = 'LSC-DATA_QUALITY_VECTOR'
run_dic['ifos']['L1']['run bitmask'] = 1
run_dic['ifos']['L1']['inj bitmask'] = 1  #448  #480
run_dic['ifos']['L1']['DQ'] = {}
run_dic['ifos']['L1']['DQ']['DQ channel names'] = ['LSC-DATA_QUALITY_VECTOR']  #[???]
run_dic['ifos']['L1']['DQ']['DQ bitmasks'] = [1]  #[???]
run_dic['ifos']['V1'] = {}
run_dic['ifos']['V1']['channel type'] = 'V1_S6_llhoft'
run_dic['ifos']['V1']['channel name'] = 'h_16384Hz'
run_dic['ifos']['V1']['state channel name'] = 'Hrec_Flag_Quality'
run_dic['ifos']['V1']['run bitmask'] = 1
run_dic['ifos']['V1']['inj bitmask'] = 1  #448  #480
run_dic['ifos']['V1']['DQ'] = {}
run_dic['ifos']['V1']['DQ']['DQ channel names'] = ['Hrec_Flag_Quality']  #[???]
run_dic['ifos']['V1']['DQ']['DQ bitmasks'] = [1]  #[???]

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
run_dic['coincidence']['H1L1']['back timeslides']['H1'] = np.zeros(50)
run_dic['coincidence']['H1L1']['back timeslides']['L1'] = np.arange(1,51,1)
run_dic['coincidence']['H1L1']['training timeslides'] = {}
run_dic['coincidence']['H1L1']['training timeslides']['H1'] = np.zeros(50)
run_dic['coincidence']['H1L1']['training timeslides']['L1'] = np.arange(-50,0,1)

run_dic['coincidence']['H1V1'] = {}
run_dic['coincidence']['H1V1']['ifos'] = ['H1','V1']
run_dic['coincidence']['H1V1']['coincidence window'] = 0.025
run_dic['coincidence']['H1V1']['coincidence snr thresh'] = 5.0
run_dic['coincidence']['H1V1']['analyze 0lag'] = True
run_dic['coincidence']['H1V1']['analyze back'] = True
run_dic['coincidence']['H1V1']['analyze noise training'] = True
run_dic['coincidence']['H1V1']['analyze signal training'] = True
run_dic['coincidence']['H1V1']['back timeslides'] = {}
run_dic['coincidence']['H1V1']['back timeslides']['H1'] = np.zeros(50)
run_dic['coincidence']['H1V1']['back timeslides']['V1'] = np.arange(1,51,1)
run_dic['coincidence']['H1V1']['training timeslides'] = {}
run_dic['coincidence']['H1V1']['training timeslides']['H1'] = np.zeros(50)
run_dic['coincidence']['H1V1']['training timeslides']['V1'] = np.arange(-50,0,1)

run_dic['coincidence']['L1V1'] = {}
run_dic['coincidence']['L1V1']['ifos'] = ['L1','V1']
run_dic['coincidence']['L1V1']['coincidence window'] = 0.025
run_dic['coincidence']['L1V1']['coincidence snr thresh'] = 5.0
run_dic['coincidence']['L1V1']['analyze 0lag'] = True
run_dic['coincidence']['L1V1']['analyze back'] = True
run_dic['coincidence']['L1V1']['analyze noise training'] = True
run_dic['coincidence']['L1V1']['analyze signal training'] = True
run_dic['coincidence']['L1V1']['back timeslides'] = {}
run_dic['coincidence']['L1V1']['back timeslides']['L1'] = np.zeros(50)
run_dic['coincidence']['L1V1']['back timeslides']['V1'] = np.arange(1,51,1)
run_dic['coincidence']['L1V1']['training timeslides'] = {}
run_dic['coincidence']['L1V1']['training timeslides']['L1'] = np.zeros(50)
run_dic['coincidence']['L1V1']['training timeslides']['V1'] = np.arange(-50,0,1)

run_dic['coincidence']['H1L1V1'] = {}
run_dic['coincidence']['H1L1V1']['ifos'] = ['H1','L1','V1']
run_dic['coincidence']['H1L1V1']['coincidence window'] = 0.025
run_dic['coincidence']['H1L1V1']['coincidence snr thresh'] = 5.0
run_dic['coincidence']['H1L1V1']['analyze 0lag'] = True
run_dic['coincidence']['H1L1V1']['analyze back'] = True
run_dic['coincidence']['H1L1V1']['analyze noise training'] = True
run_dic['coincidence']['H1L1V1']['analyze signal training'] = True
run_dic['coincidence']['H1L1V1']['back timeslides'] = {}
run_dic['coincidence']['H1L1V1']['back timeslides']['H1'] = np.zeros(50)
run_dic['coincidence']['H1L1V1']['back timeslides']['L1'] = np.arange(1,51,1)
run_dic['coincidence']['H1L1V1']['back timeslides']['V1'] = np.arange(-50,0,1)
run_dic['coincidence']['H1L1V1']['training timeslides'] = {}
run_dic['coincidence']['H1L1V1']['training timeslides']['H1'] = np.zeros(50)
run_dic['coincidence']['H1L1V1']['training timeslides']['L1'] = np.arange(-50,0,1)
run_dic['coincidence']['H1L1V1']['training timeslides']['V1'] = np.arange(1,51,1)

###
run_dic['LLRT'] = {}
run_dic['LLRT']['FAR thresh'] = 1.e-5 #1.e-6

run_dic['LLRT']['param info'] = {}
run_dic['LLRT']['param info']['low_f'] = {}
run_dic['LLRT']['param info']['low_f']['logBSN_and_BCI'] = {}
run_dic['LLRT']['param info']['low_f']['logBSN_and_BCI']['dimension'] = 2
run_dic['LLRT']['param info']['low_f']['logBSN_and_BCI']['param names'] = ['logBSN','BCI']
run_dic['LLRT']['param info']['low_f']['logBSN_and_BCI']['interp range'] = np.array([[0., 6.],[0., 30.]])

run_dic['LLRT']['H1L1'] = {}
run_dic['LLRT']['H1L1']['back dic path'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/background_info/H1L1/ts_-2000.0_2000.0_noise_back_events.pkl_Cat1Cat4Cat2Cat3'
run_dic['LLRT']['H1L1']['back livetime'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/background_info/H1L1/Cat1Cat4Cat2Cat3_total_livetime.txt'
run_dic['LLRT']['H1L1']['low_f'] = {}
run_dic['LLRT']['H1L1']['low_f']['logBSN_and_BCI'] = {}
run_dic['LLRT']['H1L1']['low_f']['logBSN_and_BCI']['oLIB signal kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Signal_log_KDE_coords.npy'
run_dic['LLRT']['H1L1']['low_f']['logBSN_and_BCI']['oLIB signal kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Signal_log_KDE_values.npy'
run_dic['LLRT']['H1L1']['low_f']['logBSN_and_BCI']['oLIB noise kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Noise_log_KDE_coords.npy'
run_dic['LLRT']['H1L1']['low_f']['logBSN_and_BCI']['oLIB noise kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Noise_log_KDE_values.npy'

run_dic['LLRT']['H1V1'] = {}
run_dic['LLRT']['H1V1']['back dic path'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/background_info/H1L1/ts_-2000.0_2000.0_noise_back_events.pkl_Cat1Cat4Cat2Cat3'
run_dic['LLRT']['H1V1']['back livetime'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/background_info/H1L1/Cat1Cat4Cat2Cat3_total_livetime.txt'
run_dic['LLRT']['H1V1']['low_f'] = {}
run_dic['LLRT']['H1V1']['low_f']['logBSN_and_BCI'] = {}
run_dic['LLRT']['H1V1']['low_f']['logBSN_and_BCI']['oLIB signal kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Signal_log_KDE_coords.npy'
run_dic['LLRT']['H1V1']['low_f']['logBSN_and_BCI']['oLIB signal kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Signal_log_KDE_values.npy'
run_dic['LLRT']['H1V1']['low_f']['logBSN_and_BCI']['oLIB noise kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Noise_log_KDE_coords.npy'
run_dic['LLRT']['H1V1']['low_f']['logBSN_and_BCI']['oLIB noise kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Noise_log_KDE_values.npy'

run_dic['LLRT']['L1V1'] = {}
run_dic['LLRT']['L1V1']['back dic path'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/background_info/H1L1/ts_-2000.0_2000.0_noise_back_events.pkl_Cat1Cat4Cat2Cat3'
run_dic['LLRT']['L1V1']['back livetime'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/background_info/H1L1/Cat1Cat4Cat2Cat3_total_livetime.txt'
run_dic['LLRT']['L1V1']['low_f'] = {}
run_dic['LLRT']['L1V1']['low_f']['logBSN_and_BCI'] = {}
run_dic['LLRT']['L1V1']['low_f']['logBSN_and_BCI']['oLIB signal kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Signal_log_KDE_coords.npy'
run_dic['LLRT']['L1V1']['low_f']['logBSN_and_BCI']['oLIB signal kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Signal_log_KDE_values.npy'
run_dic['LLRT']['L1V1']['low_f']['logBSN_and_BCI']['oLIB noise kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Noise_log_KDE_coords.npy'
run_dic['LLRT']['L1V1']['low_f']['logBSN_and_BCI']['oLIB noise kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Noise_log_KDE_values.npy'

run_dic['LLRT']['H1L1V1'] = {}
run_dic['LLRT']['H1L1V1']['back dic path'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/background_info/H1L1/ts_-2000.0_2000.0_noise_back_events.pkl_Cat1Cat4Cat2Cat3'
run_dic['LLRT']['H1L1V1']['back livetime'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/background_info/H1L1/Cat1Cat4Cat2Cat3_total_livetime.txt'
run_dic['LLRT']['H1L1V1']['low_f'] = {}
run_dic['LLRT']['H1L1V1']['low_f']['logBSN_and_BCI'] = {}
run_dic['LLRT']['H1L1V1']['low_f']['logBSN_and_BCI']['oLIB signal kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Signal_log_KDE_coords.npy'
run_dic['LLRT']['H1L1V1']['low_f']['logBSN_and_BCI']['oLIB signal kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Signal_log_KDE_values.npy'
run_dic['LLRT']['H1L1V1']['low_f']['logBSN_and_BCI']['oLIB noise kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Noise_log_KDE_coords.npy'
run_dic['LLRT']['H1L1V1']['low_f']['logBSN_and_BCI']['oLIB noise kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/H1L1/BSN_and_BCI_Noise_log_KDE_values.npy'

###
run_dic['training'] = {}
run_dic['training']['asd files'] = {}
run_dic['training']['asd files']['H1'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/training_info/S6-H1-ASD.dat'
run_dic['training']['asd files']['L1'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/training_info/S6-H1-ASD.dat'
run_dic['training']['asd files']['V1'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/training_info/S6-V1-ASD.dat'

###
run_dic['prior ranges'] = {}
run_dic['prior ranges']['LIB window'] = 0.1
run_dic['prior ranges']['min hrss'] = 1.0e-22  #3.3e-23
run_dic['prior ranges']['max hrss'] = 1.0e-15
run_dic['prior ranges']['min freq'] = 32
run_dic['prior ranges']['max freq'] = 1024
run_dic['prior ranges']['min quality'] = 0.1
run_dic['prior ranges']['max quality'] = 110

###
run_dic['search bins'] = {}
run_dic['search bins']['bin names'] = ['low_f']
run_dic['search bins']['low_f'] = {}
run_dic['search bins']['low_f']['low logBSN cut'] = 0
run_dic['search bins']['low_f']['high logBSN cut'] = 6
run_dic['search bins']['low_f']['low BCI cut'] = 1
run_dic['search bins']['low_f']['high BCI cut'] = np.inf
run_dic['search bins']['low_f']['low freq cut'] = 48
run_dic['search bins']['low_f']['high freq cut'] = 1024
run_dic['search bins']['low_f']['low quality cut'] = 2
run_dic['search bins']['low_f']['high quality cut'] = 108

#Decide what time to start running on if in online mode
if run_dic['run mode']['line'] == 'Online':
	if os.path.exists(run_dic['config']['run dir']+'/current_start.txt'):
		#Continue past run based on saved timestamp
		run_dic['config']['initial start'] = int(np.genfromtxt(run_dic['config']['run dir']+'/current_start.txt'))
	else:
		#Start running on current timestamp
		run_dic['config']['initial start'] = int(commands.getstatusoutput('%s/lalapps_tconvert now'%run_dic['config']['LIB bin dir'])[1]) - 500

#Launch oLIB
run_oLIB_eagle.executable(run_dic=run_dic)
