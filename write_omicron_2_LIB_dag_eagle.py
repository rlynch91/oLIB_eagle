#!/usr/bin/python

import sys
sys.path.insert(1,'/home/ryan.lynch/numpy/numpy-1.8.2-INSTALL/lib64/python2.7/site-packages')
import numpy as np
import os
import pickle

#=======================================================================

###
def executable(run_dic):
	"""
	"""
	if run_dic['run mode']['line'] == 'Online':
		
		#initialize the variables we need
		ifos_all = np.array(run_dic['ifos']['names'])
		ifos = []
		for ifo in ifos_all:
			if run_dic['data']['success flags'][ifo]:
				ifos += [ifo]
		segdir=run_dic['seg dir']
		infodir=run_dic['config']['info dir']
		bindir=run_dic['config']['LIB bin dir']

		actual_start = run_dic['times']['actual start']
		stride = run_dic['config']['stride']
		overlap = run_dic['config']['overlap']
		LIB_flag = run_dic['run mode']['LIB flag']
		
		train_runmode = run_dic['run mode']['train runmode']
		min_hrss = run_dic['prior ranges']['min hrss']
		max_hrss = run_dic['prior ranges']['max hrss']
		min_freq = run_dic['prior ranges']['min freq']
		max_freq = run_dic['prior ranges']['max freq']
		min_quality = run_dic['prior ranges']['min quality']
		max_quality = run_dic['prior ranges']['max quality']
		sample_freq = run_dic['config']['sample freq']
		osnr_thresh = run_dic['config']['oSNR thresh']
		LIB_window = run_dic['prior ranges']['LIB window']
		LIB_stride = run_dic['prior ranges']['LIB stride']
		sample_freq = run_dic['config']['sample freq']

		seg_files = {}
		cache_files = {}
		channel_names = {}
		channel_types = {}
		for ifo in ifos:
			seg_files[ifo] = run_dic['data']['seg files'][ifo]
			cache_files[ifo] = run_dic['data']['cache files'][ifo]
			channel_names[ifo] = run_dic['ifos'][ifo]['channel name']
			channel_types[ifo] = run_dic['ifos'][ifo]['channel type']
			
		if train_runmode == 'Train':
			sig_train_cache_files = {}
			for ifo in ifos:
				sig_train_cache_files[ifo] = run_dic['data']['signal train cache files'][ifo]

		#############################################

		##################
		### Initialize ###
		##################

		#make log directory
		if not os.path.exists("%s/log/"%segdir):
			os.makedirs("%s/log/"%segdir)
			
		#make dag directory
		if not os.path.exists("%s/dag/"%segdir):
			os.makedirs("%s/dag/"%segdir)
			
		#make runfiles directory
		if not os.path.exists("%s/runfiles/"%segdir):
			os.makedirs("%s/runfiles/"%segdir)

		#open dag file
		dagfile = open("%s/dag/2ndPipeDag_%s_%s_%s.dag"%(segdir,"".join(ifos_all),actual_start,stride-overlap),'wt')

		#initialize job number
		job = 0

		#############################################
		### Write DAG to run omicron for each ifo ###
		#############################################

		omicron_jobs=[]

		#Copy omicron sub file to segdir
		os.system('sed -e "s|SEGDIR|%s|g" %s/omicron_eagle.sub > %s/runfiles/omicron_eagle.sub'%(segdir,infodir,segdir))

		#Loop over all ifos
		for ifo in ifos:
			
			#make raw directory
			if not os.path.exists("%s/raw/%s"%(segdir,ifo)):
				os.makedirs("%s/raw/%s"%(segdir,ifo))
			
			#replace all necessary variables in params file
			os.system('sed -e "s|IFO|%s|g" -e "s|FRAMECACHE|%s|g" -e "s|CHNAME|%s|g" -e "s|SAMPFREQ|%s|g" -e "s|OLAP|%s|g" -e "s|STRIDE|%s|g" -e "s|RAWDIR|%s|g" -e "s|MINFREQ|%s|g" -e "s|MAXFREQ|%s|g" -e "s|THRESHSNR|%s|g" %s/omicron_params_eagle.txt > %s/runfiles/omicron_params_%s_eagle.txt'%(ifo, cache_files[ifo], channel_names[ifo], sample_freq, overlap, stride, segdir+'/raw/'+ifo, min_freq, max_freq, osnr_thresh, infodir, segdir, ifo))

			#write JOB
			dagfile.write('JOB %s %s/runfiles/omicron_eagle.sub\n'%(job,segdir))
			#write VARS
			dagfile.write('VARS %s macroid="omicron-%s-%s" macroarguments="%s %s"\n'%(job, ifo, job, seg_files[ifo], segdir+'/runfiles/omicron_params_%s_eagle.txt'%ifo))
			#write RETRY
			dagfile.write('RETRY %s 0\n\n'%job)
			
			#Record omicron job numbers
			omicron_jobs += [job]
			
			#Done with job
			job += 1

		##################################################################
		### Write DAG to run omicron signal training jobs for each ifo ###
		##################################################################
		
		omicron_sig_train_jobs=[]
		
		#Check if in training mode
		if train_runmode == 'Train':
			
			#Loop over all ifos
			for ifo in ifos:
				
				#make raw directory
				if not os.path.exists("%s/raw_sig_train/%s"%(segdir,ifo)):
					os.makedirs("%s/raw_sig_train/%s"%(segdir,ifo))

				#replace all necessary variables in params file
				os.system('sed -e "s|IFO|%s|g" -e "s|FRAMECACHE|%s|g" -e "s|CHNAME|%s|g" -e "s|SAMPFREQ|%s|g" -e "s|OLAP|%s|g" -e "s|STRIDE|%s|g" -e "s|RAWDIR|%s|g" -e "s|MINFREQ|%s|g" -e "s|MAXFREQ|%s|g" -e "s|THRESHSNR|%s|g" -e "s|//INJECTION|INJECTION|g" %s/omicron_params_eagle.txt > %s/runfiles/omicron_sig_train_params_%s_eagle.txt'%(ifo, sig_train_cache_files[ifo], channel_names[ifo], sample_freq, overlap, stride, segdir+'/raw_sig_train/'+ifo, min_freq, max_freq, osnr_thresh, infodir, segdir, ifo))

				#write JOB
				dagfile.write('JOB %s %s/runfiles/omicron_eagle.sub\n'%(job,segdir))
				#write VARS
				dagfile.write('VARS %s macroid="omicron_sig_train-%s-%s" macroarguments="%s %s"\n'%(job, ifo, job, seg_files[ifo], segdir+'/runfiles/omicron_sig_train_params_%s_eagle.txt'%ifo))
				#write RETRY
				dagfile.write('RETRY %s 0\n\n'%job)
				
				#Record omicron job numbers
				omicron_sig_train_jobs += [job]
				
				#Done with job
				job += 1

		####################################
		### Write DAG to run omicron2LIB ###
		####################################

		omicron2LIB_jobs = []

		#Copy omicron2LIB sub file to segdir
		os.system('sed -e "s|SEGDIR|%s|g" -e "s|INFODIR|%s|g" %s/omicron2LIB_eagle.sub > %s/runfiles/omicron2LIB_eagle.sub'%(segdir,infodir,infodir,segdir))

		#Create PostProc folder
		if not os.path.exists("%s/PostProc/"%segdir):
			os.makedirs("%s/PostProc/"%segdir)

		#Create vetoes folder with empty veto file
		if not os.path.exists("%s/vetoes/"%segdir):
			os.makedirs("%s/vetoes/"%segdir)
		os.system('> %s/vetoes/null_vetoes.txt'%segdir)
		run_dic['vetoes'] = {}
		for ifo in ifos:
			run_dic['vetoes'][ifo] = '%s/vetoes/null_vetoes.txt'%segdir
			
		#Write JOB
		dagfile.write('JOB %s %s/runfiles/omicron2LIB_eagle.sub\n'%(job,segdir))
		#Write VARS
		dagfile.write('VARS %s macroid="omicron2LIB-%s" macroarguments="-r %s"\n'%(job,job,'%s/run_dic/run_dic_%s_%s.pkl'%(segdir,actual_start,stride-overlap)))
		#Write RETRY
		dagfile.write('RETRY %s 0\n\n'%job)

		#Record omicron2LIB job number
		omicron2LIB_jobs += [job]

		#Done with job
		job += 1

		########################################################
		### Write DAG to run omicron2LIB for signal training ###
		########################################################

		omicron2LIB_sig_train_jobs = []
		
		#Check if in training mode
		if train_runmode == 'Train':

			#Create PostProc folder
			if not os.path.exists("%s/PostProc_sig_train/"%segdir):
				os.makedirs("%s/PostProc_sig_train/"%segdir)
			
			#Write JOB
			dagfile.write('JOB %s %s/runfiles/omicron2LIB_eagle.sub\n'%(job,segdir))
			#Write VARS
			dagfile.write('VARS %s macroid="omicron2LIB_sig_train-%s" macroarguments="-r %s --sig-train"\n'%(job,job,'%s/run_dic/run_dic_%s_%s.pkl'%(segdir,actual_start,stride-overlap)))
			#Write RETRY
			dagfile.write('RETRY %s 0\n\n'%job)

			#Record omicron2LIB job number
			omicron2LIB_sig_train_jobs += [job]

			#Done with job
			job += 1

		####################################
		### Check if supposed to run LIB ###
		####################################

		if LIB_flag:

			lalinference_pipe_jobs = []
			LIB_runs_jobs = []
			Bayes2FAR_jobs = []
			
			lalinference_pipe_sig_train_jobs = []
			LIB_runs_sig_train_jobs = []
			Bayes2FAR_sig_train_jobs = []

			#Copy lalinference_pipe sub file to segdir
			os.system('sed -e "s|SEGDIR|%s|g" -e "s|INFODIR|%s|g" %s/lalinference_pipe_eagle.sub > %s/runfiles/lalinference_pipe_eagle.sub'%(segdir,infodir,infodir,segdir))
			
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
				
				#If all ifos in coincidence group are analyzable, then write to dag
				if coin_flag:

					LIB_mode_options = [('analyze 0lag','0lag'), ('analyze back','back'), ('analyze noise training','noise_train')]
					if train_runmode == 'Train':
						LIB_mode_options += [('analyze signal training','sig_train')]

					for analyze_tag,mode_label in LIB_mode_options:
						
						if run_dic['coincidence'][key][analyze_tag] == True:
							
							##########################################
							### Write DAG to run lalinference_pipe ###
							##########################################

							#Create LIB folder for this coincidence group
							if not os.path.exists("%s/LIB/%s/%s/"%(segdir, key, mode_label)):
								os.makedirs("%s/LIB/%s/%s/"%(segdir, key, mode_label))

							#Get necessary info for this coincidence group
							tmp_ifos = run_dic['coincidence'][key]['ifos']
							tmp_channel_names = {}
							tmp_channel_types = {}
							tmp_freqs_low = {}
							for ifo in tmp_ifos:
								tmp_channel_names[ifo] = "%s:%s"%(ifo,channel_names[ifo])
								tmp_channel_types[ifo] =  channel_types[ifo]
								tmp_freqs_low[ifo] = int(min_freq)

							#replace all necessary fields in LIB_runs_eagle.ini file
							sed_string = 'sed -e "s|IFOSCOMMA|%s|g" -e "s|SEGDIR|%s|g" -e "s|BINDIR|%s|g"'%(tmp_ifos,segdir,bindir)
							sed_string += ' -e "s|CHANNELTYPES|%s|g" -e "s|CHANNELNAMES|%s|g" -e "s|SAMPFREQ|%s|g"'%(tmp_channel_types,tmp_channel_names,sample_freq)
							sed_string += ' -e "s|MINHRSS|%s|g" -e "s|MAXHRSS|%s|g" -e "s|MINQUALITY|%s|g" -e "s|MAXQUALITY|%s|g" -e "s|MINFREQ|%s|g" -e "s|MAXFREQ|%s|g"'%(np.log(min_hrss),np.log(max_hrss),min_quality,max_quality,min_freq,max_freq)
							sed_string += ' -e "s|LIBWINDOW|%s|g" -e "s|LIBSTRIDE|%s|g" -e "s|COINGROUP|%s|g" -e "s|COINMODE|%s|g" -e "s|FREQSLOW|%s|g"'%(LIB_window,LIB_stride,key,mode_label,tmp_freqs_low)
							
							if mode_label == '0lag' or mode_label == 'sig_train':
								sed_string += ' -e "s|LAG|0lag|g"'
							else:
								sed_string += ' -e "s|LAG|ts|g"'
							
							if mode_label == 'sig_train':
								tmp_mdc_channels = {}
								tmp_mdc_caches = {}
								for ifo in tmp_ifos:
									tmp_mdc_channels[ifo] = "%s:Science"%ifo
									tmp_mdc_caches[ifo] = run_dic['data']['signal train cache files'][ifo]
								
								sed_string += ' -e "s|MDCCHANNELS|%s|g" -e "s|MDCCACHES|%s|g" -e "s|#mdc|mdc|g" -e "s|#MDC|MDC|g" -e "s|PostProc|PostProc_sig_train|g"'%(tmp_mdc_channels,tmp_mdc_caches)
								
							sed_string += ' %s/LIB_runs_eagle.ini > %s/runfiles/LIB_%s_%s_runs_eagle.ini'%(infodir,segdir,key,mode_label)

							os.system(sed_string)

							#Write JOB
							dagfile.write('JOB %s %s/runfiles/lalinference_pipe_eagle.sub\n'%(job,segdir))
							#Write VARS
							if mode_label == '0lag':
								dagfile.write('VARS %s macroid="lalinference_pipe_%s-%s" macroarguments="%s -r %s -p %s/log/ -g %s/PostProc/LIB_trigs/%s/%s/LIB_0lag_times_%s.txt --segdir %s --infodir %s --coin-group %s --coin-mode %s"\n'%(job,mode_label,job,segdir+'/runfiles/LIB_%s_%s_runs_eagle.ini'%(key,mode_label),segdir+'/LIB/%s/%s/'%(key,mode_label),segdir,segdir,key,mode_label,key,segdir,infodir,key,mode_label))
							elif mode_label == 'sig_train':
								dagfile.write('VARS %s macroid="lalinference_pipe_%s-%s" macroarguments="%s -r %s -p %s/log/ -g %s/PostProc_sig_train/LIB_trigs/%s/%s/LIB_0lag_times_%s.txt --segdir %s --infodir %s --coin-group %s --coin-mode %s"\n'%(job,mode_label,job,segdir+'/runfiles/LIB_%s_%s_runs_eagle.ini'%(key,mode_label),segdir+'/LIB/%s/%s'%(key,mode_label),segdir,segdir,key,mode_label,key,segdir,infodir,key,mode_label))
							else:
								dagfile.write('VARS %s macroid="lalinference_pipe_%s-%s" macroarguments="%s -r %s -p %s/log/ -g %s/PostProc/LIB_trigs/%s/%s/LIB_ts_times_%s.txt --segdir %s --infodir %s --coin-group %s --coin-mode %s"\n'%(job,mode_label,job,segdir+'/runfiles/LIB_%s_%s_runs_eagle.ini'%(key,mode_label),segdir+'/LIB/%s/%s/'%(key,mode_label),segdir,segdir,key,mode_label,key,segdir,infodir,key,mode_label))
							#Write RETRY
							dagfile.write('RETRY %s 0\n\n'%job)

							#Record lalinference_pipe job number
							if mode_label != 'sig_train':
								lalinference_pipe_jobs += [job]
							else:
								lalinference_pipe_sig_train_jobs += [job]

							#Done with job
							job += 1
							
							##########################################
							### Write DAG to point to LIB_runs dag ###
							##########################################

							#Write SUBDAG EXTERNAL
							dagfile.write('SUBDAG EXTERNAL %s %s/LIB/%s/%s/LIB_runs.dag\n'%(job,segdir,key,mode_label))
							#Write RETRY
							dagfile.write('RETRY %s 0\n\n'%job)

							#Record LIB_runs job number
							if mode_label != 'sig_train':
								LIB_runs_jobs += [job]
							else:
								LIB_runs_sig_train_jobs += [job]

							#Done with job
							job += 1
							
							############################################
							### Write DAG to run Bayes_factors_2_FAR ###
							############################################
							
							#Create GraceDb folder
							if not os.path.exists("%s/GDB/"%segdir):
								os.makedirs("%s/GDB/"%segdir)

							#Copy Bayes2FAR sub file to segdir
							os.system('sed -e "s|SEGDIR|%s|g" -e "s|INFODIR|%s|g" %s/Bayes2FAR_eagle.sub > %s/runfiles/Bayes2FAR_eagle_%s_%s.sub'%(segdir,infodir,infodir,segdir,key,mode_label))

							#Write JOB
							dagfile.write('JOB %s %s/runfiles/Bayes2FAR_eagle_%s_%s.sub\n'%(job,segdir,key,mode_label))
							#Write VARS
							dagfile.write('VARS %s macroid="Bayes2FAR_%s-%s" macroarguments="-r %s -g %s -m %s"\n'%(job,mode_label,job,'%s/run_dic/run_dic_%s_%s.pkl'%(segdir,actual_start,stride-overlap),key,mode_label))
							#Write RETRY
							dagfile.write('RETRY %s 0\n\n'%job)

							#Record lalinference_pipe job number
							if mode_label != 'sig_train':
								Bayes2FAR_jobs += [job]
							else:
								Bayes2FAR_sig_train_jobs += [job]

							#Done with job
							job += 1
		
		########################################
		### Write DAG to zip and tar results ###
		########################################
		zip_and_tar_jobs = []

		#Copy zip_and_tar sub file to segdir
		if not os.path.exists("%s/tarfiles/"%segdir):
			os.makedirs("%s/tarfiles/"%segdir)
		os.system('sed -e "s|SEGDIR|%s|g" -e "s|INFODIR|%s|g" %s/zip_and_tar_results_eagle.sub > %s/tarfiles/zip_and_tar_results_eagle.sub'%(segdir,infodir,infodir,segdir))

		#Write JOB
		dagfile.write('JOB %s %s/tarfiles/zip_and_tar_results_eagle.sub\n'%(job,segdir))
		#Write VARS
		dagfile.write('VARS %s macroid="zip_and_tar-%s" macroarguments="-r %s"\n'%(job,job,'%s/run_dic/run_dic_%s_%s.pkl'%(segdir,actual_start,stride-overlap)))
		#Write RETRY
		dagfile.write('RETRY %s 0\n\n'%job)

		#Record zip_and_tar job number
		zip_and_tar_jobs += [job]

		#Done with job
		job += 1
				
		####################################
		### Write parent-child relations ###
		####################################

		#make each omicron job a parent to each omicron2LIB job
		for parent in omicron_jobs:
			for child in omicron2LIB_jobs:
				dagfile.write('PARENT %s CHILD %s\n'%(parent,child))

		#make each omicron_sig_train job a parent to each omicron2LIB_sig_train job
		for parent in omicron_sig_train_jobs:
			for child in omicron2LIB_sig_train_jobs:
				dagfile.write('PARENT %s CHILD %s\n'%(parent,child))

		#check if LIB was run
		if LIB_flag:

			#make each omicron2LIB job a parent to each lalinference_pipe job and each zip_and_tar job
			for parent in omicron2LIB_jobs:
				for child in lalinference_pipe_jobs:
					dagfile.write('PARENT %s CHILD %s\n'%(parent,child))
				for child in zip_and_tar_jobs:
					dagfile.write('PARENT %s CHILD %s\n'%(parent,child))
			
			#make each omicron2LIB_sig_train job a parent to each lalinference_pipe_sig_train job and each zip_and_tar job
			for parent in omicron2LIB_sig_train_jobs:
				for child in lalinference_pipe_sig_train_jobs:
					dagfile.write('PARENT %s CHILD %s\n'%(parent,child))
				for child in zip_and_tar_jobs:
					dagfile.write('PARENT %s CHILD %s\n'%(parent,child))
				
			#make lalinference_pipe jobs parents to LIB_runs jobs, and LIB_runs jobs parents to Bayes2FAR jobs for each run mode 
			for i in xrange(len(lalinference_pipe_jobs)):
				dagfile.write('PARENT %s CHILD %s\n'%(lalinference_pipe_jobs[i],LIB_runs_jobs[i]))
				dagfile.write('PARENT %s CHILD %s\n'%(LIB_runs_jobs[i],Bayes2FAR_jobs[i]))

			#make lalinference_pipe_sig_train jobs parents to LIB_runs_sig_train jobs, and LIB_runs_sig_train jobs parents to Bayes2FAR_sig_train jobs 
			for i in xrange(len(lalinference_pipe_sig_train_jobs)):
				dagfile.write('PARENT %s CHILD %s\n'%(lalinference_pipe_sig_train_jobs[i],LIB_runs_sig_train_jobs[i]))
				dagfile.write('PARENT %s CHILD %s\n'%(LIB_runs_sig_train_jobs[i],Bayes2FAR_sig_train_jobs[i]))					
		
			#make each Bayes2FAR job a parent to each zip_and_tar job
			for parent in Bayes2FAR_jobs:
				for child in zip_and_tar_jobs:
					dagfile.write('PARENT %s CHILD %s\n'%(parent,child))
					
			#make each Bayes2FAR_sig_train job a parent to each zip_and_tar job
			for parent in Bayes2FAR_sig_train_jobs:
				for child in zip_and_tar_jobs:
					dagfile.write('PARENT %s CHILD %s\n'%(parent,child))
		
		else:
			
			#make each omicron2LIB job a parent to each zip_and_tar job
			for parent in omicron2LIB_jobs:
				for child in zip_and_tar_jobs:
					dagfile.write('PARENT %s CHILD %s\n'%(parent,child))
		
			#make each omicron2LIB_sig_train job a parent to each zip_and_tar job
			for parent in omicron2LIB_sig_train_jobs:
				for child in zip_and_tar_jobs:
					dagfile.write('PARENT %s CHILD %s\n'%(parent,child))
		
		####################
		### Save run_dic ###
		####################
		
		if not os.path.exists("%s/run_dic"%segdir):
			os.makedirs("%s/run_dic"%segdir)
		pickle.dump(run_dic,open('%s/run_dic/run_dic_%s_%s.pkl'%(segdir,actual_start,stride-overlap),'wt'))
			
		#################
		### Close DAG ###
		#################
		
		dagfile.close()

	elif run_dic['run mode']['line'] == 'Offline':
		pass
