#!/usr/bin/python

import numpy as np
import pickle
import sys
sys.path.insert(1,'/home/ryan.lynch/numpy/numpy-1.8.2-INSTALL/lib64/python2.7/site-packages')
import commands
import GPS_day_collect_eagle

########################################################################
if __name__=='__main__':
	#Parse user options
	from optparse import OptionParser

	usage = None
	parser = OptionParser(usage=usage)

	parser.add_option("", "--ifo-groups", default=None, type="string", help="Comma-separated list of ifo groups to collect for (e.g., H1L1,H1L1V1,...)")
	parser.add_option("", "--rundir", default=None, type="string", help="Run directory to collect results from")
	parser.add_option("", "--collectdir", default=None, type="string", help="Directory in which collect results will be written")
	parser.add_option("", "--backdir", default=None, type="string", help="Directory in which background results are stored")
	parser.add_option("", "--retraindir", default=None, type="string", help="Directory in which retraining results are stored")
	parser.add_option("", "--last-gps-day-path", default=None, type="string", help="Path to file containing the last GPS day that had collection and retraining successfully completed")
	parser.add_option("", "--bindir", default=None, type="string", help="Bin directory containing the lalsuites installation to be used")
	parser.add_option("", "--max-bin-size", default=None, type="int", help="Maximum number of events that can be stored in background dictionary")
	parser.add_option("", "--max-signal-size", default=None, type="int", help="Maximum number of events that can be stored in signal training dictionary")
	parser.add_option("", "--max-noise-size", default=None, type="int", help="Maximum number of events that can be stored in noise training dictionary")
	parser.add_option("", "--train-details-dic", default=None, type="string", help="Path to dictionary containing specific details about the retraining")
	parser.add_option("", "--train-bin", default=None, type="string", help="Search bin to complete retraining for")

	#-------------------------------------------------------------------

	opts, args = parser.parse_args()

	ifo_groups = opts.ifo_groups
	rundir = opts.rundir
	collectdir = opts.collectdir
	backdir = opts.backdir
	retraindir = opts.retraindir
	last_gps_day_path = opts.last_gps_day_path
	bindir = opts.bindir
	max_back_size = opts.max_back_size
	max_signal_size = opts.max_signal_size
	max_noise_size = opts.max_noise_size
	train_details_dic = pickle.load(open(opts.train_details_dic))
	train_bin = opts.train_bin
	
	#-------------------------------------------------------------------

	#Get full gps time
	gps_time_full = int(commands.getstatusoutput('%s/lalapps_tconvert now'%bindir)[1])

	#Convert full gps time into the current gps day
	gps_day_now = int(float(gps_time_full)/100000.)

	#Collect results from the current gps day
	for mode in ['0lag','back','noise_train','sig_train']:
		GPS_day_collect_eagle.executable(gps_day=gps_day_now, mode=mode, ifo_groups=ifo_groups, rundir=rundir, outdir=collectdir)

	#Get previous gps day that background collection and retraining was successfully completed for
	gps_day_last = float(np.genfromtxt(last_gps_day_path))

	#Get next day and time threshold (1 day lag) for background collection and retraining
	gps_day_retrain = gps_day_last + 1
	gps_threshold = (gps_day_retrain + 2) * 100000.

	#If past the threshold, collect background and retrain on 
	if gps_time_full > gps_threshold:
		for group in ifo_groups:
			#Run background collection
			background_string = 'update_background_eagle.py --new-back-dic %s --new-back-lt %s '%('%s/%s/%s/%s_%s_%s_results.pkl'%(collectdir,'back',group,gps_day_retrain,'back',group), '%s/%s/%s/%s_%s_%s_livetime.txt'%(collectdir,'back',group,gps_day_retrain,'back',group))
			background_string += '--old-back-dic %s --old-back-lt %s '%('%s/%s/collected_background_dictionary.pkl'%(backdir,group), '%s/%s/collected_background_livetime.txt'%(backdir,group))
			background_string += '--outdir %s --max-back-size %s --new-gps-day %s'%('%s/%s/'%(backdir,group),max_back_size,gps_day_retrain)
			os.system(background_string)
			
			#Run retraining
			retraining_string = 'retrain_likelihoods_eagle.py --new-sig-dic %s --new-noise-dic %s '%('%s/%s/%s/%s_%s_%s_results.pkl'%(collectdir,'sig_train',group,gps_day_retrain,'sig_train',group), '%s/%s/%s/%s_%s_%s_results.pkl'%(collectdir,'noise_train',group,gps_day_retrain,'noise_train',group))
			retraining_string = '--old-sig-dic %s --old-noise-dic %s '%('%s/%s/Signal_training_dictionary.pkl'%(retraindir,group), '%s/%s/Noise_training_dictionary.pkl'%(retraindir,group))
			retraining_string = '--old-sig-bands %s --old-noise-bands %s '%('%s/%s/%s_Signal_log_KDE_bandwidths_old.npy'%(retraindir,group,train_details_dic['param info'][train_bin].keys()[0]),'%s/%s/%s_Noise_log_KDE_bandwidths_old.npy'%(retraindir,group,train_details_dic['param info'][train_bin].keys()[0]))
			retraining_string = '--outdir %s --max-signal-size %s --max-noise-size %s '%('%s/%s/'%(retraindir,group),max_signal_size,max_noise_size)
			retraining_string = '--train-details-dic %s --search-bin %s'%(opts.train_details_dic,train_bin)
			os.system(retraining_string)
			
			#Save current gps day as completed
			np.savetxt(last_gps_day_path,np.array([gps_day_retrain]))
