#!/usr/bin/python

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
run_dic['config']['run dir'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/test_runs/'
run_dic['config']['info dir'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/'
run_dic['config']['LIB bin dir'] = '/home/salvatore.vitale/lalsuites/burst_dev/noflags_opt/bin/'
run_dic['config']['initial start'] = None
run_dic['config']['stride'] = 32
run_dic['config']['overlap'] = 2
run_dic['config']['run bitmask'] = 3
run_dic['config']['inj bitmask'] = 448  #480
run_dic['config']['sample freq'] = 2048
run_dic['config']['oSNR thresh'] = 5
run_dic['config']['dt clust'] = 0.1

###
run_dic['run mode'] = {}
run_dic['run mode']['line'] = 'Online'
run_dic['run mode']['inj runmode'] = 'NonInj'
run_dic['run mode']['train runmode'] = "NonTrain"
run_dic['run mode']['gdb flag'] = False
run_dic['run mode']['LIB flag'] = False
run_dic['run mode']['tar Omicron'] = False
run_dic['run mode']['tar LIB'] = False

###
run_dic['ifos'] = {}
run_dic['ifos']['names'] = ['H1','L1']
run_dic['ifos']['H1'] = {}
run_dic['ifos']['H1']['channel type'] = 'H1_HOFT_C01'
run_dic['ifos']['H1']['channel name'] = 'DCS-CALIB_STRAIN_C01'
run_dic['ifos']['H1']['state channel name'] = 'DCS-CALIB_STATE_VECTOR_C01'
run_dic['ifos']['L1'] = {}
run_dic['ifos']['L1']['channel type'] = 'L1_HOFT_C01'
run_dic['ifos']['L1']['channel name'] = 'DCS-CALIB_STRAIN_C01'
run_dic['ifos']['L1']['state channel name'] = 'DCS-CALIB_STATE_VECTOR_C01'
#run_dic['ifos']['V1'] = {}
#run_dic['ifos']['V1']['channel type'] = None
#run_dic['ifos']['V1']['channel name'] = None
#run_dic['ifos']['V1']['state channel name'] = None

###
run_dic['coincidence'] = {}

run_dic['coincidence']['H1L1'] = {}
run_dic['coincidence']['H1L1']['ifos'] = ['H1','L1']
run_dic['coincidence']['H1L1']['coincidence window'] = 0.015
run_dic['coincidence']['H1L1']['coincidence snr thresh'] = 5.0*np.sqrt(2.)
run_dic['coincidence']['H1L1']['analyze 0lag'] = True
run_dic['coincidence']['H1L1']['analyze back'] = True
run_dic['coincidence']['H1L1']['analyze noise training'] = False
run_dic['coincidence']['H1L1']['analyze signal training'] = False
run_dic['coincidence']['H1L1']['back timeslides'] = {}
run_dic['coincidence']['H1L1']['back timeslides']['H1'] = np.zeros(50)
run_dic['coincidence']['H1L1']['back timeslides']['L1'] = np.arange(1,51,1)
run_dic['coincidence']['H1L1']['training timeslides'] = {}
run_dic['coincidence']['H1L1']['training timeslides']['H1'] = np.zeros(50)
run_dic['coincidence']['H1L1']['training timeslides']['L1'] = np.arange(-50,0,1)

#run_dic['coincidence']['H1V1'] = {}
#run_dic['coincidence']['H1V1']['ifos'] = ['H1','V1']
#run_dic['coincidence']['H1V1']['coincidence window'] = coincidence_window_H1V1
#run_dic['coincidence']['H1V1']['coincidence snr thresh'] = coincidence_snr_thresh_H1V1
#run_dic['coincidence']['H1V1']['analyze 0lag'] = True
#run_dic['coincidence']['H1V1']['analyze back'] = True
#run_dic['coincidence']['H1V1']['analyze noise training'] = True
#run_dic['coincidence']['H1V1']['analyze signal training'] = True
#run_dic['coincidence']['H1V1']['back timeslides'] = {}
#run_dic['coincidence']['H1V1']['back timeslides']['H1'] = back_time_slides_H1V1_H1
#run_dic['coincidence']['H1V1']['back timeslides']['V1'] = back_time_slides_H1V1_V1
#run_dic['coincidence']['H1V1']['training timeslides'] = {}
#run_dic['coincidence']['H1V1']['training timeslides']['H1'] = train_time_slides_H1V1_H1
#run_dic['coincidence']['H1V1']['training timeslides']['V1'] = train_time_slides_H1V1_V1

#run_dic['coincidence']['L1V1'] = {}
#run_dic['coincidence']['L1V1']['ifos'] = ['L1','V1']
#run_dic['coincidence']['L1V1']['coincidence window'] = coincidence_window_L1V1
#run_dic['coincidence']['L1V1']['coincidence snr thresh'] = coincidence_snr_thresh_L1V1
#run_dic['coincidence']['L1V1']['analyze 0lag'] = True
#run_dic['coincidence']['L1V1']['analyze back'] = True
#run_dic['coincidence']['L1V1']['analyze noise training'] = True
#run_dic['coincidence']['L1V1']['analyze signal training'] = True
#run_dic['coincidence']['L1V1']['back timeslides'] = {}
#run_dic['coincidence']['L1V1']['back timeslides']['L1'] = back_time_slides_L1V1_L1
#run_dic['coincidence']['L1V1']['back timeslides']['V1'] = back_time_slides_L1V1_V1
#run_dic['coincidence']['L1V1']['training timeslides'] = {}
#run_dic['coincidence']['L1V1']['training timeslides']['L1'] = train_time_slides_L1V1_L1
#run_dic['coincidence']['L1V1']['training timeslides']['V1'] = train_time_slides_L1V1_V1

#run_dic['coincidence']['H1L1V1'] = {}
#run_dic['coincidence']['H1L1V1']['ifos'] = ['H1','L1','V1']
#run_dic['coincidence']['H1L1V1']['coincidence window'] = coincidence_window_H1L1V1
#run_dic['coincidence']['H1L1V1']['coincidence snr thresh'] = coincidence_snr_thresh_H1L1V1
#run_dic['coincidence']['H1L1V1']['analyze 0lag'] = True
#run_dic['coincidence']['H1L1V1']['analyze back'] = True
#run_dic['coincidence']['H1L1V1']['analyze noise training'] = True
#run_dic['coincidence']['H1L1V1']['analyze signal training'] = True
#run_dic['coincidence']['H1L1V1']['back timeslides'] = {}
#run_dic['coincidence']['H1L1V1']['back timeslides']['H1'] = back_time_slides_H1L1V1_H1
#run_dic['coincidence']['H1L1V1']['back timeslides']['L1'] = back_time_slides_H1L1V1_L1
#run_dic['coincidence']['H1L1V1']['back timeslides']['V1'] = back_time_slides_H1L1V1_V1
#run_dic['coincidence']['H1L1V1']['training timeslides'] = {}
#run_dic['coincidence']['H1L1V1']['training timeslides']['H1'] = train_time_slides_H1L1V1_H1
#run_dic['coincidence']['H1L1V1']['training timeslides']['L1'] = train_time_slides_H1L1V1_L1
#run_dic['coincidence']['H1L1V1']['training timeslides']['V1'] = train_time_slides_H1L1V1_V1

###
run_dic['LLRT'] = {}
run_dic['LLRT']['FAR thresh'] = 1.e-6

run_dic['LLRT']['param info'] = {}
run_dic['LLRT']['param info']['low f'] = {}
run_dic['LLRT']['param info']['low f']['logBSN_and_BCI'] = {}
run_dic['LLRT']['param info']['low f']['logBSN_and_BCI']['dimension'] = 2
run_dic['LLRT']['param info']['low f']['logBSN_and_BCI']['param names'] = ['logBSN','BCI']
run_dic['LLRT']['param info']['low f']['logBSN_and_BCI']['interp range'] = np.array([[0., 6.],[0., 30.]])

run_dic['LLRT']['H1L1'] = {}
run_dic['LLRT']['H1L1']['back dic path'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/background_info/ts_-2000.0_2000.0_noise_back_events.pkl_Cat1Cat4Cat2Cat3'
run_dic['LLRT']['H1L1']['back livetime'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/background_info/Cat1Cat4Cat2Cat3_total_livetime.txt'
run_dic['LLRT']['H1L1']['low f'] = {}
run_dic['LLRT']['H1L1']['low f']['logBSN_and_BCI'] = {}
run_dic['LLRT']['H1L1']['low f']['logBSN_and_BCI']['oLIB signal kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/BSN_and_BCI_Signal_log_KDE_coords.npy'
run_dic['LLRT']['H1L1']['low f']['logBSN_and_BCI']['oLIB signal kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/BSN_and_BCI_Signal_log_KDE_values.npy'
run_dic['LLRT']['H1L1']['low f']['logBSN_and_BCI']['oLIB noise kde coords'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/BSN_and_BCI_Noise_log_KDE_coords.npy'
run_dic['LLRT']['H1L1']['low f']['logBSN_and_BCI']['oLIB noise kde values'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/LLRT_info/BSN_and_BCI_Noise_log_KDE_values.npy'

#run_dic['LLRT']['H1V1'] = {}
#run_dic['LLRT']['H1V1']['back dic path'] = back_dic_path_H1V1
#run_dic['LLRT']['H1V1']['back livetime'] = back_livetime_H1V1
#run_dic['LLRT']['H1V1']['low f'] = {}
#run_dic['LLRT']['H1V1']['low f']['logBSN_and_BCI'] = {}
#run_dic['LLRT']['H1V1']['low f']['logBSN_and_BCI']['oLIB signal kde coords'] = oLIB_signal_kde_coords_H1V1
#run_dic['LLRT']['H1V1']['low f']['logBSN_and_BCI']['oLIB signal kde values'] = oLIB_signal_kde_values_H1V1
#run_dic['LLRT']['H1V1']['low f']['logBSN_and_BCI']['oLIB noise kde coords'] = oLIB_noise_kde_coords_H1V1
#run_dic['LLRT']['H1V1']['low f']['logBSN_and_BCI']['oLIB noise kde values'] = oLIB_noise_kde_values_H1V1

#run_dic['LLRT']['L1V1'] = {}
#run_dic['LLRT']['L1V1']['back dic path'] = back_dic_path_L1V1
#run_dic['LLRT']['L1V1']['back livetime'] = back_livetime_L1V1
#run_dic['LLRT']['L1V1']['low f'] = {}
#run_dic['LLRT']['L1V1']['low f']['logBSN_and_BCI'] = {}
#run_dic['LLRT']['L1V1']['low f']['logBSN_and_BCI']['oLIB signal kde coords'] = oLIB_signal_kde_coords_L1V1
#run_dic['LLRT']['L1V1']['low f']['logBSN_and_BCI']['oLIB signal kde values'] = oLIB_signal_kde_values_L1V1
#run_dic['LLRT']['L1V1']['low f']['logBSN_and_BCI']['oLIB noise kde coords'] = oLIB_noise_kde_coords_L1V1
#run_dic['LLRT']['L1V1']['low f']['logBSN_and_BCI']['oLIB noise kde values'] = oLIB_noise_kde_values_L1V1

#run_dic['LLRT']['H1L1V1'] = {}
#run_dic['LLRT']['H1L1V1']['back dic path'] = back_dic_path_H1L1V1
#run_dic['LLRT']['H1L1V1']['back livetime'] = back_livetime_H1L1V1
#run_dic['LLRT']['H1L1V1']['low f'] = {}
#run_dic['LLRT']['H1L1V1']['low f']['logBSN_and_BCI'] = {}
#run_dic['LLRT']['H1L1V1']['low f']['logBSN_and_BCI']['oLIB signal kde coords'] = oLIB_signal_kde_coords_H1L1V1
#run_dic['LLRT']['H1L1V1']['low f']['logBSN_and_BCI']['oLIB signal kde values'] = oLIB_signal_kde_values_H1L1V1
#run_dic['LLRT']['H1L1V1']['low f']['logBSN_and_BCI']['oLIB noise kde coords'] = oLIB_noise_kde_coords_H1L1V1
#run_dic['LLRT']['H1L1V1']['low f']['logBSN_and_BCI']['oLIB noise kde values'] = oLIB_noise_kde_values_H1L1V1

###
run_dic['training'] = {}
run_dic['training']['asd files'] = {}
run_dic['training']['asd files']['H1'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/training_info/O1-H1-ASD.dat'
run_dic['training']['asd files']['L1'] = '/home/ryan.lynch/2nd_pipeline/pipeline_eagle/training_info/O1-H1-ASD.dat'
#run_dic['training']['asd files']['V1'] = None

###
run_dic['prior ranges'] = {}
run_dic['prior ranges']['LIB window'] = 0.1
run_dic['prior ranges']['min hrss'] = 3.3e-23
run_dic['prior ranges']['max hrss'] = 1.0e-15
run_dic['prior ranges']['min freq'] = 32
run_dic['prior ranges']['max freq'] = 1024
run_dic['prior ranges']['min quality'] = 0.1
run_dic['prior ranges']['max quality'] = 110

###
run_dic['search bins'] = {}
run_dic['search bins']['bin names'] = ['low f']
run_dic['search bins']['low f'] = {}
run_dic['search bins']['low f']['low logBSN cut'] = 0
run_dic['search bins']['low f']['high logBSN cut'] = 6
run_dic['search bins']['low f']['low BCI cut'] = 1
run_dic['search bins']['low f']['high BCI cut'] = np.inf
run_dic['search bins']['low f']['low freq cut'] = 48
run_dic['search bins']['low f']['high freq cut'] = 1024
run_dic['search bins']['low f']['low quality cut'] = 2
run_dic['search bins']['low f']['high quality cut'] = 108

#Decide what time to start running on if in online mode
if run_dic['run mode']['line'] == 'Online':
	if os.path.exists(run_dic['config']['run dir']+'/current_start.txt'):
		#Continue past run based on saved timestamp
		run_dic['config']['initial start'] = int(np.genfromtxt(run_dic['config']['run dir']+'/current_start.txt'))
	else:
		#Start running on current timestamp
		run_dic['config']['initial start'] = int(commands.getstatusoutput('%s/lalapps_tconvert now'%bindir)[1]) - 500

#Launch oLIB
run_oLIB_eagle.executable(run_dic=run_dic)
