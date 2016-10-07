#!/usr/bin/python

import sys
sys.path.insert(1,'/home/ryan.lynch/numpy/numpy-1.8.2-INSTALL/lib64/python2.7/site-packages')
import numpy as np
import os
import commands

########################################################################
if __name__=='__main__':
	#Parse user options
	from optparse import OptionParser

	usage = None
	parser = OptionParser(usage=usage)

	parser.add_option("-r", "--run-dic", default=None, type="string", help="Path to run_dic (containing all info about the runs)")
	
	#-------------------------------------------------------------------

	opts, args = parser.parse_args()

	run_dic = pickle.load(open(opts.run_dic))
	
	#-------------------------------------------------------------------
	
	#Check if the user wants to send failure emails
	if run_dic['run mode']['email flag']:
		#Check when the last failure email was sent
		last_failure_email = int(np.genfromtxt(run_dic['config']['run dir']+'/last_failure_email.txt'))
		
		#If not throttled, send another failure email
		current_gps_time = int(commands.getstatusoutput('%s/lalapps_tconvert now'%run_dic['config']['LIB bin dir'])[1])
		if current_gps_time >= (last_failure_email + run_dic['run mode']['email throttle']):
			#First send email
			email_header = "FAILURE: run_oLIB_eagle.py %s process has failed and restarted"%run_dic['config']['run label']
			email_body = "This failure of the run_oLIB_eagle.py %s process has been noticed as of gps time %s.  No more emails will be sent regarding this for another %s seconds.\n"%(run_dic['config']['run label'],current_gps_time,run_dic['run mode']['email throttle'])
			os.system('echo "%s" | mail -s "%s" %s'%(email_body,email_header," ".join(run_dic['run mode']['email addresses'])))

			#Then mark send time
			os.system('echo %s > %s/last_failure_email.txt'%run_dic['config']['run dir'])
