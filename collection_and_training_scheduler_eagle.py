#!/usr/bin/python

import sys
sys.path.insert(1,'/home/ryan.lynch/numpy/numpy-1.8.2-INSTALL/lib64/python2.7/site-packages')
import numpy as np
import pickle
import commands
import os
import GPS_day_collect_eagle

########################################################################
if __name__=='__main__':
	#Parse user options
	from optparse import OptionParser

	usage = None
	parser = OptionParser(usage=usage)

	parser.add_option("-g", "--gps-day-collect", default=None, type="string", help="GPS day to collect, or current day if not given or 'None'")
	parser.add_option("-r", "--run-dic", default=None, type="string", help="Path to run_dic (containing all info about the runs)")
	
	parser.add_option("", "--ifo-groups", default=None, type="string", help="Comma-separated list of ifo groups to collect for (e.g., H1L1,H1L1V1,...)")
	parser.add_option("", "--infodir", default=None, type="string", help="Directory where the oLIB pipeline code lives")
	parser.add_option("", "--rundir", default=None, type="string", help="Run directory to collect results from")
	parser.add_option("", "--collectdir", default=None, type="string", help="Directory in which collected results will be written")
	parser.add_option("", "--backdir", default=None, type="string", help="Directory in which background results are stored")
	parser.add_option("", "--retraindir", default=None, type="string", help="Directory in which retraining results are stored")
	parser.add_option("", "--last-gps-day-path", default=None, type="string", help="Path to file containing the last GPS day that had collection and retraining successfully completed")
	parser.add_option("", "--bindir", default=None, type="string", help="Bin directory containing the lalsuites installation to be used")
	parser.add_option("", "--max-back-size", default=None, type="int", help="Maximum number of events that can be stored in background dictionary")
	parser.add_option("", "--max-signal-size", default=None, type="int", help="Maximum number of events that can be stored in signal training dictionary")
	parser.add_option("", "--max-noise-size", default=None, type="int", help="Maximum number of events that can be stored in noise training dictionary")
	parser.add_option("", "--train-details-dic", default=None, type="string", help="Path to dictionary containing specific details about the retraining")
	parser.add_option("", "--train-bin", default=None, type="string", help="Search bin to complete retraining for")

	#-------------------------------------------------------------------

	opts, args = parser.parse_args()

	gps_day_collect = opts.gps_day_collect
	run_dic = pickle.load(open(opts.run_dic))
	
	#-------------------------------------------------------------------
	
	#initialize the variables we need
	ifo_groups = run_dic['coincidence'].keys()
	infodir = run_dic['config']['info dir']
	rundir = run_dic['config']['run dir']
	collectdir = run_dic['collection and retraining']['collect dir']
	bindir = run_dic['config']['LIB bin dir']
	max_back_size = run_dic['collection and retraining']['max back size']
	max_signal_size = run_dic['collection and retraining']['max sig train size']
	max_noise_size = run_dic['collection and retraining']['max noise train size']
	
	#???
?	#Get background and retraining directories for this search bin
?	backdir = run_dic['collection and retraining']['low_f']['back dir']
?	retraindir = run_dic['collection and retraining']['low_f']['retrain dir']
	#???
	
	#-------------------------------------------------------------------
		
	#Get current full gps time
	gps_time_full = int(commands.getstatusoutput('%s/lalapps_tconvert now'%bindir)[1])

	#Convert current full gps time into the current gps day
	if not gps_day_collect or gps_day_collect == 'None':
		gps_day_collect = int(float(gps_time_full)/100000.)
	else:
		gps_day_collect = int(gps_day_collect)
#???
?	#Collect results from the current gps day
?	for mode in ['0lag','back','noise_train','sig_train']:  #get rid of mode, deal with that in other script
?		GPS_day_collect_eagle.executable(gps_day=gps_day_collect, mode=mode, ifo_groups=ifo_groups, rundir=rundir, outdir=collectdir)

	#Get previous gps day that background collection and retraining was successfully completed for
	if os.path.isfile(last_gps_day_path):
		gps_day_last = pickle.load(open(last_gps_day_path))
	else:
		gps_day_last = {}
		gps_day_last['background'] = {}
		gps_day_last['retraining'] = {}
		for group in ifo_groups:
			gps_day_last['background'][group] = None
			gps_day_last['retraining'][group] = None
			#???retraining needs subgroup for each search bin
			
	#Open comments file to log the results of the background update and retraining 
	run_comments_file = open('%s_run_comments.txt_new'%last_gps_day_path,'wt')

	#Loop over background and retraining ifo groups
	for key in gps_day_last:
		for group in ifo_groups:
			#Get next day and time threshold (1 day lag) for background collection and retraining
			if gps_day_last[key][group]:
				gps_day_retrain = int(gps_day_last[key][group]) + 1
			else:
				gps_day_retrain = gps_day_collect
			gps_threshold = (gps_day_retrain + 2) * 100000.
			
			#If past the threshold, collect background and retrain on (depending on key)
			if gps_time_full > gps_threshold:
				
				if key == 'background':
					#Run background collection
					background_string = 'python %s/update_background_eagle.py --new-back-dic %s --new-back-lt %s '%(infodir,'%s/%s/%s/%s_%s_%s_results.pkl'%(collectdir,'back',group,gps_day_retrain,'back',group), '%s/%s/%s/%s_%s_%s_livetime.txt'%(collectdir,'back',group,gps_day_retrain,'back',group))
					background_string += '--old-back-dic %s --old-back-lt %s '%('%s/%s/collected_background_dictionary.pkl'%(backdir,group), '%s/%s/collected_background_livetime.txt'%(backdir,group))
					background_string += '--outdir %s --max-back-size %s --new-gps-day %s'%('%s/%s/'%(backdir,group),max_back_size,gps_day_retrain)
					back_status = commands.getstatusoutput(background_string)
					run_comments_file.write('%s %s %s %s \n\n'%(key, group, back_status[0], back_status[1]))  #??? also print search bin/back
					if not back_status[0]:
						gps_day_last[key][group] = int(gps_day_retrain)
						print key, group, "Success"
					else:
						print key, group, "Failure", back_status[1]
					
				elif key == 'retraining':
					#Run retraining
					retraining_string = 'python %s/retrain_likelihoods_eagle.py --new-sig-dic %s --new-noise-dic %s '%(infodir,'%s/%s/%s/%s_%s_%s_results.pkl'%(collectdir,'sig_train',group,gps_day_retrain,'sig_train',group), '%s/%s/%s/%s_%s_%s_results.pkl'%(collectdir,'noise_train',group,gps_day_retrain,'noise_train',group))
					retraining_string += '--old-sig-dic %s --old-noise-dic %s '%('%s/%s/Signal_training_dictionary.pkl'%(retraindir,group), '%s/%s/Noise_training_dictionary.pkl'%(retraindir,group))
					retraining_string += '--old-sig-bands %s --old-noise-bands %s '%('%s/%s/%s_Signal_log_KDE_bandwidths.npy'%(retraindir,group,train_details_dic['param info'][train_bin].keys()[0]),'%s/%s/%s_Noise_log_KDE_bandwidths.npy'%(retraindir,group,train_details_dic['param info'][train_bin].keys()[0]))
					retraining_string += '--outdir %s --max-signal-size %s --max-noise-size %s '%('%s/%s/'%(retraindir,group),max_signal_size,max_noise_size)
					retraining_string += '--train-details-dic %s --search-bin %s'%(opts.train_details_dic,train_bin)
					retraining_status = commands.getstatusoutput(retraining_string)
					run_comments_file.write('%s %s %s %s \n\n'%(key, group, retraining_status[0], retraining_status[1]))
					if not retraining_status[0]:
						gps_day_last[key][group] = int(gps_day_retrain)
						print key, group, "Success"
					else:
						print key, group, "Failure", retraining_status[1]
				
	#Save updated dictionary containing last completed days for background collection and retraining
	pickle.dump(gps_day_last,open(last_gps_day_path,'wt'))
	run_comments_file.close()
	if os.path.getsize('%s_run_comments.txt_new'%last_gps_day_path) > 0:
		os.system('mv %s_run_comments.txt_new %s_run_comments.txt'%(last_gps_day_path,last_gps_day_path))
	else:
		os.system('rm %s_run_comments.txt_new'%(last_gps_day_path))
