#!/usr/bin/python

import sys
sys.path.insert(1,'/home/ryan.lynch/numpy/numpy-1.8.2-INSTALL/lib64/python2.7/site-packages')
import numpy as np
import pickle
import os

#############################################
if __name__=='__main__':
	#Parse user options
	from optparse import OptionParser

	usage = None
	parser = OptionParser(usage=usage)

	parser.add_option("", "--new-back-dic", default=None, type="string", help="Path to background dictionary with new data")
	parser.add_option("", "--new-back-lt", default=None, type="string", help="Path to file with new background livetime")
	parser.add_option("", "--old-back-dic", default=None, type="string", help="Path to background dictionary with old data")
	parser.add_option("", "--old-back-lt", default=None, type="string", help="Path to file with old background livetime")
	parser.add_option("", "--outdir", default=None, type="string", help="Path to directory in which to save outputs")
	parser.add_option("", "--max-back-size", default=None, type="int", help="Maximum number of points to have in background dictionary")
	parser.add_option("", "--new-gps-day", default=None, type="int", help="GPS day that the new day covers")

	#-----------------------------------------------------------------------

	opts, args = parser.parse_args()

	new_back_dic = pickle.load(open(opts.new_back_dic))
	new_back_lt = float(np.genfromtxt(opts.new_back_lt))
	old_back_dic = pickle.load(open(opts.old_back_dic))
	old_back_lt = float(np.genfromtxt(opts.old_back_lt))
	outdir = opts.outdir
	max_back_size = opts.max_back_size
	new_gps_day = opts.new_gps_day

	#=======================================================================

	#################################
	# Copy old data to backup files #
	#################################
	os.system('cp %s/collected_background_dictionary.pkl %s/collected_background_dictionary_old.pkl'%(outdir,outdir))
	os.system('cp %s/collected_background_livetime.txt %s/collected_background_livetime_old.txt'%(outdir,outdir))

	################################
	# Update training dictionaries #
	################################

	#Create updated dictionary
	updated_back_dic = {}
	updated_lt = 0.
	event = 0
	
	#First add the new background events, only adding if gps day can be fully contained within the dic
	if (event + len(new_back_dic)) <= max_back_size:
		#Add livetime
		updated_lt += new_back_lt
		
		#Add events to dic
		for key in new_back_dic:
			#Event should be added to background
			updated_back_dic[event] = new_back_dic[key]
			updated_back_dic[event]['GPS Day']={}
			updated_back_dic[event]['GPS Day']['Day'] = int(new_gps_day)
			updated_back_dic[event]['GPS Day']['Livetime'] = new_back_lt
			
			#Update the number of events currently in background dictionary
			event += 1
			if event > max_back_size:
				raise ValueError, "Trying to add new background events when the entirety of their GPS day does not fit in dic"
	
	#Then add the old background events, only adding if gps day can be fully contained within the dic
	old_gps_day = int(new_gps_day)
	for key in old_back_dic:
		#Check if we're at a new gps day
		if int(old_back_dic[key]['GPS Day']['Day']) < old_gps_day:
			#At new GPS day, check how many events are in this day
			old_gps_day = int(old_back_dic[key]['GPS Day']['Day'])
			tmp_key = key
			tmp_num = 0
			while int(old_back_dic[tmp_key]['GPS Day']['Day']) == old_gps_day:
				tmp_key += 1
				tmp_num += 1
			#If too many events, then break loop
			if (event + tmp_num) > max_back_size:
				break
			#Else, add livetime for this new gps day
			else:
				updated_lt += float(old_back_dic[key]['GPS Day']['Livetime'])
			
		#Make sure we are going backwords in time
		elif int(old_back_dic[key]['GPS Day']['Day']) > old_gps_day:
			raise ValueError, "The old background dictionary isn't sorted from newest events to oldest"
		
		#If we've made is this far, then add the events
		updated_back_dic[event] = old_back_dic[key]
		
		#Update the number of events currently in background dictionary
		event += 1
		if event > max_back_size:
			raise ValueError, "Trying to add new background events when the entirety of their GPS day does not fit in dic"
	
	#Save updated dictionary
	pickle.dump(updated_back_dic,open('%s/collected_background_dictionary_new.pkl'%outdir,'wt'))
	np.savetxt('%s/collected_background_livetime_new.txt'%outdir,np.array([updated_lt]))

	#################################
	# Move new data to proper files #
	#################################
	os.system('mv %s/collected_background_dictionary_new.pkl %s/collected_background_dictionary.pkl'%(outdir,outdir))
	os.system('mv %s/collected_background_livetime_new.txt %s/collected_background_livetime.txt'%(outdir,outdir))
	
