#!/usr/bin/python

import numpy as np
import time
import os
import commands
import pickle
import framecache2segs_eagle
import inject_signal_training_eagle
import write_omicron_2_LIB_dag_eagle

#=======================================================================

###
def run_inject_signal_training(run_dic):
	"""
	"""
	if not os.path.exists("%s/training_injections"%run_dic['seg dir']):
		os.makedirs("%s/training_injections"%run_dic['seg dir'])
	inject_signal_training_eagle.executable(run_dic=run_dic)
	
	for ifo in run_dic['ifos']['names']:
		if run_dic['data']['success flags'][ifo]:
			run_dic['data']['signal train cache files'][ifo] = "%s/framecache/MDC_DatInjMerge_%s_%s_%s.lcf"%(run_dic['seg dir'],ifo,run_dic['times']['start'],run_dic['times']['stop'])
	print "Injected event for signal training"
	
###
def run_write_and_submit_dag(run_dic):
	"""
	"""
	#write pipeline dag and runfolders
	write_omicron_2_LIB_dag_eagle.executable(run_dic=run_dic) 

	#launch pipeline dag if not all data labeled to be skipped
	if np.any([not run_dic['data']['skip flags'][ifo_test] for ifo_test in run_dic['ifos']['names']]):
		os.system("condor_submit_dag %s/dag/2ndPipeDag_%s_%s_%s.dag"%(run_dic['seg dir'],"".join(run_dic['ifos']['names']),run_dic['times']['actual start'],run_dic['config']['stride']-run_dic['config']['overlap']))
		print "Submitted dag"
	else:
		print "All data labeled to be skipped, not submitting to condor"

###
def initialize_segment(run_dic):
	"""
	"""
	#make rundir for segment
	segdir = "%s/%s/%s_%s_%s"%(run_dic['config']['run dir'],int(run_dic['times']['actual start']/100000.),"".join(run_dic['ifos']['names']), run_dic['times']['actual start'], run_dic['config']['stride']-run_dic['config']['overlap'])
	if not os.path.exists(segdir):
		os.makedirs(segdir)
	run_dic['seg dir'] = segdir

	#initialize dics holding data info for each ifo
	run_dic['data'] = {}
	run_dic['data']['frame files'] = {}
	run_dic['data']['frame times'] = {}
	run_dic['data']['frame lengths'] = {}
	run_dic['data']['seg files'] = {}
	run_dic['data']['cache files'] = {}
	run_dic['data']['signal train cache files'] = {}
	for ifo in run_dic['ifos']['names']:
		run_dic['data']['frame files'][ifo] = [np.nan]
		run_dic['data']['frame times'][ifo] = [np.nan]
		run_dic['data']['frame lengths'][ifo] = [np.nan]
		run_dic['data']['seg files'][ifo] = None
		run_dic['data']['cache files'][ifo] = None
		run_dic['data']['signal train cache files'][ifo] = None

	#initialize flags for each ifo
	run_dic['data']['success flags'] = {}
	run_dic['data']['skip flags'] = {}
	run_dic['data']['inj flags'] = {}
	for ifo in run_dic['ifos']['names']:
		run_dic['data']['success flags'][ifo] = False
		run_dic['data']['skip flags'][ifo] = False
		run_dic['data']['inj flags'][ifo] = False

###
def executable(run_dic):
	"""
	"""
	if run_dic['run mode']['line'] == 'Online':
		
		#initialize the variables we need 
		ifos = run_dic['ifos']['names']
		rundir = run_dic['config']['run dir']
		infodir = run_dic['config']['info dir']
		bindir = run_dic['config']['LIB bin dir']
		initial_start = run_dic['config']['initial start']
		stride = run_dic['config']['stride']
		overlap = run_dic['config']['overlap']		
		wait = run_dic['config']['wait']
		max_wait = run_dic['config']['max wait']
		bitmask = run_dic['config']['bitmask']
		inj_runmode = run_dic['run mode']['inj runmode']
		train_runmode = run_dic['run mode']['train runmode']
		
		channel_types = {}
		state_channels = {}
		for ifo in ifos:
			channel_types[ifo] = run_dic['ifos'][ifo]['channel type']
			state_channels[ifo] = run_dic['ifos'][ifo]['state channel name']

		#############################################

		#initialize start time and stop times for first segment
		np.savetxt(rundir+'/current_start.txt', np.array([initial_start]))
		
		actual_start = initial_start
		start = actual_start - int(0.5*overlap)
		stop = start + stride
		running_wait = 0
		
		run_dic['times'] = {}
		run_dic['times']['actual start'] = initial_start
		run_dic['times']['start'] = start
		run_dic['times']['stop'] = stop

		#Initialize this segment
		initialize_segment(run_dic=run_dic)

		#start a while loop
		while True:
			#wait for designated amount of time
			time.sleep(wait)
			running_wait += wait
			
			#run loop for each ifo
			for i_ifo, ifo in enumerate(ifos):
				#do some checks to see if we filled time (with frames) between start and stop for each ifo
				check_before_start = False
				check_after_stop = False
					
				if run_dic['data']['frame times'][ifo][0] <= start:
					check_before_start = True
				if (run_dic['data']['frame times'][ifo][-1] + run_dic['data']['frame lengths'][ifo][-1]) >= stop:
					check_after_stop = True
						
				#if we haven't reached stop time yet, fetch frames again
				if not check_after_stop:
					print "haven't reached stop time, fetching frames for", ifo, start, stop
					run_dic['data']['frame files'][ifo] = commands.getstatusoutput("%s/gw_data_find --server=datafind.ldas.cit:80 --observatory=%s --url-type=file --type=%s --gps-start-time=%s --gps-end-time=%s"%(bindir, ifo.strip("1"), channel_types[ifo], start, stop))[1].split("\n")
					if run_dic['data']['frame files'][ifo] == [""]:
						print "no frames found for ifo", ifo, start, stop
						run_dic['data']['frame times'][ifo] = [np.nan]
						run_dic['data']['frame lengths'][ifo] = [np.nan]
					else:
						print "frames found for ifo", ifo, start, stop
						run_dic['data']['frame times'][ifo] = [int(f.split(channel_types[ifo]+'-')[-1].split('-')[0]) for f in run_dic['data']['frame files'][ifo]]
						run_dic['data']['frame lengths'][ifo] = [int(f.split(channel_types[ifo]+'-')[-1].split('-')[-1].split('.')[0]) for f in run_dic['data']['frame files'][ifo]]
						print run_dic['data']['frame times'][ifo]
						
				#here we have passed the stop time, if we still have the start time frame then we can prepare to launch the condor jobs for that ifo
				elif check_before_start:
					print "filled time for ifo", ifo, start, stop
					#check if ifo has already been flagged as ready for condor submission
					if not run_dic['data']['success flags'][ifo]:
						#create necessary framecache for each ifo
						if not os.path.exists("%s/framecache"%segdir):
							os.makedirs("%s/framecache"%segdir)
						run_dic['data']['cache files'][ifo] = "%s/framecache/%s_%s_%s.cache"%(segdir,ifo,start,stop)
						cache_file = open(run_dic['data']['cache files'][ifo],'wt')
						for i in xrange(len(run_dic['data']['frame files'][ifo])):
							cache_file.write("%s %s %s %s %s\n"%(ifo.strip("1"), channel_types[ifo], run_dic['data']['frame times'][ifo][i], run_dic['data']['frame lengths'][ifo][i], run_dic['data']['frame files'][ifo][i]))
						cache_file.close()

						#write segment file for ifo
						if not os.path.exists("%s/segments"%segdir):
							os.makedirs("%s/segments"%segdir)
						run_dic['data']['inj flags'][ifo] = framecache2segs_eagle.executable(ifo=ifo, run_dic=run_dic) 
						run_dic['data']['seg files'][ifo] = "%s/segments/%s_%s_%s.seg"%(segdir,ifo,start,stop)
						
						#check if segment file is empty
						if os.path.getsize(run_dic['data']['seg files'][ifo]) == 0:
							run_dic['data']['skip flags'][ifo] = True
								
						#check if inj_flag corresponds to inj_runmode
						if (run_dic['data']['inj flags'][ifo] == 'True' and inj_runmode == 'NonInj') or (run_dic['data']['inj flags'][ifo] == 'False' and inj_runmode == 'Inj'):
							run_dic['data']['skip flags'][ifo] = True
						
						#flag that ifo is ready for condor submission (if not intended to be skipped)
						if run_dic['data']['skip flags'][ifo] = False:
							run_dic['data']['success flags'][ifo] = True

					#check to see if all ifos have been flagged as ready for condor submission
					if np.prod([ (run_dic['data']['success flags'][ifo_test] or run_dic['data']['skip flags'][ifo_test]) for ifo_test in ifos]):
						#if in signal training mode, inject signals and point to new cache files
						if train_runmode == "Train":
							run_inject_signal_training(run_dic=run_dic)
														
						#write pipeline dag and submit to condor
						run_write_and_submit_dag(run_dic=run_dic)
						
						#save run_dic
						if not os.path.exists("%s/run_dic"%segdir):
							os.makedirs("%s/run_dic"%segdir)
						pickle.dump(run_dic,open('%s/run_dic/run_dic_%s_%s.pkl'%(segdir,start,stop),'wt'))
																				
						#move on to next time segment
						start += (stride - overlap)
						stop = start + stride
						actual_start = start + int(0.5*overlap)
						np.savetxt(rundir+'/current_start.txt', np.array([actual_start]))
						running_wait = 0
						
						run_dic['times']['actual start'] = actual_start
						run_dic['times']['start'] = start
						run_dic['times']['stop'] = stop
						
						initialize_segment(run_dic=run_dic)
					
				#here we have passed stop time, if we don't still have the start time frame then we will skip this segment
				else:
					print "lost start time for ifo", ifo, start, stop
					
					#if not already done, set skip flag to true
					if not run_dic['data']['skip flags'][ifo]:
						run_dic['data']['skip flags'][ifo] = True
					
					#check to see if all ifos have been flagged as ready for condor submission
					if np.prod([ (run_dic['data']['success flags'][ifo_test] or run_dic['data']['skip flags'][ifo_test]) for ifo_test in ifos]):					
						#if in signal training mode, inject signals and point to new cache files
						if train_runmode == "Train":
							run_inject_signal_training(run_dic=run_dic)
														
						#write pipeline dag and submit to condor
						run_write_and_submit_dag(run_dic=run_dic)
						
						#save run_dic
						if not os.path.exists("%s/run_dic"%segdir):
							os.makedirs("%s/run_dic"%segdir)
						pickle.dump(run_dic,open('%s/run_dic/run_dic_%s_%s.pkl'%(segdir,start,stop),'wt'))
						
						#move on to next time interval
						start += (stride - overlap)
						stop = start + stride
						actual_start = start + int(0.5*overlap)
						np.savetxt(rundir+'/current_start.txt', np.array([actual_start]))
						running_wait = 0
						
						run_dic['times']['actual start'] = actual_start
						run_dic['times']['start'] = start
						run_dic['times']['stop'] = stop
						
						initialize_segment(run_dic=run_dic)
				
				#Check to see if we have exceeded the maximum wait
				if running_wait > max_wait:
					print "exceeded maximum wait time for", start, stop

					#set skip flags to true for non-success ifos
					for ifo_test in ifos:
						if not run_dic['data']['success flags'][ifo_test]:
							run_dic['data']['skip flags'][ifo_test] = True
					
					#if in signal training mode, inject signals and point to new cache files
					if train_runmode == "Train":
						run_inject_signal_training(run_dic=run_dic)
													
					#write pipeline dag and submit to condor
					run_write_and_submit_dag(run_dic=run_dic)
					
					#save run_dic
					if not os.path.exists("%s/run_dic"%segdir):
						os.makedirs("%s/run_dic"%segdir)
					pickle.dump(run_dic,open('%s/run_dic/run_dic_%s_%s.pkl'%(segdir,start,stop),'wt'))
					
					#catch up to real time
					actual_start = int(commands.getstatusoutput('%s/lalapps_tconvert now'%bindir)[1])
					np.savetxt(rundir+'/current_start.txt', np.array([actual_start]))
					start = actual_start - int(0.5*overlap)
					stop = start + stride
					running_wait = 0
					
					run_dic['times']['actual start'] = actual_start
					run_dic['times']['start'] = start
					run_dic['times']['stop'] = stop
					
					initialize_segment(run_dic=run_dic)
					
	elif run_dic['run mode'['line'] == 'Offline':
		pass