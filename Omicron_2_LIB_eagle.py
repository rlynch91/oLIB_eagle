#!/usr/bin/python

import numpy as np
import os
import time

#############################################
#Define Functions

###
def collect_trigs(rawdir, ifo, channel_name, ppdir):
	"""
	Collect omicron trigs from rawdir and compile them into a single, time-sorted list
	"""
	#Find all omicron raw output files
	files_all = os.listdir("%s/%s/%s:%s"%(rawdir,ifo,ifo,channel_name))
	
	#Make necessary folders
	if not os.path.exists("%s/unclustered/"%ppdir):
		os.makedirs("%s/unclustered/"%ppdir)
	os.system("> %s/unclustered/triggers_unclustered_%s.txt"%(ppdir,ifo))
	
	#Collect trigger info from all raw output files
	for i, f in enumerate(files_all):
		if f.split('.')[1] == 'txt':
			os.system("sed '/#/d' %s/%s/%s:%s/%s >> %s/unclustered/triggers_unclustered_%s.txt"%(rawdir,ifo,ifo,channel_name,f,ppdir,ifo))
			print "Collected file %s of %s for %s"%(i+1, len(files_all), ifo)
	 
	#Sort the compiled file
	os.system("sort %s/unclustered/triggers_unclustered_%s.txt -n -o %s/unclustered/triggers_unclustered_%s.txt"%(ppdir,ifo,ppdir,ifo))
	
	return "%s/unclustered/triggers_unclustered_%s.txt"%(ppdir, ifo)

###
def cluster_trigs(unclust_file, t_clust, ifo, ppdir):
	"""
	Cluster set of neighboring identical-template triggers (same f_0 and Q) to the trigger with the highest SNR within a specified time window
	"""

	#open output file to write to
	if not os.path.exists("%s/clustered/"%ppdir):
		os.makedirs("%s/clustered/"%ppdir)
	clust_file_nm = "%s/clustered/triggers_clustered_%s_tc%s.txt"%(ppdir, ifo, t_clust)
	clust_file = open(clust_file_nm,'wt')
	
	#load in lines from time-sorted file
	with open(unclust_file,'rt') as read_unclust_file:
		lines = list(read_unclust_file)
	i_list = range(len(lines))
	
	#iterate over triggers
	for i in i_list:
		if i == 'SKIP':
			continue
		
		#initialize tmp_dic to store relevant triggers
		tmp_dic = {}
		
		#get current trigger info
		current_elements = lines[i].split()
		t_current = float(current_elements[0])
		f_current = float(current_elements[1])
		snr_current = float(current_elements[2])
		Q_current = float(current_elements[3])
	
		#add current trig to tmp_dic, labeled by snr so that finding loudest event is trivial
		tmp_dic[snr_current] = current_elements
	
		#check to see if on last trigger
		if (i + 1) >= len(i_list):
			#if last trigger, write it and end loop
			final_elements = tmp_dic[max(tmp_dic)]
			t_final = float(final_elements[0])
			f_final = float(final_elements[1])
			snr_final = float(final_elements[2])
			Q_final = float(final_elements[3])
			clust_file.write('%10.10f %10.10f %10.10f %10.10f\n'%(t_final, f_final, snr_final, Q_final))
			break
		
		#compare to subsequent triggers within specified time window
		i_comp = i+1
		while i_list[i_comp] == 'SKIP':  #make sure the comparison line isn't meant to be skipped
			if (i_comp + 1) >= len(i_list):
				break
			i_comp += 1
		if 	i_list[i_comp] == 'SKIP':  #will trigger if the last line is labeled to be skipped
			break
		compare_elements = lines[i_comp].split()
		t_compare = float(compare_elements[0])
		f_compare = float(compare_elements[1])
		snr_compare = float(compare_elements[2])
		Q_compare = float(compare_elements[3])
		
		while abs(t_compare - t_current) <= t_clust:
			#check if comparison trigger is the same template
			if (f_current == f_compare) and (Q_current == Q_compare):
				#if same template, add to tmp_dic...
				tmp_dic[snr_compare] = compare_elements
				
				#...update current trigger...
				t_current = t_compare
				f_current = f_compare
				snr_current = snr_compare
				Q_current = Q_compare
				
				#...and remove comparison index from i_list
				i_list[i_comp] = 'SKIP'
				
			#move comparison trigger to next trigger
			if (i_comp + 1) >= len(i_list):  #break if on last trigger
				break
			i_comp += 1
			while i_list[i_comp] == 'SKIP':  #make sure the comparison line isn't meant to be skipped
				if (i_comp + 1) >= len(i_list):
					break
				i_comp += 1
			if 	i_list[i_comp] == 'SKIP':  #will trigger if the last line is labeled to be skipped
				break
			
			compare_elements = lines[i_comp].split()
			t_compare = float(compare_elements[0])
			f_compare = float(compare_elements[1])
			snr_compare = float(compare_elements[2])
			Q_compare = float(compare_elements[3])
		
		#write maximum snr trigger to file
		final_elements = tmp_dic[max(tmp_dic)]  #choose trigger with loudest SNR
		t_final = float(final_elements[0])
		f_final = float(final_elements[1])
		snr_final = float(final_elements[2])
		Q_final = float(final_elements[3])
		clust_file.write('%10.10f %10.10f %10.10f %10.10f\n'%(t_final, f_final, snr_final, Q_final))
	
	clust_file.close()
	
	os.system("sort %s -n -o %s"%(clust_file_nm, clust_file_nm))
	
	return clust_file_nm
		
###
def constrain_2_eff_segs(trig_file, seg_file, t_clust, ifo, ppdir):
	"""
	Constrain list of time-sorted triggers to lie within the passed time-sorted effective segments (i.e., apply vetoes)
	"""
	#import clustered trigs and segments
	with open(trig_file,'rt') as read_trig_file:
		trig_list= list(read_trig_file)
	seg_start_stop = np.genfromtxt(seg_file).reshape((-1,2))

	#open output file
	survive_file_nm = "%s/clustered/triggers_clustered_%s_tc%s_postveto.txt"%(ppdir, ifo, t_clust)
	survive_file = open(survive_file_nm,'wt')

	i_seg = 0
	end_flag = 0
	seg_start = seg_start_stop[i_seg,0]
	seg_stop = seg_start_stop[i_seg,1]

	#starting at beginning, find next trig
	for i_trig,line in enumerate(trig_list):
			
		#Get time for each trig
		trig_time = float(line.split()[0])
		
		#Find first segment that has an end after the trig time (only iterate once all trig times have passed segment end)
		while seg_stop < trig_time:
			#Check to see if there is another seg
			if i_seg >= len(seg_start_stop)-1:
				#Not another seg so end the loop over trigs
				end_flag = 1
				break
			else:
				#Move to next seg
				i_seg += 1
				seg_start = seg_start_stop[i_seg,0]
				seg_stop = seg_start_stop[i_seg,1]
		if end_flag:
			break
			
		#Check to see if trig lies completely within segment
		if (trig_time >= seg_start) and (trig_time <= seg_stop):
			#Trig lies within segment, so write to file
			survive_file.write("%s"%line)
		else:
			#Trig does not lie within segment, so disregard it
			continue
			
	survive_file.close()
		
	return survive_file_nm
	
###	
def coincidence(trig_list_1, trig_list_2, tshift1, tshift2, tshift_num, ifos1, ifo2, t_coin, snr_coin, coin_group, coin_mode, ppdir):
	"""
	Coincide two sets of triggers, using timing and snr parameters and constraining concident triggers to have identical f_0 and Q
	"""
	#Open file to write coincident triggers to
	coin_file_nm = "%s/coincident/%s/%s/triggers_coincident_%s%s_tc%s_snr%s_tsnum%s_.txt"%(ppdir, coin_group, coin_mode, ifos1, ifo2, t_coin, snr_coin, tshift_num)
	if not os.path.exists("%s/coincident/%s/%s/"%(ppdir, coin_group, coin_mode)):
		os.makedirs("%s/coincident/%s/%s/"%(ppdir, coin_group, coin_mode))
	coin_file = open(coin_file_nm,'wt')
	
	#Iterate through list 1, comparing to list 2
	i2_min = 0
	
	for current_line in trig_list_1:
		current_elements = current_line.split()
		t_current = float(current_elements[0]) + float(tshift1)
		f_current = float(current_elements[1])
		snr_current = float(current_elements[2])
		Q_current = float(current_elements[3])
		
		#Update reference index for list 2
		t2_min = float(trig_list_2[i2_min].split()[0]) + float(tshift2)
		while abs(t_current - t2_min) > t_coin:
			if (t2_min - t_current) >  t_coin:
				break
			elif (i2_min + 1) >= len(trig_list_2):
				break
			else:
				i2_min += 1
				t2_min = float(trig_list_2[i2_min].split()[0]) + float(tshift2)
		
		#Search for coincident templates within time window
		i2_compare = i2_min
		compare_elements = trig_list_2[i2_compare].split()
		t_compare = float(compare_elements[0]) + float(tshift2)
		f_compare = float(compare_elements[1])
		snr_compare = float(compare_elements[2])
		Q_compare = float(compare_elements[3])
		
		while abs(t_current - t_compare) <= t_coin:
			if (f_current == f_compare) and (Q_current == Q_compare) and (snr_current >= snr_coin) and (snr_compare >= snr_coin):
				if len(current_elements) <= 4:
					coin_file.write( "%10.10f %10.10f %10.10f %10.10f %s %s\n"%((t_current+t_compare)/2., (f_current+f_compare)/2., np.sqrt(snr_current**2. + snr_compare**2.), (Q_current+Q_compare)/2., " ".join(current_elements), " ".join(compare_elements)) )
				else:
					coin_file.write( "%10.10f %10.10f %10.10f %10.10f %s %s\n"%((t_current+t_compare)/2., (f_current+f_compare)/2., np.sqrt(snr_current**2. + snr_compare**2.), (Q_current+Q_compare)/2., " ".join(current_elements[4:]), " ".join(compare_elements)) )
			if (i2_compare + 1) >= len(trig_list_2):
				break

			i2_compare += 1
			compare_elements = trig_list_2[i2_compare].split()
			t_compare = float(compare_elements[0]) + float(tshift2)
			f_compare = float(compare_elements[1])
			snr_compare = float(compare_elements[2])
			Q_compare = float(compare_elements[3])
	
	coin_file.close()
	
	os.system("sort %s -n -o %s"%(coin_file_nm, coin_file_nm))
				
	return coin_file_nm
	
###
def time_slide(trig_files1, trig_files2, ts_list_1, ts_list_2, ifos1, ifo2, t_coin, snr_coin, coin_group, coin_mode, ppdir):
	"""
	Create a set of coincided timeslides
	"""
	#Create folder for writing coincident segments
	if not os.path.exists("%s/coincident/%s/%s/"%(ppdir,coin_group,coin_mode)):
		os.makedirs("%s/coincident/%s/%s/"%(ppdir,coin_group,coin_mode))
	
	#Initiate running sums for livetime calculations
	new_trigfiles = [None]*len(trig_files1)
	
	#Loop over timeslides, doing trigger coincidence for each
	for i in xrange(len(trig_files1)):
		#Initiate this particular timeslide
		ts1 = ts_list_1[i]
		ts2 = ts_list_2[i]
			
		#load in trig lists
		with open(trig_files1[i],'rt') as read_trig_file_1:
			trig_list_1 = list(read_trig_file_1)
		with open(trig_files2[i],'rt') as read_trig_file_2:
			trig_list_2 = list(read_trig_file_2)
				
		#do coincidence with trig lists
		new_trigfiles[i] = coincidence(trig_list_1=trig_list_1, trig_list_2=trig_list_2, tshift1=ts1, tshift2=ts2, tshift_num=i, ifos1=ifos1, ifo2=ifo2, t_coin=t_coin, snr_coin=snr_coin, coin_group=coin_group, coin_mode=coin_mode, ppdir=ppdir)
		print "Coincided trigs for %s and %s for time slide number %s"%(ifos1, ifo2, i)
		
	#Return list of new intersected segment files
	return new_trigfiles

###
def LIB_trig_production(ifo_list, tshift_dic, LIB_window, coin_group, coin_mode, ppdir):
	"""
	Downselect triggers by performing log likelihood ratio thresholding test
	"""
	#Create folder for writing LIB trigs	
	if not os.path.exists("%s/LIB_trigs/%s/%s/"%(ppdir,coin_group,coin_mode)):
		os.makedirs("%s/LIB_trigs/%s/%s/"%(ppdir,coin_group,coin_mode))
	
	#Open write files for LIB trigs and their corresponding timeslides for both 0-lags and timeslide triggers
	lib_0lag_times = open('%s/LIB_trigs/%s/%s/LIB_0lag_times_%s.txt'%(ppdir, coin_group, coin_mode, coin_group), 'wt')
	lib_0lag_timeslides = open('%s/LIB_trigs/%s/%s/LIB_0lag_timeslides_%s.txt'%(ppdir, coin_group, coin_mode, coin_group), 'wt')
	lib_ts_times = open('%s/LIB_trigs/%s/%s/LIB_ts_times_%s.txt'%(ppdir, coin_group, coin_mode, coin_group), 'wt')
	lib_ts_timeslides = open('%s/LIB_trigs/%s/%s/LIB_ts_timeslides_%s.txt'%(ppdir, coin_group, coin_mode, coin_group), 'wt')
	
	#Create identifying label by merging ifos together
	ifos_together = "".join(ifo_list)
	
	#Find necessary files to grab triggers from
	files_all = os.listdir("%s/coincident/%s/%s/"%(ppdir,coin_group,coin_mode))
	files_final = []
	for f in files_all:
		if f.split('_')[2] == ifos_together:
			files_final += [f]
	files_final = sorted(files_final)
	
	#Loop through the files
	for f in files_final:
		#Load in coincident omicron data for each timeslide
		terms = f.split("_")
		tshift_num = float(terms[5].split("tsnum")[1])
		try:
			data_array = np.genfromtxt("%s/coincident/%s/%s/%s"%(ppdir,coin_group,coin_mode,f)).reshape( (-1,4*(len(ifo_list)+1)) )
		except IOError:
			data_array = np.array([])
				
		if len(data_array):
			#Cluster all trigs so there is only one trig per LIB analysis window
			final_trigs = cluster_LIB_trigs(LIB_trig_array=data_array, LIB_window=LIB_window)
			
			#Save LIB triggers
			np.savetxt('%s/LIB_trigs/%s/%s/LIB_trigs_%s_tsnum%s_.txt'%(ppdir, coin_group, coin_mode, coin_group, tshift_num), final_trigs)
			if (coin_mode == "0lag") or (coin_mode == "sig_train"):
				for i in xrange(len(trigs_above_thresh)):
					lib_0lag_times.write('%10.10f\n'%final_trigs[i,0])
					lib_0lag_timeslides.write('%s\n'%( " ".join([tshift_dic[ifo][i] for ifo in ifo_list]) ))
			elif (coin_mode == "back") or (coin_mode == "noise_train"):
				for i in xrange(len(trigs_above_thresh)):
					lib_ts_times.write('%10.10f\n'%final_trigs[i,0])
					lib_ts_timeslides.write('%s\n'%( " ".join([tshift_dic[ifo][i] for ifo in ifo_list]) ))
		else:
			os.system('> %s/LIB_trigs/%s/%s/LIB_trigs_%s_tsnum%s_.txt'%(ppdir, coin_group, coin_mode, coin_group, tshift_num))
	
	lib_0lag_times.close()
	lib_0lag_timeslides.close()
	lib_ts_times.close()
	lib_ts_timeslides.close()

###
def cluster_LIB_trigs(LIB_trig_array, LIB_window):
	"""
	Cluster LIB trigs so that the LIB trig times are those of the loudest trig within a given LIB window length
	"""
	#Initialize for first loop over trigs
	iterations = 0
	clust_flag = 1  #Do this to start loop below
	in_array = LIB_trig_array

	#Loop over algorithm until no clustering is done
	while clust_flag:
		
		#Count number of iterations through algorithm
		iterations += 1
		
		#Initialize out_array
		out_list = []
		
		#Initialize clust_flag as 0, marking no clustering yet done
		clust_flag = 0

		#Iterate over lines, clustering them into windows of specified length, centered on highest SNR trigger within window
		t_start = float('inf')
		window_dic = {}
		found = 0

		for line in in_array:
			#Read in necessary data parameters
			t_current = line[0]
			snr_current = line[2]
			
			#Compare current time to window start time to see if current trig is in window
			if abs(t_current - t_start) <= 0.5*LIB_window:
				#If in current window, save trigger in dic with snr as key
				window_dic[snr_current] = line
				#Note that clustering was done during this iteration
				clust_flag = 1
			else:
				#Trigger outside of window, so write old window and start new window
				if window_dic:
					#If there are triggers in the old window, write to file
					found += 1
					max_line = window_dic[max(window_dic)]
					out_list += [max_line]
				
				#Set start time of new window
				t_start = t_current
				
				#Initiate new window
				window_dic = {}
				window_dic[snr_current] = line
				
		#Check and write last window
		if window_dic:
			#If there are triggers in the old window, write to file
			found += 1
			max_line = window_dic[max(window_dic)]
			out_list += [max_line]	

		#Turn out_list into out_array
		out_array = np.array(out_list)
		if len(out_array) == 0.:
			#No trigs, can break clustering loop
			break

		#Replace initial trig array with down-selected trig array
		in_array = out_array
			
	print "Finished down selection of LIB trigs after %s iterations"%iterations
	return out_array

###
def crop_segs(seg_file, overlap, ifo, ppdir):
	"""
	Crop out the Omicron overlap from merged segments to get segments in which triggers can actually occur (note that these segments should be merged first!)
	"""
	#import segments
	seg_start_stop = np.genfromtxt(seg_file).reshape((-1,2))
	
	#open output file
	cropped_segs_file_nm = "%s/live_segs/segments_%s_cropped.seg"%(ppdir, ifo)
	if not os.path.exists("%s/live_segs/"%ppdir):
		os.makedirs("%s/live_segs/"%ppdir)
	cropped_segs_file = open(cropped_segs_file_nm,'wt')
	
	#loop through segments, cropping off the Omicron overlap from the edges
	for seg in seg_start_stop:
		tmp_start = seg[0] + int(overlap/2.)
		tmp_stop = seg[1] - int(overlap/2.)
		#write cropped segment start and stop times if still valid after cropping
		if tmp_start < tmp_stop:
			cropped_segs_file.write("%10.10f %10.10f\n"%(tmp_start,tmp_stop))
			
	cropped_segs_file.close()
	return cropped_segs_file_nm
		
###
def effective_segs(seg_file, veto_file, ifo, ppdir):
	"""
	Remove vetoes from segment list for a given ifo, thus creating effective segments
	"""
	#import segments and vetoes
	seg_start_stop = np.genfromtxt(seg_file).reshape((-1,2))

	try:
		veto_start_stop = np.genfromtxt(veto_file).reshape((-1,2))
		if not veto_start_stop.any():
			veto_start_stop = np.array([[float('inf'), float('inf')]])
	except IOError:
		veto_start_stop = np.array([[float('inf'), float('inf')]])

	#sort segments and vetoes, this sorting will be conserved
	seg_start_stop = np.array(sorted(seg_start_stop, key = lambda x:x[0]))
	veto_start_stop = np.array(sorted(veto_start_stop, key = lambda x:x[0]))

	#open output file
	eff_segs_file_nm = "%s/live_segs/segments_%s_postveto.seg"%(ppdir, ifo)
	if not os.path.exists("%s/live_segs/"%ppdir):
		os.makedirs("%s/live_segs/"%ppdir)
	eff_segs_file = open(eff_segs_file_nm,'wt')

	#Start at first veto
	i_veto = 0
	veto_start = veto_start_stop[i_veto,0]
	veto_stop = veto_start_stop[i_veto,1]

	#Loop through segments
	for i_seg in xrange(len(seg_start_stop)):
		seg_start = seg_start_stop[i_seg,0]
		seg_stop = seg_start_stop[i_seg,1]
		
		#Interate through vetoes until we find one that either intersects with our segment or occurs after
		while (veto_start < seg_start) and (veto_stop < seg_start):
			if i_veto >= len(veto_start_stop)-1:
				#if at end of vetoes, set veto times to infinity
				veto_start = float('inf')
				veto_stop = float('inf')
			else:
				#increment veto
				i_veto += 1
				veto_start = veto_start_stop[i_veto,0]
				veto_stop = veto_start_stop[i_veto,1]
		
		###At this point, at least veto_stop occurs after seg_start###
		
		#Choose initial segment start based on location of veto
		if (veto_start <= seg_start) and (veto_stop >= seg_start):
			start = veto_stop
		elif (veto_start > seg_start) and (veto_stop > seg_start):	
			start = seg_start
		else:
			raise ValueError, "Encountered situation that is not considered, exiting"
		
		#Loop through vetoes occuring within segment
		while (veto_start < seg_stop) and (veto_stop < seg_stop):
			if (veto_start <= seg_start) and (veto_stop < seg_stop):
				#Increment veto so that veto occurs completely after segment start
				if i_veto >= len(veto_start_stop)-1:
					#if at end of vetoes, set to infinity
					veto_start = float('inf')
					veto_stop = float('inf')
				else:
					#increment veto
					i_veto += 1
					veto_start = veto_start_stop[i_veto,0]
					veto_stop = veto_start_stop[i_veto,1]
			elif (veto_start > seg_start) and (veto_stop < seg_stop):
			#Record the effective segments
				stop = veto_start
				if start < stop:
					eff_segs_file.write("%10.10f %10.10f\n"%(start,stop))
				#Change to new start and iterate veto
				start = veto_stop
				if i_veto >= len(veto_start_stop)-1:
					#if at end of vetoes, set to infinity
					veto_start = float('inf')
					veto_stop = float('inf')
				else:
					#increment veto
					i_veto += 1
					veto_start = veto_start_stop[i_veto,0]
					veto_stop = veto_start_stop[i_veto,1]
			else:
				raise ValueError, "Encountered situation that is not considered, exiting"
			
		###At this point, at least veto_stop occurs after seg_stop###
			
		#We should now be at last relevant veto for this segment
		if (veto_start <= seg_start) and (veto_stop >= seg_stop):
			pass	
		elif (veto_start <= seg_stop) and (veto_stop >= seg_stop):
		#Record the effective segments
			stop = veto_start
			if start < stop:
				eff_segs_file.write("%10.10f %10.10f\n"%(start,stop))
		elif (veto_start >= seg_stop) and (veto_stop >= seg_stop):
			stop = seg_stop
			if start < stop:
				eff_segs_file.write("%10.10f %10.10f\n"%(start,stop))
					
	eff_segs_file.close()
	return eff_segs_file_nm

###
def merge_segs(seg_file, ifo, ppdir):
	"""
	For a time-sorted segment list, combine segments that are divided at a common start/stop time
	"""
	#Load segments into an array
	seg_array = np.genfromtxt(seg_file).reshape((-1,2))
	
	#open output file
	write_seg_file_nm = "%s/live_segs/segments_%s_merged.seg"%(ppdir, ifo)
	if not os.path.exists("%s/live_segs/"%ppdir):
		os.makedirs("%s/live_segs/"%ppdir)
	write_seg_file = open(write_seg_file_nm,'wt')
	
	#If only 1 segment, nothing needs to be merged
	if np.shape(seg_array) == (1,2):
		write_seg_file.write("%10.10f %10.10f\n"%(seg_array[0,0],seg_array[0,1]))	
	
	#If more than 1 segment, loop over segments
	else:
		#Initialize first pair of neighboring segs
		i_seg = 0
		start_current = seg_array[i_seg,0]
		stop_current = seg_array[i_seg,1]
		
		i_seg += 1
		start_next = seg_array[i_seg,0]
		stop_next = seg_array[i_seg,1]
		
		#Loop over all pairs of neighboring segs
		while i_seg < len(seg_array):
			#Check if segments need to be merged
			if stop_current == start_next:
				#merge current and next segments together
				stop_current = stop_next
			else:
				#write current segment start and stop times
				if start_current < stop_current:
					write_seg_file.write("%10.10f %10.10f\n"%(start_current,stop_current))
				#make next segment the current segment
				start_current = start_next
				stop_current = stop_next
			
			#iterate to next segment
			if i_seg >= len(seg_array) - 1:
				#if we've reached last seg, then break and end loop
				break
			else:
				#else iterate to next segment
				i_seg += 1
				start_next = seg_array[i_seg,0]
				stop_next = seg_array[i_seg,1]
				
		#Write final segment
		if start_current < stop_current:
			write_seg_file.write("%10.10f %10.10f\n"%(start_current,stop_current))
				
	#Close seg_file
	write_seg_file.close()
	
	
###
def intersect_segments(seg_array1, seg_array2, ifos1, ifo2, ts_num, coin_group, coin_mode, ppdir):
	"""
	For time-sorted segments, find intersection of livetime between two detectors
	"""
		
	seg_intersect_nm = "%s/live_segs/%s/%s/intersect_%s%s_tsnum%s.seg"%(ppdir, coin_group, coin_mode, ifos1, ifo1, ts_num)
	if not os.path.exists("%s/live_segs/%s/%s/"%(ppdir, coin_group, coin_mode)):
		os.makedirs("%s/live_segs/%s/%s/"%(ppdir, coin_group, coin_mode))
	seg_intersect = open(seg_intersect_nm,'wt')
	
	i1 = 0
	i2 = 0
	
	while (i1 <= len(seg_array1)-1) and (i2 <= len(seg_array2)-1):
		#Take highest start time and lowest end time
		t_low_tmp = max(seg_array1[i1,0], seg_array2[i2,0])
		t_high_tmp = min(seg_array1[i1,1], seg_array2[i2,1])
		
		#Print intersecting segment to file
		if t_low_tmp < t_high_tmp:
			seg_intersect.write("%10.10f %10.10f\n"%(t_low_tmp, t_high_tmp))
		
		#Advance whichever current segment ends first
		if (seg_array1[i1,1] <= seg_array2[i2,1]):
			i1 += 1
		elif (seg_array2[i2,1] <= seg_array1[i1,1]):
			i2 += 1
	
	seg_intersect.close()
	return seg_intersect_nm

###
def calculate_livetimes(seg_files1, seg_files2, ts_list_1, ts_list_2, ifos1, ifo2, coin_group, coin_mode, ppdir):
	"""
	Add up effective segments for 0-lag and for each timeslide to calculate effective livetimes
	"""	
	#Create folder for writing coincident segments
	if not os.path.exists("%s/live_segs/%s/%s/"%(ppdir,coin_group,coin_mode)):
		os.makedirs("%s/live_segs/%s/%s/"%(ppdir,coin_group,coin_mode))
	
	#Initiate running sums for livetime calculations
	zero_lag_lt = 0.
	timeslide_lt = 0.
	new_segfiles = [None]*len(seg_files1)
	
	#Loop over timeslides, intersecting segs and calculating overlapping livetime for each
	for i in xrange(len(seg_files1)):
		#Initiate this particular timeslide
		ts1 = ts_list_1[i]
		ts2 = ts_list_2[i]
		ts_lt = 0.
		
		#Load 1st set of segmets into an array
		seg_array1 = np.genfromtxt(seg_files1[i]).reshape((-1,2)) + ts1
		
		#Load 2nd set of segments into an array
		seg_array2 = np.genfromtxt(seg_files2[i]).reshape((-1,2)) + ts2
		
		#Intersect the timeslided segments
		new_segfiles[i] = intersect_segments(seg_array1=seg_array1, seg_array2=seg_array2, ifos1=ifos1, ifo2=ifo2, ts_num=i, coin_group=coin_group, coin_mode=coin_mode, ppdir=ppdir)
		
		#Add up the livetime from the intersected segments
		read_tmp_intersected_segs = open(new_segfiles[i],'rt')
		for line in read_tmp_intersected_segs:
			elements = line.split()
			ts_lt += float(elements[1]) - float(elements[0])
		read_tmp_intersected_segs.close()
		
		#Add livetime to appropriate sum
		if (coin_mode == "0lag") or (coin_mode == "sig_train"):
			zero_lag_lt += ts_lt
		elif (coin_mode == "back") or (coin_mode == "noise_train"):
			timeslide_lt += ts_lt
		
	#Write summed livetimes to file
	if (coin_mode == "0lag") or (coin_mode == "sig_train"):
		np.savetxt("%s/live_segs/%s/%s/livetime_0lag_%s%s.txt"%(ppdir,coin_group,coin_mode,ifos1,ifo2), np.array([zero_lag_lt]))
	elif (coin_mode == "back") or (coin_mode == "noise_train"):
		np.savetxt("%s/live_segs/%s/%s/livetime_timeslides_%s%s.txt"%(ppdir,coin_group,coin_mode,ifos1,ifo2), np.array([timeslide_lt]))
	
	#Return list of new intersected segment files
	return new_segfiles
	
###
def get_LIB_trigs_from_clustered_trigs(run_dic, seg_files, clust_files, LIB_window, coin_group, coin_mode, ppdir):
	"""
	"""
	#Get coincidence parameters
	t_coin = run_dic['coincidence'][coin_group]['coincidence window']
	snr_coin = run_dic['coincidence'][coin_group]['coincidence snr thresh']
	coin_ifos = run_dic['coincidence'][coin_group]['ifos']
	
	if (coin_mode == "0lag") or (coin_mode == "sig_train"):
		coin_ts_dic = {}
		for ifo in coin_ifos:
			coin_ts_dic = np.array([0.])
		
	elif coin_mode == "back":
		coin_ts_dic = run_dic['coincidence'][coin_group]['back timeslides']
	
	elif coin_mode == "noise_train":
		coin_ts_dic = run_dic['coincidence'][coin_group]['training timeslides']

	#Make necessary folders
	if not os.path.exists("%s/live_segs/%s/%s/"%(ppdir,coin_group,coin_mode)):
		os.makedirs("%s/live_segs/%s/%s/"%(ppdir,coin_group,coin_mode))
	os.system('rm %s/live_segs/%s/%s/*'%(ppdir,coin_group,coin_mode))
	
	if not os.path.exists("%s/coincident/%s/%s/"%(ppdir,coin_group,coin_mode)):
		os.makedirs("%s/coincident/%s/%s/"%(ppdir,coin_group,coin_mode))
	os.system('rm %s/coincident/%s/%s/*'%(ppdir,coin_group,coin_mode))

	#Initialize first ifo to do coincidence with
	ifos_prev = coin_ifos[0]
	timeslides_prev = coin_ts_dic[ifos_prev]
	seg_files_prev = [seg_files[ifos_prev]]*len(timeslides_prev)
	clust_files_prev = [clust_files[ifos_prev]]*len(timeslides_prev)

	for i in xrange(len(coin_ifos)-1):
		
		#Get info for new ifo to do coincidence with
		ifo_new = coin_ifos[i+1]
		timeslides_new = coin_ts_dic[ifo_new]
		seg_files_new = [seg_files[ifo_new]]*len(timeslides_new)
		clust_files_new = [clust_files[ifo_new]]*len(timeslides_new)
						
		#Live time intersection
		coin_seg_files = calculate_livetimes(seg_files1=seg_files_prev, seg_files2=seg_files_new, ts_list_1=timeslides_prev, ts_list_2=timeslides_new, ifos1=ifos_prev, ifo2=ifo_new, coin_group=coin_group, coin_mode=coin_mode, ppdir=ppdir)
		print "Calculated total coincident live time for 0-lag and timeslides"

		#coincidence
		coin_trig_files = time_slide(trig_files1=clust_files_prev, trig_files2=clust_files_new, ts_list_1=timeslides_prev, ts_list_2=timeslides_new, ifos1=ifos_prev, ifo2=ifo_new, t_coin=t_coin, snr_coin=snr_coin, coin_group=coin_group, coin_mode=coin_mode, ppdir=ppdir)

		#Prepare for next round of coincidence
		ifos_prev += ifo_new
		timeslides_prev = np.array([0.]*len(timeslides_prev))
		seg_files_prev = coin_seg_files
		clust_files_prev = coin_trig_files
	
	#LIB window clustering
	if not os.path.exists("%s/LIB_trigs/%s/%s/"%(ppdir,coin_group,coin_mode)):
		os.makedirs("%s/LIB_trigs/%s/%s/"%(ppdir,coin_group,coin_mode))
	os.system('rm %s/LIB_trigs/%s/%s/*'%(ppdir,coin_group,coin_mode))

	LIB_trig_production(ifo_list=coin_ifos, tshift_dic=coin_ts_dic, LIB_window=LIB_window, coin_group=coin_group, coin_mode=coin_mode, ppdir=ppdir)
	print "Down-selected trigs to run LIB on for %s %s"%(coin_group, coin_mode)
	
##############################################
if __name__=='__main__':

	from optparse import OptionParser

	usage = None
	parser = OptionParser(usage=usage)

	#general options
	parser.add_option("-r", "--run-dic", default=None, type="string", help="Path to run_dic (containing all info about the runs")
	parser.add_option("", "--sig-train", default=False, action="store_true", help="Pass if want to run over injections for signal training")

	#----------------------------------------------

	opts, args = parser.parse_args()

	run_dic = pickle.load(open(opts.run_dic))
	sig_train_flag = opts.sig_train
	run_mode = run_dic['run mode']['line']
	
	#----------------------------------------------
	
	#MAIN

	#----------------------------------------------
	
	#Check if in online run mode
	if run_mode == 'Online':
		
		#First initialize the variables we need
		ifos_all = np.array(run_dic['ifos']['names'])
		ifos = []
		for ifo in ifos_all:
			if run_dic['data']['success flags'][ifo]:
				ifos += [ifo]
		overlap = run_dic['config']['overlap']
		t_clust = run_dic['config']['dt clust']
		LIB_window = run_dic['prior ranges']['LIB window']
		
		channel_names = {}
		segs = {}
		veto_files = {}
		for ifo in ifos:
			channel_names[ifo] = run_dic['ifos'][ifo]['channel name']
			segs[ifo] = run_dic['data']['seg files'][ifo]
			veto_files[ifo] = run_dic['vetoes'][ifo]
		
		if not sig_train_flag:
			ppdir = "%s/PostProc/"%run_dic['seg dir']
			rawdir = "%s/raw/"%run_dic['seg dir']
		else:
			ppdir = "%s/PostProc_sig_train/"%run_dic['seg dir']
			rawdir = "%s/raw_sig_train/"%run_dic['seg dir']
		
		#collect
		if not os.path.exists("%s/unclustered/"%ppdir):
			os.makedirs("%s/unclustered/"%ppdir)
		os.system('rm %s/unclustered/*'%ppdir)
		unclust_files = {}
		for i,ifo in enumerate(ifos):
			unclust_files[ifo] = collect_trigs(rawdir=rawdir, ifo=ifo, channel_name=channel_names[i], ppdir=ppdir)
			print "Collected and sorted trigs for %s"%ifo

		#cluster
		if not os.path.exists("%s/clustered/"%ppdir):
			os.makedirs("%s/clustered/"%ppdir)
		os.system('rm %s/clustered/*'%ppdir)
		clust_files = {}
		for ifo in ifos:		
			clust_files[ifo] = cluster_trigs(unclust_file=unclust_files[ifo], t_clust=t_clust, ifo=ifo, ppdir=ppdir)
			print "Clustered trigs for %s"%ifo

		#cropped and effective segments
		if not os.path.exists("%s/live_segs/"%ppdir):
			os.makedirs("%s/live_segs/"%ppdir)
		os.system('rm %s/live_segs/*'%ppdir)
		seg_files = {}
		for i,ifo in enumerate(ifos):
			seg_files[ifo] = merge_segs(seg_file=segs[i], ifo=ifo, ppdir=ppdir)
			seg_files[ifo] = crop_segs(seg_file=seg_files[ifo], overlap=overlap, ifo=ifo, ppdir=ppdir)
			seg_files[ifo] = effective_segs(seg_file=seg_files[ifo], veto_file=veto_files[ifo], ifo=ifo, ppdir=ppdir)
			print "Cropped Omicron overlaps and removed vetoes to create effective segments for %s"%ifo
		
		#apply vetoes by constraining triggers to effective segments
		for ifo in ifos:	
			clust_files[ifo] = constrain_2_eff_segs(trig_file=clust_files[ifo], seg_file=seg_files[ifo], t_clust=t_clust, ifo=ifo, ppdir=ppdir)
			print "Applied vetoes by constraining triggers to effective segments for %s"%ifo
		
		#Loop over all coincidence groups
		for key in run_dic['coincidence']:
			#Check to see if all ifos of the coincidence group are analyzable
			coin_flag = True
			for ifo in run_dic['coincidence'][key]['ifos']:
				if run_dic['data']['success flags'][ifo]:
					continue
				else:
					coin_flag = False
					break
			
			#If all ifos in coincidence group are analyzable, then do the coincidence
			if coin_flag:
					
				#Check if injections are in the data for signal training
				if not sig_train_flag:			
					#Do 0-lag coincidence				
					if run_dic['coincidence'][key]['analyze 0lag'] == True:
						get_LIB_trigs_from_clustered_trigs(run_dic=run_dic, seg_files=seg_files, clust_files=clust_files, LIB_window=LIB_window, coin_group=key, coin_mode='0lag', ppdir=ppdir)
					
					#Do background coincidence	
					if run_dic['coincidence'][key]['analyze back'] == True:
						get_LIB_trigs_from_clustered_trigs(run_dic=run_dic, seg_files=seg_files, clust_files=clust_files, LIB_window=LIB_window, coin_group=key, coin_mode='back', ppdir=ppdir)	
					
					#Do noise training coincidence		
					if run_dic['coincidence'][key]['analyze noise training'] == True:
						get_LIB_trigs_from_clustered_trigs(run_dic=run_dic, seg_files=seg_files, clust_files=clust_files, LIB_window=LIB_window, coin_group=key, coin_mode='noise_train', ppdir=ppdir)
				
				else:
					#Do signal training coincidence		
					if run_dic['coincidence'][key]['analyze signal training'] == True:
						get_LIB_trigs_from_clustered_trigs(run_dic=run_dic, seg_files=seg_files, clust_files=clust_files, LIB_window=LIB_window, coin_group=key, coin_mode='sig_train', ppdir=ppdir)
		
		#Tar Omicron triggers now that they are no longer needed
		if run_dic['run mode']['tar Omicron']:
			os.system('tar -zcvf %s.tar.gz %s'%(rawdir,rawdir))
			os.system('rm %s -r'%rawdir)
							
		#Complete
		print "Complete"

	#----------------------------------------------

	#Check if in offline run mode
	elif run_mode == 'Offline':
		pass
