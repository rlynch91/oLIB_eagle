#!/usr/bin/python

import sys
sys.path.insert(1,'/home/ryan.lynch/numpy/numpy-1.8.2-INSTALL/lib64/python2.7/site-packages')
import commands

#Get full gps time
gps_time_full = int(commands.getstatusoutput('%s/lalapps_tconvert now'%run_dic['config']['LIB bin dir'])[1])

#Convert full gps time into the current gps day
gps_day_now = int(float(gps_time_full)/100000.)

#Collect results from the current gps day
???

#Get previous gps day
gps_day_last = float(np.genfromtxt(???))

#Get threshold for background collection and retraining
gps_threshold = gps_day_last * 100000. + 50000.

#If past the threshold, collect background and retrain
if gps_time_full > gps_threshold:
	#Run background collection
	???
	#Run retraining
	???
	#Save current gps day as completed
	???
