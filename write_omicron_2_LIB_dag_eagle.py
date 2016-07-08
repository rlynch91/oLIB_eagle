#!/usr/bin/python

import numpy as np
import os

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
		gdb_flag = run_dic['run mode']['gdb flag']
		LIB_flag = run_dic['run mode']['LIB flag']

		FAR_thresh = run_dic['LLRT']['FAR thresh']
		back_dic_path = run_dic['LLRT']['back dic path']
		back_livetime = run_dic['LLRT']['back livetime']
		oLIB_signal_kde_coords = run_dic['LLRT']['oLIB signal kde coords']
		oLIB_signal_kde_values = run_dic['LLRT']['oLIB signal kde values']
		oLIB_noise_kde_coords = run_dic['LLRT']['oLIB noise kde coords']
		oLIB_noise_kde_values = run_dic['LLRT']['oLIB noise kde values']
		
		train_runmode = run_dic['run mode']['train runmode']
		min_hrss = run_dic['prior ranges']['min hrss']
		max_hrss = run_dic['prior ranges']['max hrss']
		min_freq = run_dic['prior ranges']['min freq']
		max_freq = run_dic['prior ranges']['max freq']
		min_quality = run_dic['prior ranges']['min quality']
		max_quality = run_dic['prior ranges']['max quality']
		sample_freq = run_dic['config']['sample freq']
		osnr_thresh = run_dic['config']['oSNR thresh']

		seg_files = {}
		cache_files = {}
		channel_names = {}
		channel_types = {}
		for ifo in ifos:
			seg_files[ifo] = run_dic['data']['seg files'][ifo]
			cache_files[ifo] = run_dic['data']['cache files'][ifo]
			channel_names[ifo] = run_dic['ifos'][ifo]['channel name']
			channel_types[ifo] = run_dic['ifos'][ifo]['channel type']

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
		dagfile = open("%s/dag/2ndPipeDag_%s_%s_%s.dag"%(segdir,"".join(ifos),actual_start,stride-overlap),'wt')

		#initialize job number
		job = 0

		#############################################
		### Write DAG to run omicron for each ifo ###
		#############################################

		omicron_jobs=[]

		#Loop over all ifos
		for i,ifo in enumerate(ifos):
			
			#make raw directory
			if not os.path.exists("%s/raw/%s"%(segdir,ifo)):
				os.makedirs("%s/raw/%s"%(segdir,ifo))

			#replace all IFO in omicron sub file with ifo
			os.system('sed -e "s|IFO|%s|g" -e "s|SEGDIR|%s|g" %s/omicron_eagle.sub > %s/runfiles/omicron_%s_eagle.sub'%(ifo,segdir,infodir,segdir,ifo))
			#replace all necessary variables in params file
			os.system('sed -e "s|IFO|%s|g" -e "s|FRAMECACHE|%s|g" -e "s|CHNAME|%s|g" -e "s|SAMPFREQ|%s|g" -e "s|OLAP|%s|g" -e "s|STRIDE|%s|g" -e "s|RAWDIR|%s|g" -e "s|MINFREQ|%s|g" -e "s|MAXFREQ|%s|g" -e "s|THRESHSNR|%s|g" %s/omicron_params_eagle.txt > %s/runfiles/omicron_params_%s_eagle.txt'%(ifo, cache_files[i], channel_names[i], sample_freq, overlap, stride, segdir+'/raw/'+ifo, min_freq, max_freq, osnr_thresh, infodir, segdir, ifo))
#??			if train_runmode == 'Signal':
				os.system('sed -e "s|//INJECTION|INJECTION|g" %s/runfiles/omicron_params_%s_eagle.txt > %s/tmp.txt; mv %s/tmp.txt %s/runfiles/omicron_params_%s_eagle.txt'%(segdir,ifo,segdir,segdir,segdir,ifo))

			#write JOB
			dagfile.write('JOB %s %s/runfiles/omicron_%s_eagle.sub\n'%(job,segdir,ifo))
			#write VARS
			dagfile.write('VARS %s macroid="omicron-%s-%s" macroarguments="%s %s"\n'%(job, ifo, job, seg_files[i], segdir+'/runfiles/omicron_params_%s_eagle.txt'%ifo))
			#write RETRY
			dagfile.write('RETRY %s 0\n\n'%job)
			
			#Record omicron job numbers
			omicron_jobs += [job]
			
			#Done with job
			job += 1
#??here??
		####################################
		### Write DAG to run omicron2LIB ###
		####################################

		#first cluster triggers for each ifo
		#then do coincidence for each listed combination (0-lag,background,sig train, noise train), stepping through ifos as listed
		#finally, cluster LIB trigs and mark down what ifos LIB needs to analyze each trig with

		omicron2LIB_jobs = []

		#Copy omicron2LIB sub file to segdir
		os.system('sed "s|RUNDIR|%s|g" %s/omicron2LIB_eagle.sub > %s/runfiles/omicron2LIB_eagle.sub'%(segdir,infodir,segdir))

		#Create PostProc folder
		if not os.path.exists("%s/PostProc/"%segdir):
			os.makedirs("%s/PostProc/"%segdir)

		#Create vetoes folder with empty veto file
		if not os.path.exists("%s/vetoes/"%segdir):
			os.makedirs("%s/vetoes/"%segdir)
		os.system('touch %s/vetoes/null_vetoes.txt'%segdir)
		run_dic['vetoes'] = {}
		for ifo in ifos:
			run_dic['vetoes'][ifo] = '%s/vetoes/null_vetoes.txt'%segdir
	
		#Save run_dic
		???pickle.dump(run_dic,open('%s/run_dic/run_dic_%s_%s.pkl'%(segdir,start,stop),'wt'))
		
		#Write JOB
		dagfile.write('JOB %s %s/runfiles/omicron2LIB_eagle.sub\n'%(job,segdir))
		#Write VARS
		dagfile.write('VARS %s macroid="omicron2LIB-%s" macroarguments="-p %s/PostProc -i %s -I %s -r %s/raw -c %s --cluster-t=0.1 --coin-t=0.05 --coin-snr=0. --t-shift-start=%s --t-shift-stop=%s --t-shift-num=%s --segs=%s --veto-files=%s/vetoes/null_vetoes.txt,%s/vetoes/null_vetoes.txt --overlap=%s --log-like-thresh=0. --LIB-window=0.1 --signal-kde-coords=%s --signal-kde-values=%s --noise-kde-coords=%s --noise-kde-values=%s --train-runmode=%s"\n'%(job,job,segdir,infodir,opts.IFOs,segdir,",".join(channel_names),t_shift_start,t_shift_stop,t_shift_num,opts.seg_files,segdir,segdir,overlap,dt_signal_kde_coords,dt_signal_kde_values,dt_noise_kde_coords,dt_noise_kde_values,train_runmode))
		#Write RETRY
		dagfile.write('RETRY %s 0\n\n'%job)

		#Record omicron2LIB job number
		omicron2LIB_jobs += [job]

		#Done with job
		job += 1

		####################################
		### Check if supposed to run LIB ###
		####################################

		if LIB_flag:

			####################################################
			### Write DAG to run lalinference_pipe on 0-lags ###
			####################################################

			lalinference_pipe_0lag_jobs = []

			#Create LIB_0lag folder
			if not os.path.exists("%s/LIB_0lag/"%segdir):
				os.makedirs("%s/LIB_0lag/"%segdir)

			#replace all necessary fields in LIB_runs_eagle.ini file
			os.system('sed -e "s|IFOSCOMMA|%s|g" -e "s|IFOSTOGETHER|%s|g" -e "s|LIBLABEL|%s|g" -e "s|SEGNAME|%s|g" -e "s|RUNDIR|%s|g" -e "s|BINDIR|%s|g" -e "s|CHANNELTYPES|%s|g" -e "s|CHANNELNAMES|%s|g" -e "s|LAG|0lag|g" -e "s|MINHRSS|%s|g" -e "s|MAXHRSS|%s|g" %s/LIB_runs_eagle.ini > %s/runfiles/LIB_0lag_runs_eagle.ini'%(ifos,"".join(ifos),lib_label,"%s_%s_%s"%("".join(ifos),actual_start,stride-overlap),segdir,bindir,channel_types,channel_names,np.log(min_hrss),np.log(max_hrss),infodir,segdir))
			if train_runmode == 'Signal':
				os.system('sed -e "s|START|%s|g" -e "s|STOP|%s|g" -e "s|#mdc|mdc|g" -e "s|#MDC|MDC|g" %s/runfiles/LIB_0lag_runs_eagle.ini > %s/tmp.txt; mv %s/tmp.txt %s/runfiles/LIB_0lag_runs_eagle.ini'%(actual_start-int(0.5*overlap),actual_start-int(0.5*overlap)+stride,segdir,segdir,segdir,segdir))
				
			#Copy lalinference_pipe sub file to segdir
			os.system('sed "s|RUNDIR|%s|g" %s/lalinference_pipe_eagle.sub > %s/runfiles/lalinference_pipe_eagle.sub'%(segdir,infodir,segdir))

			#Write JOB
			dagfile.write('JOB %s %s/runfiles/lalinference_pipe_eagle.sub\n'%(job,segdir))
			#Write VARS
			dagfile.write('VARS %s macroid="lalinference_pipe_0lag-%s" macroarguments="%s -r %s -p /usr1/ryan.lynch/logs/ -g %s/PostProc/LIB_trigs/LIB_0lag_times_%s.txt"\n'%(job,job,segdir+'/runfiles/LIB_0lag_runs_eagle.ini',segdir+'/LIB_0lag/',segdir,"".join(ifos)))
			#Write RETRY
			dagfile.write('RETRY %s 0\n\n'%job)

			#Record lalinference_pipe job number
			lalinference_pipe_0lag_jobs += [job]

			#Done with job
			job += 1
			
			########################################################
			### Write DAG to run lalinference_pipe on timeslides ###
			########################################################

			lalinference_pipe_ts_jobs = []

			#Create LIB_ts folder
			if not os.path.exists("%s/LIB_ts/"%segdir):
				os.makedirs("%s/LIB_ts/"%segdir)

			#replace all necessary fields in LIB_runs_eagle.ini file
			os.system('sed -e "s|IFOSCOMMA|%s|g" -e "s|IFOSTOGETHER|%s|g" -e "s|LIBLABEL|%s|g" -e "s|SEGNAME|%s|g" -e "s|RUNDIR|%s|g" -e "s|BINDIR|%s|g" -e "s|CHANNELTYPES|%s|g" -e "s|CHANNELNAMES|%s|g" -e "s|LAG|ts|g" -e "s|MINHRSS|%s|g" -e "s|MAXHRSS|%s|g" %s/LIB_runs_eagle.ini > %s/runfiles/LIB_ts_runs_eagle.ini'%(ifos,"".join(ifos),lib_label,"%s_%s_%s"%("".join(ifos),actual_start,stride-overlap),segdir,bindir,channel_types,channel_names,np.log(min_hrss),np.log(max_hrss),infodir,segdir))
			if train_runmode == 'Signal':
				os.system('sed -e "s|START|%s|g" -e "s|STOP|%s|g" -e "s|#mdc|mdc|g" -e "s|#MDC|MDC|g" %s/runfiles/LIB_ts_runs_eagle.ini > %s/tmp.txt; mv %s/tmp.txt %s/runfiles/LIB_ts_runs_eagle.ini'%(actual_start-int(0.5*overlap),actual_start-int(0.5*overlap)+stride,segdir,segdir,segdir,segdir))
			
			#Write JOB
			dagfile.write('JOB %s %s/runfiles/lalinference_pipe_eagle.sub\n'%(job,segdir))
			#Write VARS
			dagfile.write('VARS %s macroid="lalinference_pipe_ts-%s" macroarguments="%s -r %s -p /usr1/ryan.lynch/logs/ -g %s/PostProc/LIB_trigs/LIB_ts_times_%s.txt"\n'%(job,job,segdir+'/runfiles/LIB_ts_runs_eagle.ini',segdir+'/LIB_ts/',segdir,"".join(ifos)))
			#Write RETRY
			dagfile.write('RETRY %s 0\n\n'%job)

			#Record lalinference_pipe job number
			lalinference_pipe_ts_jobs += [job]

			#Done with job
			job += 1

			###############################################
			### Write DAG to point to LIB_0lag_runs dag ###
			###############################################

			LIB_0lag_runs_jobs = []

			#Write SUBDAG EXTERNAL
			dagfile.write('SUBDAG EXTERNAL %s %s/LIB_0lag/LIB_runs.dag\n'%(job,segdir))
			#Write RETRY
			dagfile.write('RETRY %s 0\n\n'%job)

			#Record LIB_runs job number
			LIB_0lag_runs_jobs += [job]

			#Done with job
			job += 1
			
			#############################################
			### Write DAG to point to LIB_ts_runs dag ###
			#############################################

			LIB_ts_runs_jobs = []

			#Write SUBDAG EXTERNAL
			dagfile.write('SUBDAG EXTERNAL %s %s/LIB_ts/LIB_runs.dag\n'%(job,segdir))
			#Write RETRY
			dagfile.write('RETRY %s 0\n\n'%job)

			#Record LIB_runs job number
			LIB_ts_runs_jobs += [job]

			#Done with job
			job += 1

			######################################################
			### Write DAG to run Bayes_factors_2_LIB for 0-lag ###
			######################################################

			Bayes2LIB_0lag_jobs = []

			#Create LIB_0lag_rr folder
			if not os.path.exists("%s/LIB_0lag_rr/"%segdir):
				os.makedirs("%s/LIB_0lag_rr/"%segdir)
			
			#Create GraceDb folder
			if not os.path.exists("%s/GDB/"%segdir):
				os.makedirs("%s/GDB/"%segdir)

			#replace all necessary fields in LIB_reruns_eagle.ini file if running follow-up
			if LIB_followup_flag:
				os.system('sed -e "s|IFOSCOMMA|%s|g" -e "s|IFOSTOGETHER|%s|g" -e "s|LIBLABEL|%s|g" -e "s|SEGNAME|%s|g" -e "s|RUNDIR|%s|g" -e "s|BINDIR|%s|g" -e "s|CHANNELTYPES|%s|g" -e "s|CHANNELNAMES|%s|g" -e "s|LAG|0lag|g" -e "s|MINHRSS|%s|g" -e "s|MAXHRSS|%s|g" %s/LIB_reruns_eagle.ini > %s/runfiles/LIB_0lag_reruns_eagle.ini'%(ifos,"".join(ifos),lib_label,"%s_%s_%s"%("".join(ifos),actual_start,stride-overlap),segdir,bindir,channel_types,channel_names,np.log(min_hrss),np.log(max_hrss),infodir,segdir))
				if train_runmode == 'Signal':
					os.system('sed -e "s|START|%s|g" -e "s|STOP|%s|g" -e "s|#mdc|mdc|g" -e "s|#MDC|MDC|g" %s/runfiles/LIB_0lag_reruns_eagle.ini > %s/tmp.txt; mv %s/tmp.txt %s/runfiles/LIB_0lag_reruns_eagle.ini'%(actual_start-int(0.5*overlap),actual_start-int(0.5*overlap)+stride,segdir,segdir,segdir,segdir))

			#Copy Bayes2LIB sub file to segdir
			os.system('sed "s|RUNDIR|%s|g" %s/Bayes2LIB_eagle.sub > %s/runfiles/Bayes2LIB_eagle.sub'%(segdir,infodir,segdir))

			#Write JOB
			dagfile.write('JOB %s %s/runfiles/Bayes2LIB_eagle.sub\n'%(job,segdir))
			#Write VARS
			B2L_args = "-I %s -r %s -i %s -b %s --lib-label=%s --start=%s --stride=%s --overlap=%s --lag=0lag --FAR-thresh=%s --background-dic=%s --background-livetime=%s --signal-kde-coords=%s --signal-kde-values=%s --noise-kde-coords=%s --noise-kde-values=%s --train-runmode=%s --LIB-window=0.1"%(",".join(ifos),segdir,infodir,bindir,lib_label,actual_start,stride,overlap,FAR_thresh,back_dic_path,back_livetime,oLIB_signal_kde_coords,oLIB_signal_kde_values,oLIB_noise_kde_coords,oLIB_noise_kde_values,train_runmode)
			if gdb_flag:
				B2L_args += " --gdb"
			if LIB_followup_flag:
				B2L_args += " --LIB-followup"
			dagfile.write('VARS %s macroid="Bayes2LIB_0lag-%s" macroarguments="%s"\n'%(job,job,B2L_args))
			#Write RETRY
			dagfile.write('RETRY %s 0\n\n'%job)

			#Record lalinference_pipe job number
			Bayes2LIB_0lag_jobs += [job]

			#Done with job
			job += 1
			
			###########################################################
			### Write DAG to run Bayes_factors_2_LIB for timeslides ###
			###########################################################

			Bayes2LIB_ts_jobs = []
				
			#Create LIB_ts_rr folder
			if not os.path.exists("%s/LIB_ts_rr/"%segdir):
				os.makedirs("%s/LIB_ts_rr/"%segdir)
				
			#Create GraceDb folder
			if not os.path.exists("%s/GDB/"%segdir):
				os.makedirs("%s/GDB/"%segdir)

			#replace all necessary fields in LIB_reruns_eagle.ini file if running follow-up
			if LIB_followup_flag:
				os.system('sed -e "s|IFOSCOMMA|%s|g" -e "s|IFOSTOGETHER|%s|g" -e "s|LIBLABEL|%s|g" -e "s|SEGNAME|%s|g" -e "s|RUNDIR|%s|g" -e "s|BINDIR|%s|g" -e "s|CHANNELTYPES|%s|g" -e "s|CHANNELNAMES|%s|g" -e "s|LAG|ts|g" -e "s|MINHRSS|%s|g" -e "s|MAXHRSS|%s|g" %s/LIB_reruns_eagle.ini > %s/runfiles/LIB_ts_reruns_eagle.ini'%(ifos,"".join(ifos),lib_label,"%s_%s_%s"%("".join(ifos),actual_start,stride-overlap),segdir,bindir,channel_types,channel_names,np.log(min_hrss),np.log(max_hrss),infodir,segdir))
				if train_runmode == 'Signal':
					os.system('sed -e "s|START|%s|g" -e "s|STOP|%s|g" -e "s|#mdc|mdc|g" -e "s|#MDC|MDC|g" %s/runfiles/LIB_ts_reruns_eagle.ini > %s/tmp.txt; mv %s/tmp.txt %s/runfiles/LIB_ts_reruns_eagle.ini'%(actual_start-int(0.5*overlap),actual_start-int(0.5*overlap)+stride,segdir,segdir,segdir,segdir))

			#Write JOB
			dagfile.write('JOB %s %s/runfiles/Bayes2LIB_eagle.sub\n'%(job,segdir))
			#Write VARS
			B2L_args = "-I %s -r %s -i %s -b %s --lib-label=%s --start=%s --stride=%s --overlap=%s --lag=ts --FAR-thresh=%s --background-dic=%s --background-livetime=%s --signal-kde-coords=%s --signal-kde-values=%s --noise-kde-coords=%s --noise-kde-values=%s --train-runmode=%s --LIB-window=0.1"%(",".join(ifos),segdir,infodir,bindir,lib_label,actual_start,stride,overlap,FAR_thresh,back_dic_path,back_livetime,oLIB_signal_kde_coords,oLIB_signal_kde_values,oLIB_noise_kde_coords,oLIB_noise_kde_values,train_runmode)
			if LIB_followup_flag:
				B2L_args += " --LIB-followup"
			dagfile.write('VARS %s macroid="Bayes2LIB_ts-%s" macroarguments="%s"\n'%(job,job,B2L_args))
			#Write RETRY
			dagfile.write('RETRY %s 0\n\n'%job)

			#Record lalinference_pipe job number
			Bayes2LIB_ts_jobs += [job]

			#Done with job
			job += 1	

		####################################
		### Write parent-child relations ###
		####################################

		#make each omicron job a parent to each omicron2LIB job
		for parent in omicron_jobs:
			for child in omicron2LIB_jobs:
				dagfile.write('PARENT %s CHILD %s\n'%(parent,child))

		if LIB_flag:

			#make each omicron2LIB job a parent to each lalinference_pipe_0lag job
			for parent in omicron2LIB_jobs:
				for child in lalinference_pipe_0lag_jobs:
					dagfile.write('PARENT %s CHILD %s\n'%(parent,child))
					
			#make each omicron2LIB job a parent to each lalinference_pipe_ts job
			for parent in omicron2LIB_jobs:
				for child in lalinference_pipe_ts_jobs:
					dagfile.write('PARENT %s CHILD %s\n'%(parent,child))
					
			#make each lalinference_pipe_0lag job a parent to each LIB_0lag_runs job
			for parent in lalinference_pipe_0lag_jobs:
				for child in LIB_0lag_runs_jobs:
					dagfile.write('PARENT %s CHILD %s\n'%(parent,child))
			
			#make each lalinference_pipe_ts job a parent to each LIB_ts_runs job
			for parent in lalinference_pipe_ts_jobs:
				for child in LIB_ts_runs_jobs:
					dagfile.write('PARENT %s CHILD %s\n'%(parent,child))
					
			#make each LIB_0lag_runs job a parent to each Bayes2LIB_0lag job
			for parent in LIB_0lag_runs_jobs:
				for child in Bayes2LIB_0lag_jobs:
					dagfile.write('PARENT %s CHILD %s\n'%(parent,child))
			
			#make each LIB_ts_runs job a parent to each Bayes2LIB_ts job
			for parent in LIB_ts_runs_jobs:
				for child in Bayes2LIB_ts_jobs:
					dagfile.write('PARENT %s CHILD %s\n'%(parent,child))
					
			if LIB_followup_flag:
			
				#make each Bayes2LIB_0lag job a parent to each LIB_0lag_reruns job
				for parent in Bayes2LIB_0lag_jobs:
					for child in LIB_0lag_reruns_jobs:
						dagfile.write('PARENT %s CHILD %s\n'%(parent,child))
						
				#make each Bayes2LIB_ts job a parent to each LIB_ts_reruns job
				for parent in Bayes2LIB_ts_jobs:
					for child in LIB_ts_reruns_jobs:
						dagfile.write('PARENT %s CHILD %s\n'%(parent,child))

		#################
		### Close DAG ###
		#################
		dagfile.close()

	elif run_dic['run mode'['line'] == 'Offline':
		pass
