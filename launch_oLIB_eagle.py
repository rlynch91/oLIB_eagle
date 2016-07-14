#!/usr/bin/python

import numpy as np
import os
import commands
import run_2ndpipe_beta

#=======================================================================

#Config file for launching the oLIB pipeline

#initialize the run dictionary that will hold all info about run
run_dic = {}

###
run_dic['config'] = {}
run_dic['config']['wait'] = wait
run_dic['config']['max wait'] = max_wait
run_dic['config']['run dir'] = rundir
run_dic['config']['info dir'] = infodir
run_dic['config']['LIB bin dir'] = bindir
run_dic['config']['initial start'] = initial_start
run_dic['config']['stride'] = stride
run_dic['config']['overlap'] = overlap
run_dic['config']['bitmask'] = bitmask
run_dic['config']['sample freq'] = sample_freq
run_dic['config']['oSNR thresh'] = snr_thresh
run_dic['config']['dt clust'] = dt_clust

###
run_dic['run mode'] = {}
run_dic['run mode']['line'] = line
run_dic['run mode']['inj runmode'] = inj_runmode
run_dic['run mode']['train runmode'] = train_runmode
run_dic['run mode']['gdb flag'] = gdb_flag
run_dic['run mode']['LIB flag'] = LIB_flag
run_dic['run mode']['tar Omicron'] = tar_omicron
run_dic['run mode']['tar LIB'] = tar_lib

###
run_dic['ifos'] = {}
run_dic['ifos']['names'] = ['H1','L1','V1']
run_dic['ifos']['H1'] = {}
run_dic['ifos']['H1']['channel type'] = channel_types[?]
run_dic['ifos']['H1']['channel name'] = channel_names[?]
run_dic['ifos']['H1']['state channel name'] = state_channels[?]
run_dic['ifos']['L1'] = {}
run_dic['ifos']['L1']['channel type'] = channel_types[?]
run_dic['ifos']['L1']['channel name'] = channel_names[?]
run_dic['ifos']['L1']['state channel name'] = state_channels[?]
run_dic['ifos']['V1'] = {}
run_dic['ifos']['V1']['channel type'] = channel_types[?]
run_dic['ifos']['V1']['channel name'] = channel_names[?]
run_dic['ifos']['V1']['state channel name'] = state_channels[?]

###
run_dic['coincidence'] = {}

run_dic['coincidence']['H1L1'] = {}
run_dic['coincidence']['H1L1']['ifos'] = ['H1','L1']
run_dic['coincidence']['H1L1']['coincidence window'] = coincidence_window_H1L1
run_dic['coincidence']['H1L1']['coincidence snr thresh'] = coincidence_snr_thresh_H1L1
run_dic['coincidence']['H1L1']['analyze 0lag'] = True
run_dic['coincidence']['H1L1']['analyze back'] = True
run_dic['coincidence']['H1L1']['analyze noise training'] = True
run_dic['coincidence']['H1L1']['analyze signal training'] = True
run_dic['coincidence']['H1L1']['back timeslides'] = {}
run_dic['coincidence']['H1L1']['back timeslides']['H1'] = back_time_slides_H1L1_H1
run_dic['coincidence']['H1L1']['back timeslides']['L1'] = back_time_slides_H1L1_L1
run_dic['coincidence']['H1L1']['training timeslides'] = {}
run_dic['coincidence']['H1L1']['training timeslides']['H1'] = train_time_slides_H1L1_H1
run_dic['coincidence']['H1L1']['training timeslides']['L1'] = train_time_slides_H1L1_L1

run_dic['coincidence']['H1V1'] = {}
run_dic['coincidence']['H1V1']['ifos'] = ['H1','V1']
run_dic['coincidence']['H1V1']['coincidence window'] = coincidence_window_H1V1
run_dic['coincidence']['H1V1']['coincidence snr thresh'] = coincidence_snr_thresh_H1V1
run_dic['coincidence']['H1V1']['analyze 0lag'] = True
run_dic['coincidence']['H1V1']['analyze back'] = True
run_dic['coincidence']['H1V1']['analyze noise training'] = True
run_dic['coincidence']['H1V1']['analyze signal training'] = True
run_dic['coincidence']['H1V1']['back timeslides'] = {}
run_dic['coincidence']['H1V1']['back timeslides']['H1'] = back_time_slides_H1V1_H1
run_dic['coincidence']['H1V1']['back timeslides']['V1'] = back_time_slides_H1V1_V1
run_dic['coincidence']['H1V1']['training timeslides'] = {}
run_dic['coincidence']['H1V1']['training timeslides']['H1'] = train_time_slides_H1V1_H1
run_dic['coincidence']['H1V1']['training timeslides']['V1'] = train_time_slides_H1V1_V1

run_dic['coincidence']['L1V1'] = {}
run_dic['coincidence']['L1V1']['ifos'] = ['L1','V1']
run_dic['coincidence']['L1V1']['coincidence window'] = coincidence_window_L1V1
run_dic['coincidence']['L1V1']['coincidence snr thresh'] = coincidence_snr_thresh_L1V1
run_dic['coincidence']['L1V1']['analyze 0lag'] = True
run_dic['coincidence']['L1V1']['analyze back'] = True
run_dic['coincidence']['L1V1']['analyze noise training'] = True
run_dic['coincidence']['L1V1']['analyze signal training'] = True
run_dic['coincidence']['L1V1']['back timeslides'] = {}
run_dic['coincidence']['L1V1']['back timeslides']['L1'] = back_time_slides_L1V1_L1
run_dic['coincidence']['L1V1']['back timeslides']['V1'] = back_time_slides_L1V1_V1
run_dic['coincidence']['L1V1']['training timeslides'] = {}
run_dic['coincidence']['L1V1']['training timeslides']['L1'] = train_time_slides_L1V1_L1
run_dic['coincidence']['L1V1']['training timeslides']['V1'] = train_time_slides_L1V1_V1

run_dic['coincidence']['H1L1V1'] = {}
run_dic['coincidence']['H1L1V1']['ifos'] = ['H1','L1','V1']
run_dic['coincidence']['H1L1V1']['coincidence window'] = coincidence_window_H1L1V1
run_dic['coincidence']['H1L1V1']['coincidence snr thresh'] = coincidence_snr_thresh_H1L1V1
run_dic['coincidence']['H1L1V1']['analyze 0lag'] = True
run_dic['coincidence']['H1L1V1']['analyze back'] = True
run_dic['coincidence']['H1L1V1']['analyze noise training'] = True
run_dic['coincidence']['H1L1V1']['analyze signal training'] = True
run_dic['coincidence']['H1L1V1']['back timeslides'] = {}
run_dic['coincidence']['H1L1V1']['back timeslides']['H1'] = back_time_slides_H1L1V1_H1
run_dic['coincidence']['H1L1V1']['back timeslides']['L1'] = back_time_slides_H1L1V1_L1
run_dic['coincidence']['H1L1V1']['back timeslides']['V1'] = back_time_slides_H1L1V1_V1
run_dic['coincidence']['H1L1V1']['training timeslides'] = {}
run_dic['coincidence']['H1L1V1']['training timeslides']['H1'] = train_time_slides_H1L1V1_H1
run_dic['coincidence']['H1L1V1']['training timeslides']['L1'] = train_time_slides_H1L1V1_L1
run_dic['coincidence']['H1L1V1']['training timeslides']['V1'] = train_time_slides_H1L1V1_V1

###
run_dic['LLRT'] = {}
run_dic['LLRT']['FAR thresh'] = FAR_thresh

run_dic['LLRT']['param info'] = {}
run_dic['LLRT']['param info']['low f'] = {}
run_dic['LLRT']['param info']['low f']['logBSN_and_BCI'] = {}
run_dic['LLRT']['param info']['low f']['logBSN_and_BCI']['dimension'] = 2
run_dic['LLRT']['param info']['low f']['logBSN_and_BCI']['param names'] = ['logBSN','BCI']
run_dic['LLRT']['param info']['low f']['logBSN_and_BCI']['interp range'] = np.array([[??., ??],[??, ??]])

run_dic['LLRT']['H1L1'] = {}
run_dic['LLRT']['H1L1']['back dic path'] = back_dic_path_H1L1
run_dic['LLRT']['H1L1']['back livetime'] = back_livetime_H1L1
run_dic['LLRT']['H1L1']['low f'] = {}
run_dic['LLRT']['H1L1']['low f']['logBSN_and_BCI'] = {}
run_dic['LLRT']['H1L1']['low f']['logBSN_and_BCI']['oLIB signal kde coords'] = oLIB_signal_kde_coords_H1L1
run_dic['LLRT']['H1L1']['low f']['logBSN_and_BCI']['oLIB signal kde values'] = oLIB_signal_kde_values_H1L1
run_dic['LLRT']['H1L1']['low f']['logBSN_and_BCI']['oLIB noise kde coords'] = oLIB_noise_kde_coords_H1L1
run_dic['LLRT']['H1L1']['low f']['logBSN_and_BCI']['oLIB noise kde values'] = oLIB_noise_kde_values_H1L1

run_dic['LLRT']['H1V1'] = {}
run_dic['LLRT']['H1V1']['back dic path'] = back_dic_path_H1V1
run_dic['LLRT']['H1V1']['back livetime'] = back_livetime_H1V1
run_dic['LLRT']['H1V1']['low f'] = {}
run_dic['LLRT']['H1V1']['low f']['logBSN_and_BCI'] = {}
run_dic['LLRT']['H1V1']['low f']['logBSN_and_BCI']['oLIB signal kde coords'] = oLIB_signal_kde_coords_H1V1
run_dic['LLRT']['H1V1']['low f']['logBSN_and_BCI']['oLIB signal kde values'] = oLIB_signal_kde_values_H1V1
run_dic['LLRT']['H1V1']['low f']['logBSN_and_BCI']['oLIB noise kde coords'] = oLIB_noise_kde_coords_H1V1
run_dic['LLRT']['H1V1']['low f']['logBSN_and_BCI']['oLIB noise kde values'] = oLIB_noise_kde_values_H1V1

run_dic['LLRT']['L1V1'] = {}
run_dic['LLRT']['L1V1']['back dic path'] = back_dic_path_L1V1
run_dic['LLRT']['L1V1']['back livetime'] = back_livetime_L1V1
run_dic['LLRT']['L1V1']['low f'] = {}
run_dic['LLRT']['L1V1']['low f']['logBSN_and_BCI'] = {}
run_dic['LLRT']['L1V1']['low f']['logBSN_and_BCI']['oLIB signal kde coords'] = oLIB_signal_kde_coords_L1V1
run_dic['LLRT']['L1V1']['low f']['logBSN_and_BCI']['oLIB signal kde values'] = oLIB_signal_kde_values_L1V1
run_dic['LLRT']['L1V1']['low f']['logBSN_and_BCI']['oLIB noise kde coords'] = oLIB_noise_kde_coords_L1V1
run_dic['LLRT']['L1V1']['low f']['logBSN_and_BCI']['oLIB noise kde values'] = oLIB_noise_kde_values_L1V1

run_dic['LLRT']['H1L1V1'] = {}
run_dic['LLRT']['H1L1V1']['back dic path'] = back_dic_path_H1L1V1
run_dic['LLRT']['H1L1V1']['back livetime'] = back_livetime_H1L1V1
run_dic['LLRT']['H1L1V1']['low f'] = {}
run_dic['LLRT']['H1L1V1']['low f']['logBSN_and_BCI'] = {}
run_dic['LLRT']['H1L1V1']['low f']['logBSN_and_BCI']['oLIB signal kde coords'] = oLIB_signal_kde_coords_H1L1V1
run_dic['LLRT']['H1L1V1']['low f']['logBSN_and_BCI']['oLIB signal kde values'] = oLIB_signal_kde_values_H1L1V1
run_dic['LLRT']['H1L1V1']['low f']['logBSN_and_BCI']['oLIB noise kde coords'] = oLIB_noise_kde_coords_H1L1V1
run_dic['LLRT']['H1L1V1']['low f']['logBSN_and_BCI']['oLIB noise kde values'] = oLIB_noise_kde_values_H1L1V1

###
run_dic['training'] = {}
run_dic['training']['asd files'] = {}
run_dic['training']['asd files']['H1'] = asd_file
run_dic['training']['asd files']['L1'] = asd_file
run_dic['training']['asd files']['V1'] = asd_file

###
run_dic['prior ranges'] = {}
run_dic['prior ranges']['LIB window'] = LIB_window
run_dic['prior ranges']['min hrss'] = min_hrss
run_dic['prior ranges']['max hrss'] = max_hrss
run_dic['prior ranges']['min freq'] = min_freq
run_dic['prior ranges']['max freq'] = max_freq
run_dic['prior ranges']['min quality'] = min_quality
run_dic['prior ranges']['max quality'] = max_quality

###
run_dic['search bins'] = {}
run_dic['search bins']['bin names'] = ['low f']
run_dic['search bins']['low f'] = {}
run_dic['search bins']['low f']['low logBSN cut'] = low_logBSN_cut
run_dic['search bins']['low f']['high logBSN cut'] = high_logBSN_cut
run_dic['search bins']['low f']['low BCI cut'] = low_BCI_cut
run_dic['search bins']['low f']['high BCI cut'] = high_BCI_cut
run_dic['search bins']['low f']['low freq cut'] = low_freq_cut
run_dic['search bins']['low f']['high freq cut'] = high_freq_cut
run_dic['search bins']['low f']['low quality cut'] = low_quality_cut
run_dic['search bins']['low f']['high quality cut'] = high_quality_cut

#Decide what time to start running on if in online mode
if run_dic['run mode']['line'] == 'Online':
	if os.path.exists(rundir+'/current_start.txt'):
		#Continue past run based on saved timestamp
		run_dic['config']['initial start'] = int(np.genfromtxt(rundir+'/current_start.txt'))
	else:
		#Start running on current timestamp
		run_dic['config']['initial start'] = int(commands.getstatusoutput('%s/lalapps_tconvert now'%bindir)[1]) - 500

#Launch oLIB
run_2ndpipe_beta.executable(run_dic=run_dic)
