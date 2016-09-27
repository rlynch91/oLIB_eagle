#!/usr/bin/python

import sys
sys.path.insert(1,'/home/ryan.lynch/numpy/numpy-1.8.2-INSTALL/lib64/python2.7/site-packages')
import numpy as np
import os
import pickle
from ligo.gracedb.rest import GraceDb
import json
import LLRT_object_eagle
import commands

#############################################
#Define Functions

###
def check_parameter_space(dic_entry, search_bin, run_dic):
	q_min = run_dic['search bins'][search_bin]['low quality cut']
	q_max = run_dic['search bins'][search_bin]['high quality cut']
	f_min = run_dic['search bins'][search_bin]['low freq cut']
	f_max = run_dic['search bins'][search_bin]['high freq cut']
	BCI_min = run_dic['search bins'][search_bin]['low BCI cut']
	BCI_max = run_dic['search bins'][search_bin]['high BCI cut']
	logBSN_min = run_dic['search bins'][search_bin]['low logBSN cut']
	logBSN_max = run_dic['search bins'][search_bin]['high logBSN cut']
	
	#Check to see if the event lies within the defined parameter space
	if (dic_entry['quality']['posterior median'] >= q_min) and (dic_entry['quality']['posterior median'] <= q_max) and (dic_entry['frequency']['posterior median'] >= f_min) and (dic_entry['frequency']['posterior median'] <= f_max) and (dic_entry['BCI'] >= BCI_min) and (dic_entry['BCI'] <= BCI_max) and (np.log10(dic_entry['BSN']) >= logBSN_min) and (np.log10(dic_entry['BSN']) <= logBSN_max):
		flag = True
	else:
		flag = False
		
	return flag

#############################################
if __name__=='__main__':
		
	#Parse user options
	from optparse import OptionParser

	usage = None
	parser = OptionParser(usage=usage)

	#general options
	parser.add_option("-r", "--run-dic", default=None, type="string", help="Path to run_dic (containing all info about the runs")
	parser.add_option("-g", "--coin-group", default=None, type="string", help="Coincidence IFO group to collect LIB results for (i.e., H1L1)")
	parser.add_option("-m", "--coin-mode", default=None, type="string", help="Coincidence mode to collect LIB results for (i.e., 0lag, back, noise train, sig train)")

	#----------------------------------------------

	opts, args = parser.parse_args()

	run_dic = pickle.load(open(opts.run_dic))
	coin_group = opts.coin_group
	coin_mode = opts.coin_mode
	run_mode = run_dic['run mode']['line']
	
	#----------------------------------------------
	
	#MAIN

	#----------------------------------------------
	
	#Check if in online run mode
	if run_mode == 'Online':

		ifos = run_dic['coincidence'][coin_group]['ifos']
		segdir = run_dic['seg dir']
		
		if coin_mode == '0lag':		
			email_flag = run_dic['run mode']['email flag']
			if email_flag:
				email_addresses = run_dic['run mode']['email addresses']
			
			gdb_flag = run_dic['run mode']['gdb flag']
			if gdb_flag:
				gdb = GraceDb()
		
		elif coin_mode == 'sig_train':
			bindir = run_dic['config']['LIB bin dir']
			LIB_window = run_dic['prior ranges']['LIB window']

		#===============================================================

		#Initialize dictionary
		dictionary = {}

		#Find trigtimes and timeslides and add to dictionary
		if coin_mode == '0lag':		
			timeslide_array = np.genfromtxt('%s/PostProc/LIB_trigs/%s/%s/LIB_0lag_timeslides_%s.txt'%(segdir,coin_group, coin_mode, coin_group)).reshape(-1,len(ifos))
			trigtime_array = np.genfromtxt('%s/PostProc/LIB_trigs/%s/%s/LIB_0lag_times_%s.txt'%(segdir,coin_group, coin_mode, coin_group)).reshape(-1,1)
		elif coin_mode == 'sig_train':
			timeslide_array = np.genfromtxt('%s/PostProc_sig_train/LIB_trigs/%s/%s/LIB_0lag_timeslides_%s.txt'%(segdir,coin_group, coin_mode, coin_group)).reshape(-1,len(ifos))
			trigtime_array = np.genfromtxt('%s/PostProc_sig_train/LIB_trigs/%s/%s/LIB_0lag_times_%s.txt'%(segdir,coin_group, coin_mode, coin_group)).reshape(-1,1)
		elif coin_mode == 'back' or coin_mode == 'noise_train':
			timeslide_array = np.genfromtxt('%s/PostProc/LIB_trigs/%s/%s/LIB_ts_timeslides_%s.txt'%(segdir,coin_group, coin_mode, coin_group)).reshape(-1,len(ifos))
			trigtime_array = np.genfromtxt('%s/PostProc/LIB_trigs/%s/%s/LIB_ts_times_%s.txt'%(segdir,coin_group, coin_mode, coin_group)).reshape(-1,1)

		for event in xrange(len(trigtime_array)):
			dictionary[event] = {}
			dictionary[event]['gpstime'] = str(trigtime_array[event,0])
			dictionary[event]['timeslides'] = {}
			for i, ifo in enumerate(ifos):
				dictionary[event]['timeslides'][ifo] = str(timeslide_array[event,i])

		#Find BSNs and waveform params
		posterior_files = os.listdir("%s/LIB/%s/%s/posterior_samples/"%(segdir,coin_group,coin_mode))
		for f in posterior_files:
			if (len(f.split('_')[1].split('1')) == (len(ifos)+1)) and (f.split('.')[2] == 'dat_B'):
				#Initialize dictionary for event
				event = int(f.split('-')[1].split(".")[0])
				
				#Add basic info to dictionary
				dictionary[event]['instruments'] = ",".join(ifos)
				dictionary[event]['nevents'] = 1
				dictionary[event]['likelihood']= None
				
				#Add BSN to dictionary
				post_file = open("%s/LIB/%s/%s/posterior_samples/%s"%(segdir,coin_group,coin_mode,f), 'rt')
				for line in post_file:
					bsn = float(line.split()[0])
				dictionary[event]['BSN'] = bsn
				dictionary[event]['logBSN'] = np.log10(bsn)
				post_file.close()
				
				#First gather all waveform parameter samples
				with open("%s/LIB/%s/%s/posterior_samples/%s"%(segdir,coin_group,coin_mode,f.split('_B.txt')[0]),'rt') as pos_samp_file:
					pos_samps = list(pos_samp_file)
				
				freq_ind = np.nan
				qual_ind = np.nan
				hrss_ind = np.nan
				
				freq_samps = np.ones(len(pos_samps)-1)*np.nan
				qual_samps = np.ones(len(pos_samps)-1)*np.nan
				hrss_samps = np.ones(len(pos_samps)-1)*np.nan
				
				for iline,line in enumerate(pos_samps):
					#loop over all samples
					params = line.split()
					if iline == 0:
						#on header line, look for necessary indices
						for ipar, par in enumerate(params):
							if par == 'frequency':
								freq_ind = ipar
							elif par == 'quality':
								qual_ind = ipar
							elif par == 'loghrss':
								hrss_ind = ipar
					else:
						#now on sample lines
						freq_samps[iline-1] = float(params[freq_ind])
						qual_samps[iline-1] = float(params[qual_ind])
						hrss_samps[iline-1] = np.exp(float(params[hrss_ind]))
					
				#With samples, add necessary estimators to dictionaries
				dictionary[event]['frequency'] = {}
				dictionary[event]['frequency']['posterior mean'] = np.mean(freq_samps)
				dictionary[event]['frequency']['posterior median'] = np.median(freq_samps)
				
				dictionary[event]['quality'] = {}
				dictionary[event]['quality']['posterior mean'] = np.mean(qual_samps)
				dictionary[event]['quality']['posterior median'] = np.median(qual_samps)
				
				dictionary[event]['hrss'] = {}
				dictionary[event]['hrss']['posterior mean'] = np.mean(hrss_samps)
				dictionary[event]['hrss']['posterior median'] = np.median(hrss_samps)

		#Find BCIs		
		coherence_files = os.listdir("%s/LIB/%s/%s/coherence_test/"%(segdir,coin_group,coin_mode))
		for f in coherence_files:
				#Get event
				event = int(f.split('-')[1].split(".")[0])
				
				#Add BCI to dictionary
				coh_file = open("%s/LIB/%s/%s/coherence_test/%s"%(segdir,coin_group,coin_mode,f), 'rt')
				for line in coh_file:
					bci = float(line.split()[0])
				dictionary[event]['BCI'] = bci
				coh_file.close()

		#Find Omicron SNR
		event = 0

		if coin_mode == '0lag':
			try:
				trig_info_array = np.genfromtxt("%s/PostProc/LIB_trigs/%s/%s/%s"%(segdir,coin_group,coin_mode,'LIB_trigs_%s_tsnum0_.txt'%coin_group)).reshape((-1,4*(len(ifos)+1)))
				for line in trig_info_array:
					if np.absolute(float(dictionary[event]['gpstime']) - line[0]) <= 0.01:
						dictionary[event]['Omicron SNR'] = {}
						dictionary[event]['Omicron SNR']['Network'] = line[2]
						for i,ifo in enumerate(ifos):
							dictionary[event]['Omicron SNR'][ifo] = line[4*(i+1) + 2]
						event += 1
					else:
						raise ValueError("The event and trig time do not match up when finding Omicron SNR")
			except IOError:
				pass
		
		elif coin_mode == 'sig_train':
			try:
				trig_info_array = np.genfromtxt("%s/PostProc_sig_train/LIB_trigs/%s/%s/%s"%(segdir,coin_group,coin_mode,'LIB_trigs_%s_tsnum0_.txt'%coin_group)).reshape((-1,4*(len(ifos)+1)))
				for line in trig_info_array:
					if np.absolute(float(dictionary[event]['gpstime']) - line[0]) <= 0.01:
						dictionary[event]['Omicron SNR'] = {}
						dictionary[event]['Omicron SNR']['Network'] = line[2]
						for i,ifo in enumerate(ifos):
							dictionary[event]['Omicron SNR'][ifo] = line[4*(i+1) + 2]
						event += 1
					else:
						raise ValueError("The event and trig time do not match up when finding Omicron SNR")
			except IOError:
				pass
		
		elif coin_mode == 'back' or coin_mode == 'noise_train':
			if coin_mode == 'back':
				ts_name = 'back timeslides'
			elif coin_mode == 'noise_train':
				ts_name = 'training timeslides'
			for tshift_num in xrange(len(run_dic['coincidence'][coin_group][ts_name][ifos[0]])):
				try:
					trig_info_array = np.genfromtxt("%s/PostProc/LIB_trigs/%s/%s/LIB_trigs_%s_tsnum%s_.txt"%(segdir,coin_group,coin_mode,coin_group, tshift_num)).reshape((-1,4*(len(ifos)+1)))
					for line in trig_info_array:
						if np.absolute(float(dictionary[event]['gpstime']) - line[0]) <= 0.01:
							dictionary[event]['Omicron SNR'] = {}
							dictionary[event]['Omicron SNR']['Network'] = line[2]
							for i,ifo in enumerate(ifos):
								dictionary[event]['Omicron SNR'][ifo] = line[4*(i+1) + 2]
							event += 1
						else:
							raise ValueError("The event and trig time do not match up when finding Omicron SNR")
				except IOError:
					pass

		#Construct LLRT object for the set of events if dealing with 0lag runs
		if coin_mode == '0lag':
			#Get necessary LLRT parameters and save background info to runfiles
			FAR_thresh = run_dic['LLRT']['FAR thresh']
			back_dic_path = run_dic['LLRT'][coin_group]['back dic path']
			back_livetime_path = run_dic['LLRT'][coin_group]['back livetime']
			trials_factor = len(run_dic['search bins']['bin names'])
			
			if not os.path.exists("%s/runfiles/"%segdir):
				os.makedirs("%s/runfiles/"%segdir)
			os.system('cp %s %s/runfiles/'%(back_dic_path,segdir))
			os.system('cp %s %s/runfiles/'%(back_livetime_path,segdir))
			
			#Build calc_info dictionary
			calc_info = {}
			calc_info['interp method'] = 'Grid Linear'
			calc_info['extrap method'] = 'Grid Nearest'

			#Loop over search bins
			for search_bin in run_dic['search bins']['bin names']:
				#Build param_info dictionary and training dictionaries
				param_info = run_dic['LLRT']['param info'][search_bin]
				train_signal_data = {}
				train_noise_data = {}
				for param_group in param_info:
					#Get KDE results and copy them to runfiles directory
					signal_kde_coords = run_dic['LLRT'][coin_group][search_bin][param_group]['oLIB signal kde coords']
					signal_kde_values = run_dic['LLRT'][coin_group][search_bin][param_group]['oLIB signal kde values']
					noise_kde_coords = run_dic['LLRT'][coin_group][search_bin][param_group]['oLIB noise kde coords']
					noise_kde_values = run_dic['LLRT'][coin_group][search_bin][param_group]['oLIB noise kde values']

					os.system('cp %s %s/runfiles/'%(signal_kde_coords,segdir))
					os.system('cp %s %s/runfiles/'%(signal_kde_values,segdir))
					os.system('cp %s %s/runfiles/'%(noise_kde_coords,segdir))
					os.system('cp %s %s/runfiles/'%(noise_kde_values,segdir))

					#Load likelihood estimate for signal
					train_signal_data[param_group] = {}
					train_signal_data[param_group]['KDE'] = ([np.load(signal_kde_coords),np.load(signal_kde_values)])

					#Load likelihood estimate for noise
					train_noise_data[param_group] = {}
					train_noise_data[param_group]['KDE'] = ([np.load(noise_kde_coords),np.load(noise_kde_values)])

				#Build foreground_data dictionary
				logBSNs = np.ones(len(dictionary))*np.nan
				BCIs = np.ones(len(dictionary))*np.nan
				events = np.ones(len(dictionary))*np.nan

				for i,event in enumerate(dictionary):
					if check_parameter_space(dictionary[event],search_bin=search_bin,run_dic=run_dic) == True:
						dictionary[event]['search bin'] = search_bin
						logBSNs[i] = np.log10(dictionary[event]['BSN'])
						BCIs[i] = dictionary[event]['BCI']
						events[i] = event
					else:
						pass

				logBSNs = logBSNs[ logBSNs >= -np.inf ]
				BCIs = BCIs[ BCIs >= -np.inf ]
				events = events[ events >= -np.inf ]

				foreground_data = {}
				foreground_data['npoints'] = len(events)
				foreground_data['logBSN'] = {}
				foreground_data['logBSN']['data'] = np.transpose(np.array([logBSNs]))
				foreground_data['BCI'] = {}
				foreground_data['BCI']['data'] = np.transpose(np.array([BCIs]))

				#Build background_data dictionary
				try:
					float_back_livetime = float(np.genfromtxt(back_livetime_path))
				except IOError:
					float_back_livetime = np.nan
				back_dic = pickle.load(open(back_dic_path))
				back_coords = np.ones((len(back_dic),2))*np.nan

				for i,key in enumerate(back_dic):
					if check_parameter_space(back_dic[key],search_bin=search_bin,run_dic=run_dic) == True:
						back_coords[i,0] = np.log10(back_dic[key]['BSN'])
						back_coords[i,1] = back_dic[key]['BCI']
					else:
						pass

				back_coords = back_coords[ back_coords >= -np.inf ].reshape(-1,2)

				background_data = {}
				background_data['npoints'] = len(back_coords)
				background_data['logBSN'] = {}
				background_data['logBSN']['data'] = back_coords[:,0]
				background_data['BCI'] = {}
				background_data['BCI']['data'] = back_coords[:,1]

				#Initialize the LLRT object
				if foreground_data['npoints'] > 0:
					LLRT = LLRT_object_eagle.LLRT(calc_info=calc_info, param_info=param_info, train_signal_data=train_signal_data, train_noise_data=train_noise_data, foreground_data=foreground_data, background_data=background_data)

					#Calculate FAR for each foreground event wrt background events
					event_LLRs = LLRT.log_likelihood_ratios(groundtype='Foreground')
					for event,event_LLR in zip(events,event_LLRs):
						dictionary[event]['raw FAR'] = LLRT.calculate_FAR_of_thresh(threshold=event_LLR, livetime=float_back_livetime, groundtype='Background')
						dictionary[event]['trials factor'] = trials_factor
						dictionary[event]['FAR'] = dictionary[event]['raw FAR'] * trials_factor
					
						#Send email alert if exceed FAR threshold
						if (dictionary[event]['FAR'] <= FAR_thresh) and (email_flag):
							email_header = "oLIB 0-lag event found at %s with FAR of %s Hz"%(dictionary[event]['gpstime'],dictionary[event]['FAR'])
							if gdb_flag:
								email_body = "This oLIB event *should* be posted to GraceDB momentarily.\n\n"
							else:
								email_body = "This oLIB event *will not* to be posted to GraceDB because of the pipeline configuration.\n\n"
							email_body += "GPS time:  %s\n"%dictionary[event]['gpstime']
							email_body += "FAR [Hz]: %s\n"%dictionary[event]['FAR']
							email_body += "IFOs: %s\n"%",".join(ifos)
							email_body += "logBSN: %s\n"%np.log10(dictionary[event]['BSN'])
							email_body += "BCI: %s\n"%dictionary[event]['BCI']
							email_body += "Network SNR: %s\n"%dictionary[event]['Omicron SNR']['Network']
							email_body += "Mean f_0 [Hz]: %s\n"%dictionary[event]['frequency']['posterior mean']
							email_body += "Mean Q: %s\n"%dictionary[event]['quality']['posterior mean']
							email_body += "INJ flag: %s\n"%any([run_dic['data']['inj flags'][ifo] for ifo in ifos])
							email_body += "DQV flag: %s\n"%any([run_dic['data']['DQV flags'][ifo] for ifo in ifos])
							email_body += "Search bin: %s\n"%search_bin
							os.system('echo "%s" | mail -s "%s" %s'%(email_body,email_header," ".join(email_addresses)))
					
					
						#Upload events to GDB if exceed FAR threshold
						if (dictionary[event]['FAR'] <= FAR_thresh) and (gdb_flag):		
							#Save dictionary as json file
							dic_path = segdir+'/GDB/%s/%s.json'%(coin_group,'%s-%s'%(dictionary[event]['gpstime'],event))
							if not os.path.exists("%s/GDB/%s/"%(segdir,coin_group)):
								os.makedirs("%s/GDB/%s/"%(segdir,coin_group))
							with open(dic_path, 'wt') as fp:
								json.dump(dictionary[event], fp)
							
							#Upload dictionary to GraceDb
							response = gdb.createEvent('Test','LIB',dic_path, search='AllSky', filecontents=None) #gdb.createEvent('Burst','LIB',dic_path, search='AllSky', filecontents=None)
							
							#Parse GraceDb ID so that labels can be applied
							response = json.loads(response.read())
							gid = response["graceid"]
							
							#Mark GraceDb event as hardware injection if need be
							if any([run_dic['data']['inj flags'][ifo] for ifo in ifos]):
								gdb.writeLabel(gid, 'INJ')
			
							#Mark GraceDb event as data-quality veto if need be
							if any([run_dic['data']['DQV flags'][ifo] for ifo in ifos]):
								gdb.writeLabel(gid, 'DQV')

							#Mark that event has been uploaded to GDB
							dictionary[event]['GDB upload'] = True
		
		#If in signal training mode, match the LIB event with its injection 
		if coin_mode == 'sig_train':
			#find the times of the training injections
			inj_times = commands.getstatusoutput('%s/ligolw_print %s/training_injections/raw/*.xml -c "time_geocent_gps" -c "time_geocent_gps_ns" -d "."'%(bindir,segdir))[1].split()
			print "Inj times: ", inj_times

			#First mark all events as non-detections
			for event in dictionary:
				dictionary[event]['Training injection'] = False

			#Loop through time-sorted injections and events, doing coincidence
			inj_times = sorted(np.array(inj_times).astype(float))
			events = sorted(dictionary.keys())
			i_event_min = 0
			for inj_time in inj_times:
				#Iterate through events until within coincidence window or past the injection time
				while np.absolute(inj_time - float(dictionary[events[i_event_min]]['gpstime'])) > 0.5*LIB_window:
					if (float(dictionary[events[i_event_min]]['gpstime']) - inj_time) > 0.5*LIB_window:
						break
					elif (i_event_min + 1) >= len(events):
						break
					else:
						i_event_min += 1
				
				#LIB needs to have run over at least part of the injection for it to be considered found
				tmp_inj_dic = {}
				i_event = i_event_min
				while np.absolute(inj_time - float(dictionary[events[i_event]]['gpstime'])) <= 0.5*LIB_window:
					tmp_inj_dic[dictionary[events[i_event]]['Omicron SNR']['Network']] = events[i_event]
					if (i_event + 1) >= len(events):
						break
					else:
						i_event += 1
						
				#Choose the coincident injection with the highest network SNR
				if len(tmp_inj_dic) > 0:
					event_coin = tmp_inj_dic[max(tmp_inj_dic)]
					dictionary[event_coin]['Training injection'] = True
				
		#Save dictionary and mark that it is ready for cumulative collection
		trig_dic_path = '%s/results_dic/%s/%s/LIB_trigs_results_%s_%s.pkl'%(segdir,coin_group,coin_mode,coin_group,coin_mode)
		if not os.path.exists("%s/results_dic/%s/%s/"%(segdir,coin_group,coin_mode)):
			os.makedirs("%s/results_dic/%s/%s/"%(segdir,coin_group,coin_mode))
		pickle.dump(dictionary, open(trig_dic_path,'wt'))
		os.system('> %s/results_dic/%s/%s/results_dic_ready_for_collection.txt'%(segdir,coin_group,coin_mode))
		
	elif run_mode == 'Offline':
		pass
