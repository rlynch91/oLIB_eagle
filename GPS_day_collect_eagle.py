#!/usr/bin/python

import sys
sys.path.insert(1,'/home/ryan.lynch/numpy/numpy-1.8.2-INSTALL/lib64/python2.7/site-packages')
import numpy as np
import pickle
import os

###
def executable(run_dic,gps_day):
	"""
	"""
	#Initialize the variables we need
	rundir = run_dic['config']['run dir']
	outdir = run_dic['collection and retraining']['collect dir']
	
	for mode,check_mode in [('0lag','analyze 0lag'),('back','analyze back'),('noise_train','analyze noise training'),('sig_train','analyze signal training')]:
		#Get the ifo groups we need to collect for this mode
		ifo_groups = []
		for group in run_dic['coincidence']:
			if run_dic['coincidence'][group][check_mode]:
				ifo_groups += [group]
			
		#Open folders for writing summary files
		summary_files = {}
		for group in ifo_groups:
			if not os.path.exists('%s/%s/%s/'%(outdir,mode,group)):
				os.makedirs('%s/%s/%s/'%(outdir,mode,group))
			summary_files[group] = open('%s/%s/%s/%s_%s_%s_summary.txt'%(outdir,mode,group,gps_day,mode,group),'wt')
		
		#Initialize collection dictionary
		total_lts = {}
		dictionary = {}
		events = {}
		for group in ifo_groups:
			total_lts[group] = 0.
			dictionary[group] = {}
			events[group] = 0
		
		#Loop through all files in gps_day folder in reverse chronological order (so that most recent triggers have lowest index)
		files = os.listdir('%s/%s/'%(rundir,gps_day))
		start_times = [float(f.split('_')[1]) for f in files]
		files_sorted = sorted(zip(start_times,files), key = lambda x:x[0])[::-1]
		for time,f in files_sorted:
			#Check to see if livetime was analyzed
			time_flags = {}
			tmp_lts = {}
			for group in ifo_groups:
				time_flags[group] = False
				tmp_lts[group] = np.nan

				if (mode == '0lag') or (mode == 'sig_train'):
					if os.path.isfile('%s/%s/%s/livetime/%s/%s/livetime_0lag_%s.txt'%(rundir,gps_day,f,group,mode,group)):
						time_flags[group] = True
						tmp_lts[group] = float(np.genfromtxt('%s/%s/%s/livetime/%s/%s/livetime_0lag_%s.txt'%(rundir,gps_day,f,group,mode,group)))
						total_lts[group] += tmp_lts[group]
				elif (mode == 'back') or (mode == 'noise_train'):
					if os.path.isfile('%s/%s/%s/livetime/%s/%s/livetime_timeslides_%s.txt'%(rundir,gps_day,f,group,mode,group)):
						time_flags[group] = True
						tmp_lts[group] = float(np.genfromtxt('%s/%s/%s/livetime/%s/%s/livetime_timeslides_%s.txt'%(rundir,gps_day,f,group,mode,group)))
						total_lts[group] += tmp_lts[group]
			
			#Check to see if the dag failed
			fail_flag = False
			dag_missing_flag = False
			still_running_flag = False
			if os.path.exists('%s/%s/%s/dag/'%(rundir,gps_day,f)):
				for dag_file in os.listdir('%s/%s/%s/dag/'%(rundir,gps_day,f)):
					if dag_file.split('.')[-1][:6] == 'rescue':
						fail_flag = True
					if dag_file.split('.')[-1] == 'lock':
						still_running_flag = True
						
			else:
				dag_missing_flag = True	
			
			#Check to see if there is a results_dic ready to be collected for each group, and if so collect it and mark that it has been collected
			for group in ifo_groups:
				collected_flag = False
				no_results_flag = False
				if os.path.isfile('%s/%s/%s/results_dic/%s/%s/LIB_trigs_results_%s_%s.pkl'%(rundir,gps_day,f,group,mode,group,mode)) and os.path.isfile('%s/%s/%s/results_dic/%s/%s/results_dic_ready_for_collection.txt'%(rundir,gps_day,f,group,mode)):
					tmp_dic = pickle.load(open('%s/%s/%s/results_dic/%s/%s/LIB_trigs_results_%s_%s.pkl'%(rundir,gps_day,f,group,mode,group,mode)))
					for key in tmp_dic:
						dictionary[group][events[group]] = tmp_dic[key]
						events[group] += 1
					os.system('> %s/%s/%s/results_dic/%s/%s/results_dic_has_been_collected.txt'%(rundir,gps_day,f,group,mode))
					collected_flag = True
				else:
					no_results_flag = True
			
				#Write status to summary files for each group
				if still_running_flag:
					summary_files[group].write('%s\t%s\t%s\n'%(f,tmp_lts[group],'Dag still running (locked)'))			
				elif fail_flag:
					summary_files[group].write('%s\t%s\t%s\n'%(f,tmp_lts[group],'Dag failed'))
				elif dag_missing_flag:
					summary_files[group].write('%s\t%s\t%s\n'%(f,tmp_lts[group],'Dag not created'))			
				elif no_results_flag:
					summary_files[group].write('%s\t%s\t%s\n'%(f,tmp_lts[group],'No results to collect'))
				elif collected_flag:
					summary_files[group].write('%s\t%s\t%s\n'%(f,tmp_lts[group],'Succesfully collected results'))
				else:
					summary_files[group].write('%s\t%s\t%s\n'%(f,tmp_lts[group],'Unknown'))
			
		#Close summary files
		for group in ifo_groups:
			summary_files[group].close()
			
		#Save dictionaries and livetimes
		for group in ifo_groups:
			pickle.dump(dictionary[group], open('%s/%s/%s/%s_%s_%s_results.pkl'%(outdir,mode,group,gps_day,mode,group),'wt'))
			np.savetxt('%s/%s/%s/%s_%s_%s_livetime.txt'%(outdir,mode,group,gps_day,mode,group),np.array([total_lts[group]]))
			
##############################################
if __name__=='__main__':
	from optparse import OptionParser

	usage = None
	parser = OptionParser(usage=usage)

	parser.add_option("-r", "--run-dic", default=None, type="string", help="Path to run_dic (containing all info about the runs)")
	parser.add_option("-g", "--gps-day", default=None, type='int', help="GPS day, in 100000s of seconds, for which to collect")

	#---------------------------------------------

	opts, args = parser.parse_args()

	run_dic = pickle.load(open(opts.run_dic))
	gps_day = opts.gps_day
	
	#---------------------------------------------
	
	executable(run_dic=run_dic, gps_day=gps_day)
