import numpy as np
import os
import commands
import re

#=======================================================================

###
def executable(run_dic):
	"""
	"""
	#initialize variables we need
	ifos_all = np.array(run_dic['ifos']['names'])
	ifos = []
	for ifo in ifos_all:
		if run_dic['data']['success flags'][ifo]:
			ifos += [ifo]
	bindir = run_dic['config']['LIB bin dir']
	start = run_dic['times']['start']
	stop = run_dic['times']['stop']
	overlap = run_dic['config']['overlap']
	segdir = run_dic['seg dir']
	min_hrss = run_dic['prior ranges']['min hrss']
	max_hrss = run_dic['prior ranges']['max hrss']
	min_freq = run_dic['prior ranges']['min freq']
	max_freq = run_dic['prior ranges']['max freq']
	min_quality = run_dic['prior ranges']['min quality']
	max_quality = run_dic['prior ranges']['max quality']
	snr_thresh = run_dic['config']['oSNR thresh']
	
	cache_files = {}
	asd_files = {}
	for ifo in ifos:
		cache_files[ifo] = run_dic['data']['cache files'][ifo]
		asd_files[ifo] = run_dic['training']['asd files'][ifo]

	#=======================================================================
	#Make necessary folders
	os.makedirs("%s/training_injections/raw"%segdir)
	os.makedirs("%s/training_injections/merged"%segdir)

	#Initialize mdc parameters
	ifos_str = repr(",".join(ifos))  #"'H1,L1'"
	num_mdc = 1  #number of mdc injection frames generated
	mdc_start_time = start  #start time of mdc injection frame
	mdc_end_time = stop  #end time of mdc injection frame
	padding = int(overlap/2.)  # buffer between edges of frame and injections, value is padding on each end

	mdc_duration = mdc_end_time - mdc_start_time
	trig_end_time = mdc_end_time - padding
	trig_start_time = mdc_start_time + padding + np.random.randint(low=0, high=min((mdc_duration-2*padding+1),100))
	seed = trig_start_time

	mdc_par={
	"ifos":"["+ifos_str+"]",
	"duration":mdc_duration,
	"pad":padding,
	"gps-start":mdc_start_time,
	}

	#Initialize injection parameters
	#Randomly select SG vs WNB
	types = ["SG"]
	inj_type = types[np.random.randint(low=0, high=len(types))]

	if inj_type == "SG":
		par={
		"population":"all_sky_sinegaussian", # time domain SG
		"q-distr":"uniform",
		"min-q":min_quality,
		"max-q":max_quality,
		"f-distr":"uniform",
		"min-frequency":min_freq,
		"max-frequency":max_freq,
		"hrss-distr":"volume",
		'min-hrss':min_hrss, # approximate lower limit of detectability
		'max-hrss':max_hrss,
		"polar-angle-distr":"uniform",
		"min-polar-angle":0.0,
		"max-polar-angle":2.0*np.pi,
		"polar-eccentricity-distr":"uniform",
		"min-polar-eccentricity":0.0,
		"max-polar-eccentricity":1.0,
		"seed":seed,
		"gps-start-time":trig_start_time,
		"gps-end-time":trig_end_time,
		"time-step":100.,
		"min-snr":(snr_thresh*np.sqrt(len(ifos)))/2.0,
		"max-snr":1000000.,
		"ifos":",".join(ifos),
		"output": "%s/training_injections/raw/SG_seed_%s_hrss_%s_%s_time_%s_%s.xml"%(segdir,seed,min_hrss,max_hrss,mdc_start_time,mdc_end_time)
		}

		for ifo in ifos:
			if ifo == 'H1' or ifo == 'L1':
				par["ligo-psd"] = asd_files[ifo]
				par["ligo-start-freq"] = 0.1
			elif ifo == 'V1':
				par["virgo-psd"] = asd_files[ifo]
				par["virgo-start-freq"] = 0.1

	else:
		raise ValueError, "No injection type selected"

	#Create timeslide file
	os.chdir('%s/training_injections/raw/'%segdir)
	os.system("%s/ligolw_tisi --instrument H1=0:0:0 --instrument L1=0:0:0 --instrument V1=0:0:0 %s/training_injections/raw/time_slides.xml.gz"%(bindir,segdir)) # if this file doesn't exist, the main function will complain

	#Run lalapps_libbinj to create injection xml file
	libbinj_string="%s/lalapps_libbinj --time-slide-file %s/training_injections/raw/time_slides.xml.gz"%(bindir,segdir)

	for key in par:
		if type(par[key])==str:
			libbinj_string += " --" + key + " " + par[key]
		else:
			libbinj_string += " --" + key + " " + repr(par[key])

	os.chdir('%s/training_injections/raw/'%segdir)
	os.system(libbinj_string)

	#Run lalapps_simburst_to_frame to create injection frames
	frame_string="%s/lalapps_simburst_to_frame --simburst-file %s --channels %s"%(bindir, par["output"], '['+','.join(['Science']*len(ifos))+']')

	for key in mdc_par:
	  if type(mdc_par[key])==str:
		frame_string += " --" + key + " " + mdc_par[key]
	  else:
		frame_string += " --" + key + " " + repr(mdc_par[key])

	os.chdir('%s/training_injections/raw/'%segdir)
	os.system(frame_string)

	#Make cache file for the injection frames
	os.system('ls %s/training_injections/raw/*.gwf | lalapps_path2cache >> %s/framecache/MDC_Injections_%s_%s.lcf'%(segdir,segdir,mdc_start_time,mdc_end_time))

	#Combine data frames and injection frame, putting it in a cache file
	for ifo in ifos:
		cache = open('%s/framecache/MDC_DatInjMerge_%s_%s_%s.lcf'%(segdir,ifo,mdc_start_time,mdc_end_time),'wt')

		#Get paths of data frames
		dat_files = []
		dat_cache = open(cache_files[ifo],'rt')
		for line in dat_cache:
			#Get frame_file from data cache
			words = line.split()
			frame_file = words[4].split('file://localhost')[1]
			dat_files.append(frame_file)
		dat_files = " ".join(dat_files).strip()

		#Get paths of injection frames
		inj_files = commands.getstatusoutput("ls %s/training_injections/raw/*.gwf"%segdir)[1]
		inj_files = re.split('\n', inj_files)
		inj_files = " ".join(inj_files).strip()

		out_file = "%s/training_injections/merged/%s-DatInjMerge-%u-%u.gwf"%(segdir, ifo, mdc_start_time, mdc_duration)
		os.system("FrCopy -i %s %s -o %s"%(inj_files, dat_files, out_file))
		out_file_actual = commands.getstatusoutput("readlink -f %s"%out_file)[1]
		cache.write("%s DatInjMerge %s %s %s\n"%(ifo, mdc_start_time, mdc_duration, "file://localhost"+out_file_actual))
			
		cache.close()
