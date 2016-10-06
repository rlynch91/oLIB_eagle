#!/usr/bin/python

import sys
sys.path.insert(1,'/home/ryan.lynch/numpy/numpy-1.8.2-INSTALL/lib64/python2.7/site-packages')
import numpy as np
import pickle
import LLRT_object_eagle
import os

#############################################
#Define Functions

###
def check_parameter_space(dic_entry, search_bin, train_details_dic):
	q_min = train_details_dic['search bins'][search_bin]['low quality cut']
	q_max = train_details_dic['search bins'][search_bin]['high quality cut']
	f_min = train_details_dic['search bins'][search_bin]['low freq cut']
	f_max = train_details_dic['search bins'][search_bin]['high freq cut']
	BCI_min = train_details_dic['search bins'][search_bin]['low BCI cut']
	BCI_max = train_details_dic['search bins'][search_bin]['high BCI cut']
	logBSN_min = train_details_dic['search bins'][search_bin]['low logBSN cut']
	logBSN_max = train_details_dic['search bins'][search_bin]['high logBSN cut']
	
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

	parser.add_option("-r", "--run-dic", default=None, type="string", help="Path to run_dic (containing all info about the runs)")
	parser.add_option("-g", "--new-gps-day", default=None, type="int", help="GPS day that the new day covers")
	parser.add_option("-i", "--ifo-group", default=None, type="string", help="IFO group to update background for (i.e., H1L1)")
	parser.add_option("-b", "--search-bin", default=None, type="string", help="Name of search bin for which to train")

	#-----------------------------------------------------------------------

	opts, args = parser.parse_args()

	run_dic = pickle.load(open(opts.run_dic))
	new_gps_day = opts.new_gps_day
	group = opts.ifo_group
	search_bin = opts.search_bin 

	#=======================================================================
	
	####################################
	# Initialize the variables we need #
	####################################
	outdir = '%s/%s/'%(run_dic['collection and retraining'][search_bin]['retrain dir'],group)
	if not os.path.exists(outdir):
		os.makedirs(outdir)
	max_signal_size = run_dic['collection and retraining']['max sig train size']
	max_noise_size = run_dic['collection and retraining']['max noise train size']
	collectdir = run_dic['collection and retraining']['collect dir']
	
	new_signal_dic_path = '%s/%s/%s/%s_%s_%s_results.pkl'%(collectdir,'sig_train',group,new_gps_day,'sig_train',group)
	new_noise_dic_path = '%s/%s/%s/%s_%s_%s_results.pkl'%(collectdir,'noise_train',group,new_gps_day,'noise_train',group)
	if os.path.isfile(new_signal_dic_path) and os.path.isfile(new_noise_dic_path):
		new_signal_dic = pickle.load(open(new_signal_dic_path))
		new_noise_dic = pickle.load(open(new_noise_dic_path))
	else:
		new_signal_dic = {}
		new_noise_dic = {}

	old_signal_dic_path = '%s/Signal_training_dictionary.pkl'%outdir
	old_noise_dic_path = '%s/Noise_training_dictionary.pkl'%outdir
	if os.path.isfile(old_signal_dic_path) and os.path.isfile(old_noise_dic_path):
		old_signal_dic = pickle.load(open(old_signal_dic_path))
		old_noise_dic = pickle.load(open(old_noise_dic_path))
		os.system('cp %s %s/Signal_training_dictionary_old.pkl'%(old_signal_dic_path,outdir))
		os.system('cp %s %s/Noise_training_dictionary_old.pkl'%(old_noise_dic_path,outdir))
	else:
		old_signal_dic = {}
		old_noise_dic = {}

#???NEED TO LOOP OVER SEARCH BIN PARAMETERS, HERE AND FOR ACTUAL RETRAINING???
	old_signal_bands_path = '%s/%s_Signal_log_KDE_bandwidths.npy'%(outdir,run_dic['LLRT']['param info'][search_bin].keys()???)
	old_noise_bands_path = '%s/%s_Noise_log_KDE_bandwidths.npy'%(outdir,run_dic['LLRT']['param info'][search_bin].keys()???)
	if os.path.isfile(old_signal_bands_path) and os.path.isfile(old_noise_bands_path):
		old_signal_bands = np.load(old_signal_bands_path)
		old_noise_bands = np.load(old_noise_bands_path)
		os.system('cp %s %s/%s_Signal_log_KDE_bandwidths_old.npy'%(old_signal_bands_path,outdir,run_dic['LLRT']['param info'][search_bin].keys()???))
		os.system('cp %s %s/%s_Noise_log_KDE_bandwidths_old.npy'%(old_noise_bands_path,outdir,run_dic['LLRT']['param info'][search_bin].keys()???))
	else:
		old_signal_bands = np.ones(len(run_dic['LLRT']['param info'][search_bin][???]['param names'])*np.nan
		old_noise_bands = np.ones(len(run_dic['LLRT']['param info'][search_bin][???]['param names']))*np.nan

	#IN SAME LOOP, MOVE OLD KDE FILES IF THEY EXIST

#???	
	
	#################################
	# Copy old data to backup files #
	#################################
	os.system('cp %s/%s_Noise_log_KDE_coords.npy %s/%s_Noise_log_KDE_coords_old.npy'%(outdir,train_details_dic['param info'][search_bin].keys()[0],outdir,train_details_dic['param info'][search_bin].keys()[0]))
	os.system('cp %s/%s_Noise_log_KDE_values.npy %s/%s_Noise_log_KDE_values_old.npy'%(outdir,train_details_dic['param info'][search_bin].keys()[0],outdir,train_details_dic['param info'][search_bin].keys()[0]))
	os.system('cp %s/%s_Signal_log_KDE_coords.npy %s/%s_Signal_log_KDE_coords_old.npy'%(outdir,train_details_dic['param info'][search_bin].keys()[0],outdir,train_details_dic['param info'][search_bin].keys()[0]))
	os.system('cp %s/%s_Signal_log_KDE_values.npy %s/%s_Signal_log_KDE_values_old.npy'%(outdir,train_details_dic['param info'][search_bin].keys()[0],outdir,train_details_dic['param info'][search_bin].keys()[0]))
	os.system('cp %s %s/%s_Noise_log_KDE_bandwidths_old.npy'%(opts.old_noise_bands,outdir,train_details_dic['param info'][search_bin].keys()[0]))
	os.system('cp %s %s/%s_Signal_log_KDE_bandwidths_old.npy'%(opts.old_sig_bands,outdir,train_details_dic['param info'][search_bin].keys()[0]))

	################################
	# Update training dictionaries #
	################################

	#Create updated dictionary
	updated_signal_dic = {}
	updated_noise_dic = {}
	event_signal = 0
	event_noise = 0
	
	###SIGNAL###
	
	#First add the new signal training events
	if event_signal < max_signal_size:
		for key in new_signal_dic:
			if check_parameter_space(dic_entry=new_signal_dic[key], search_bin=search_bin, train_details_dic=train_details_dic) and new_signal_dic[key]['Training injection']:
				#Event should be used in training
				updated_signal_dic[event_signal] = new_signal_dic[key]
				
				#Update the number of events currently in training dictionary
				event_signal += 1
				if event_signal >= max_signal_size:
					break
	
	#Then add the old signal training events
	if event_signal < max_signal_size:
		for key in old_signal_dic:
			if check_parameter_space(dic_entry=old_signal_dic[key], search_bin=search_bin, train_details_dic=train_details_dic) and old_signal_dic[key]['Training injection']:
				#Event should be used in training
				updated_signal_dic[event_signal] = old_signal_dic[key]
				
				#Update the number of events currently in training dictionary
				event_signal += 1
				if event_signal >= max_signal_size:
					break
	
	###NOISE###
	#First add the new noise training events
	if event_noise < max_noise_size:
		for key in new_noise_dic:
			if check_parameter_space(dic_entry=new_noise_dic[key], search_bin=search_bin, train_details_dic=train_details_dic):
				#Event should be used in training
				updated_noise_dic[event_noise] = new_noise_dic[key]
				
				#Update the number of events currently in training dictionary
				event_noise += 1
				if event_noise >= max_noise_size:
					break
	
	#Then add the old noise training events
	if event_noise < max_noise_size:
		for key in old_noise_dic:
			if check_parameter_space(dic_entry=old_noise_dic[key], search_bin=search_bin, train_details_dic=train_details_dic):
				#Event should be used in training
				updated_noise_dic[event_noise] = old_noise_dic[key]
				
				#Update the number of events currently in training dictionary
				event_noise += 1
				if event_noise >= max_noise_size:
					break

	#Save updated dictionary
	pickle.dump(updated_signal_dic,open('%s/Signal_training_dictionary_new.pkl'%(outdir),'wt'))
	pickle.dump(updated_noise_dic,open('%s/Noise_training_dictionary_new.pkl'%(outdir),'wt'))

	#-----------------------------------------------------------------------

	#######################
	# Retrain likelihoods #
	#######################

	#Start building LLRT dictionaries
	calc_info = train_details_dic['calc info']
	param_info = train_details_dic['param info'][search_bin]
	
	optimize_signal_training = train_details_dic['optimize signal training'][search_bin]
	optimize_signal_training[optimize_signal_training.keys()[0]]['optimization initial coords'] = old_signal_bands
	
	optimize_noise_training = train_details_dic['optimize noise training'][search_bin]
	optimize_noise_training[optimize_noise_training.keys()[0]]['optimization initial coords'] = old_noise_bands

	#Collect all signal training coordinates from dictionaries and put in arrays
	sig_logBSN = np.ones(len(updated_signal_dic))*np.nan
	sig_BCI = np.ones(len(updated_signal_dic))*np.nan
	for i, key in enumerate(updated_signal_dic):
		sig_logBSN[i] = np.log10(updated_signal_dic[key]['BSN'])
		sig_BCI[i] = updated_signal_dic[key]['BCI']
		
	sig_logBSN = sig_logBSN[ sig_logBSN >= -np.inf ]
	sig_BCI = sig_BCI[ sig_BCI >= -np.inf ]

	train_signal_data = train_details_dic['train signal data'][search_bin]
	train_signal_data['logBSN']['data'] = np.transpose(np.array([sig_logBSN]))
	train_signal_data['BCI']['data'] = np.transpose(np.array([sig_BCI]))

	#Collect all noise training coordinates from dictionaries and put in arrays
	noise_logBSN = np.ones(len(updated_noise_dic))*np.nan
	noise_BCI = np.ones(len(updated_noise_dic))*np.nan
	for i, key in enumerate(updated_noise_dic):
		noise_logBSN[i] = np.log10(updated_noise_dic[key]['BSN'])
		noise_BCI[i] = updated_noise_dic[key]['BCI']
	
	noise_logBSN = noise_logBSN[ noise_logBSN >= -np.inf ]
	noise_BCI = noise_BCI[ noise_BCI >= -np.inf ]

	train_noise_data = train_details_dic['train noise data'][search_bin]
	train_noise_data['logBSN']['data'] = np.transpose(np.array([noise_logBSN]))
	train_noise_data['BCI']['data'] = np.transpose(np.array([noise_BCI]))

	#Initialize LLRT object (which launches likelihood training), and then save the trained likelihoods to temporary files
	LLRT = LLRT_object_eagle.LLRT(calc_info=calc_info, param_info=param_info, train_signal_data=train_signal_data, train_noise_data=train_noise_data, foreground_data=None, background_data=None, optimize_signal_training=optimize_signal_training, optimize_noise_training=optimize_noise_training)
	LLRT.save_all_KDE(outdir,label='new')
	LLRT.save_all_bandwidths(outdir,label='new')

	#################################
	# Move new data to proper files #
	#################################
	os.system('mv %s/%s_Noise_log_KDE_coords_new.npy %s/%s_Noise_log_KDE_coords.npy'%(outdir,train_details_dic['param info'][search_bin].keys()[0],outdir,train_details_dic['param info'][search_bin].keys()[0]))
	os.system('mv %s/%s_Noise_log_KDE_values_new.npy %s/%s_Noise_log_KDE_values.npy'%(outdir,train_details_dic['param info'][search_bin].keys()[0],outdir,train_details_dic['param info'][search_bin].keys()[0]))
	os.system('mv %s/%s_Signal_log_KDE_coords_new.npy %s/%s_Signal_log_KDE_coords.npy'%(outdir,train_details_dic['param info'][search_bin].keys()[0],outdir,train_details_dic['param info'][search_bin].keys()[0]))
	os.system('mv %s/%s_Signal_log_KDE_values_new.npy %s/%s_Signal_log_KDE_values.npy'%(outdir,train_details_dic['param info'][search_bin].keys()[0],outdir,train_details_dic['param info'][search_bin].keys()[0]))
	os.system('mv %s/%s_Noise_log_KDE_bandwidths_new.npy %s/%s_Noise_log_KDE_bandwidths.npy'%(outdir,train_details_dic['param info'][search_bin].keys()[0],outdir,train_details_dic['param info'][search_bin].keys()[0]))
	os.system('mv %s/%s_Signal_log_KDE_bandwidths_new.npy %s/%s_Signal_log_KDE_bandwidths.npy'%(outdir,train_details_dic['param info'][search_bin].keys()[0],outdir,train_details_dic['param info'][search_bin].keys()[0]))
	os.system('mv %s/Noise_training_dictionary_new.pkl %s/Noise_training_dictionary.pkl'%(outdir,outdir))
	os.system('mv %s/Signal_training_dictionary_new.pkl %s/Signal_training_dictionary.pkl'%(outdir,outdir))
	
