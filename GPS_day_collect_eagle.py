#!/usr/bin/python

import numpy as np
import pickle
import os

###
def executable(gps_day, mode, ifo_groups, rundir, outdir):
	"""
	"""
	#Open folders for writing summary files
	summary_files = {}
	for group in ifo_groups:
		if not os.path.exists('%s/%s/%s/'%(outdir,mode,group)):
			os.makedirs('%s/%s/%s/'%(outdir,mode,group))
		summary_files[ifo_group] = open('%s/%s/%s/%s_%s_%s_summary.txt'%(outdir,mode,group,gps_day,mode,group),'wt')
	
	#Initialize collection dictionary
	dictionary = {}
	events = {}
	for group in ifo_groups:
		dictionary[group] = {}
		events[group] = 0
	
	#Loop through all files in gps_day folder in reverse chronological order (so that most recent triggers have lowest index)
	files = os.listdir('%s/%s/'%(rundir,gps_day))[::-1]
	start_times = [float(f.split('_')[1]) for f in files]
	files_sorted = sorted(zip(start_times,files), key = lambda x:x[0])
	for time,f in files_sorted:
		#Check to see if the dag failed
		???
		
		#Check to see if there is a results_dic ready to be collected for each group, and if so collect it and mark that it has been collected
		collected_flags = {}
		for group in ifo_groups:
			collected_flags[group] = False
			if os.path.isfile('%s/%s/%s/results_dic/%s/%s/LIB_trigs_results_%s_%s.pkl'%(rundir,gps_day,f,group,mode,group,mode)) and os.path.isfile('%s/%s/%s/results_dic/%s/%s/results_dic_ready_for_collection.txt'%(rundir,gps_day,f,group,mode)):
				tmp_dic = pickle.load(open('%s/%s/%s/results_dic/%s/%s/LIB_trigs_results_%s_%s.pkl'%(rundir,gps_day,f,group,mode,group,mode)))
				for key in tmp_dic:
					dictionary[group][events[group]] = tmp_dic[key]
					events[group] += 1
				os.system('> %s/%s/%s/results_dic/%s/%s/results_dic_has_been_collected.txt'%(rundir,gps_day,f,group,mode))
				collected_flags[group] = True
		
		#Write status to summary files for each group
		???
		
	#Close summary files
	for group in ifo_groups:
		summary_files[ifo_group].close()
		
	#Save dictionaries
	for group in ifo_groups:
		pickle.dump(dictionary[group], '%s/%s/%s/%s_%s_%s_results.pkl'%(outdir,mode,group,gps_day,mode,group)
		
