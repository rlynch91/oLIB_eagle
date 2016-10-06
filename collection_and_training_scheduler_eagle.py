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

	parser.add_option("-r", "--run-dic", default=None, type="string", help="Path to run_dic (containing all info about the runs)")
	parser.add_option("-g", "--gps-day-collect", default=None, type="string", help="GPS day to collect, or current day if not given or 'None'")
	
	#-------------------------------------------------------------------

	opts, args = parser.parse_args()

	run_dic = pickle.load(open(opts.run_dic))
	gps_day_collect = opts.gps_day_collect
	
	#-------------------------------------------------------------------
	
	#initialize the variables we need
	ifo_groups = run_dic['coincidence'].keys()
	infodir = run_dic['config']['info dir']
	rundir = run_dic['config']['run dir']
	bindir = run_dic['config']['LIB bin dir']
	
	last_gps_day_path = rundir + '/last_gps_day_collected_and_trained.pkl'
	last_gps_day_comments_path = rundir + '/last_gps_day_collected_and_trained_comments.txt'
		
	#-------------------------------------------------------------------
		
	#Get current full gps time
	gps_time_full = int(commands.getstatusoutput('%s/lalapps_tconvert now'%bindir)[1])

	#Convert current full gps time into the current gps day
	if not gps_day_collect or gps_day_collect == 'None':
		gps_day_collect = int(float(gps_time_full)/100000.)
	else:
		gps_day_collect = int(gps_day_collect)

	#Collect results from the current gps day
	GPS_day_collect_eagle.executable(run_dic=run_dic,gps_day=gps_day_collect)
	
	#Get previous gps day that background collection and retraining was successfully completed for
	if os.path.isfile(last_gps_day_path):
		gps_day_last = pickle.load(open(last_gps_day_path))
	else:
		gps_day_last = {}
		gps_day_last['background'] = {}
		gps_day_last['retraining'] = {}
		for group in ifo_groups:
			gps_day_last['background'][group] = None
			gps_day_last['retraining'][group] = {}
			for search_bin in run_dic['search bins']['bin names']:
				gps_day_last['retraining'][group][search_bin] = None
			
	#Open comments file to log the results of the background update and retraining 
	run_comments_file = open('%s_new'%last_gps_day_comments_path,'wt')

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
					background_string = 'python %s/update_background_eagle.py --run-dic %s --new-gps-day %s --ifo-group %s'%(infodir,opts.run_dic,gps_day_retrain,group)
					back_status = commands.getstatusoutput(background_string)
					run_comments_file.write('%s %s %s %s %s \n\n'%(key, 'back', group, back_status[0], back_status[1]))
					if not back_status[0]:
						gps_day_last[key][group] = int(gps_day_retrain)
						print key, 'back', group, "Success"
					else:
						print key, 'back', group, "Failure", back_status[1]
#???					
				elif key == 'retraining':
					#Loop over search bins
					for search_bin in run_dic['search bins']['bin names']:
						#Run retraining
						retraining_string = 'python %s/retrain_likelihoods_eagle.py --run-dic %s --new-gps-day %s --ifo-group %s --search-bin %s'%(infodir,opts.run_dic,gps_day_retrain,group,search_bin)
						retraining_status = commands.getstatusoutput(retraining_string)
						run_comments_file.write('%s %s %s %s \n\n'%(key, search_bin, group, retraining_status[0], retraining_status[1]))
						if not retraining_status[0]:
							gps_day_last[key][group] = int(gps_day_retrain)
							print key, search_bin, group, "Success"
						else:
							print key, search_bin, group, "Failure", retraining_status[1]
#???

	#???ADD IN FUNCTION THAT DOES TARRING IF WE ARE COMPLETELY DONE WITH A DAY????
				
	#Save updated dictionary containing last completed days for background collection and retraining
	pickle.dump(gps_day_last,open(last_gps_day_path,'wt'))
	run_comments_file.close()
	if os.path.getsize(last_gps_day_comments_path) > 0:
		os.system('mv %s_new %s'%(last_gps_day_comments_path,last_gps_day_comments_path))
	else:
		os.system('rm %s_new'%(last_gps_day_comments_path))
