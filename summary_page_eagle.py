#!/usr/bin/python

import numpy as np
import os
import commands
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
import pickle

##############################################

###
def cumulative_SNR_plot(snr_array_0lag,snr_array_back,livetime_0lag,livetime_back,ifos,label,outdir):
	"""
	Makes plot of rate of triggers above a given SNR
	"""
	snr_sorted_0lag = np.sort(snr_array_0lag)[::-1]
	snr_sorted_back = np.sort(snr_array_back)[::-1]
	
	rate_above_0lag = np.arange(1,len(snr_sorted_0lag)+1) / float(livetime_0lag)
	rate_above_back = np.arange(1,len(snr_sorted_back)+1) / float(livetime_0lag)

	myfig = plt.figure()

	plt.plot(snr_sorted_0lag, rate_above_0lag, 'b-', label='0lag', linewidth=3)
	plt.plot(snr_sorted_back, rate_above_back, 'r-', label='Background', linewidth=3)

	plt.xlabel("%s SNR"%ifos)
	plt.ylabel("Rate exceeding SNR value during livetime [Hz]")
	plt.grid(True,which="both")
	plt.xscale('log')
	plt.yscale('log')
	plt.title('Cumulative SNR rates for %s'%ifos)
	plt.legend(loc='best')

	myfig.savefig('%s/cumrate_vs_SNR_%s_%s'%(outdir,ifos,label), bbox_inches='tight')

###
def cumulative_logBSN_plot(logBSN_array_0lag,logBSN_array_back,livetime_0lag,livetime_back,label,outdir):
	"""
	Makes plot of rate of triggers above a given logBSN
	"""
	logBSN_sorted_0lag = np.sort(logBSN_array_0lag)[::-1]
	logBSN_sorted_back = np.sort(logBSN_array_back)[::-1]
	
	rate_above_0lag = np.arange(1,len(logBSN_sorted_0lag)+1) / float(livetime_0lag)
	rate_above_back = np.arange(1,len(logBSN_sorted_back)+1) / float(livetime_back)
	
	myfig = plt.figure()

	plt.plot(logBSN_sorted_0lag, rate_above_0lag, 'b-', label='0lag', linewidth=3)
	plt.plot(logBSN_sorted_back, rate_above_back, 'r-', label='Background', linewidth=3)

	plt.xlabel("log10BSN")
	plt.ylabel("Rate exceeding log10BSN value during livetime [Hz]")
	plt.grid(True,which="both")
	plt.xscale('log')
	plt.yscale('log')
	plt.title('Cumulative log10BSN rates')
	leg = plt.legend(loc='upper right', fancybox=True)
	leg.get_frame().set_alpha(0.5)

	myfig.savefig('%s/cumrate_vs_logBSN_%s'%(outdir,label), bbox_inches='tight')
	
###
def cumulative_BCI_plot(BCI_array_0lag,BCI_array_back,livetime_0lag,livetime_back,label,outdir):
	"""
	Makes plot of rate of triggers above a given BCI
	"""
	BCI_sorted_0lag = np.sort(BCI_array_0lag)[::-1]
	BCI_sorted_back = np.sort(BCI_array_back)[::-1]
	
	rate_above_0lag = np.arange(1,len(BCI_sorted_0lag)+1) / float(livetime_0lag)
	rate_above_back = np.arange(1,len(BCI_sorted_back)+1) / float(livetime_back)
	
	myfig = plt.figure()

	plt.plot(BCI_sorted_0lag, rate_above_0lag, 'b-', label='0lag', linewidth=3)
	plt.plot(BCI_sorted_back, rate_above_back, 'r-', label='Background', linewidth=3)

	plt.xlabel("BCI")
	plt.ylabel("Rate exceeding BCI value during livetime [Hz]")
	plt.grid(True,which="both")
	plt.xscale('log')
	plt.yscale('log')
	plt.title('Cumulative BCI rates')
	leg = plt.legend(loc='upper right', fancybox=True)
	leg.get_frame().set_alpha(0.5)

	myfig.savefig('%s/cumrate_vs_BCI_%s'%(outdir,label), bbox_inches='tight')

###
def cumulative_frequency_plot(freq_array_0lag,freq_array_back,livetime_0lag,livetime_back,label,outdir):
	"""
	Makes plot of rate of triggers above a given frequency
	"""
	freq_sorted_0lag = np.sort(freq_array_0lag)[::-1]
	freq_sorted_back = np.sort(freq_array_back)[::-1]
	
	rate_above_0lag = np.arange(1,len(freq_sorted_0lag)+1) / float(livetime_0lag)
	rate_above_back = np.arange(1,len(freq_sorted_back)+1) / float(livetime_back)
	
	myfig = plt.figure()

	plt.plot(freq_sorted_0lag, rate_above_0lag, 'b-', label='0lag', linewidth=3)
	plt.plot(freq_sorted_back, rate_above_back, 'r-', label='Background', linewidth=3)

	plt.xlabel("Mean Central Frequency [Hz]")
	plt.ylabel("Rate exceeding frequency value during livetime [Hz]")
	plt.grid(True,which="both")
	plt.xscale('log')
	plt.yscale('log')
	plt.title('Cumulative central frequency rates')
	leg = plt.legend(loc='upper right', fancybox=True)
	leg.get_frame().set_alpha(0.5)

	myfig.savefig('%s/cumrate_vs_freq_%s'%(outdir,label), bbox_inches='tight')

###
def cumulative_Q_plot(Q_array_0lag,Q_array_back,livetime_0lag,livetime_back,label,outdir):
	"""
	Makes plot of rate of triggers above a given Q
	"""
	Q_sorted_0lag = np.sort(Q_array_0lag)[::-1]
	Q_sorted_back = np.sort(Q_array_back)[::-1]
	
	rate_above_0lag = np.arange(1,len(Q_sorted_0lag)+1) / float(livetime_0lag)
	rate_above_back = np.arange(1,len(Q_sorted_back)+1) / float(livetime_back)
	
	myfig = plt.figure()

	plt.plot(Q_sorted_0lag, rate_above_0lag, 'b-', label='0lag', linewidth=3)
	plt.plot(Q_sorted_back, rate_above_back, 'r-', label='Background', linewidth=3)

	plt.xlabel("Mean Quality Factor (Q)")
	plt.ylabel("Rate exceeding Q value during livetime [Hz]")
	plt.grid(True,which="both")
	plt.xscale('log')
	plt.yscale('log')
	plt.title('Cumulative Q rates')
	leg = plt.legend(loc='upper right', fancybox=True)
	leg.get_frame().set_alpha(0.5)

	myfig.savefig('%s/cumrate_vs_Q_%s'%(outdir,label), bbox_inches='tight')

###
def trig_rate_vs_time_plot(time_array,snr_array,t_start,t_stop,ifos,label,outdir):
	"""
	Makes plot of trigger rate binned into 1 minute intervals
	"""
	bins = np.linspace(start=t_start, stop=t_stop, num=np.ceil((t_stop - t_start + 60.)/60.))
	
	myfig=plt.figure()

	above_5 = time_array[snr_array >= 5.]
	above_8 = time_array[snr_array >= 8.]
	above_15 = time_array[snr_array >= 15.]

	plt.plot((bins[1:]-t_stop)/86400., np.histogram(above_5,bins=bins)[0]/60., 'bo', label='SNR >= 5', markersize=3)
	plt.plot((bins[1:]-t_stop)/86400., np.histogram(above_8,bins=bins)[0]/60., 'ro', label='SNR >= 8', markersize=3)
	plt.plot((bins[1:]-t_stop)/86400., np.histogram(above_15,bins=bins)[0]/60., 'go', label='SNR >= 15', markersize=3)

	t_stop_p60_utc = commands.getstatusoutput('lalapps_tconvert -d %s'%int(t_stop+60))[1]
	plt.xlabel("Time [days] since %s (UTC: %s), 60s bins"%(int(t_stop+60),t_stop_p60_utc))
	plt.ylabel("Rate [Hz]")
	plt.grid(True,which="both")
	leg = plt.legend(loc='upper right', fancybox=True)
	leg.get_frame().set_alpha(0.5)
	plt.yscale('log')
	plt.title('Coincident glitch rate as a function of %s SNR'%ifos)

	myfig.savefig('%s/glitchrate_%s_%s'%(outdir,ifos,label), bbox_inches='tight')

##############################################
if __name__=='__main__':	
	
	from optparse import OptionParser

	usage = None
	parser = OptionParser(usage=usage)

	parser.add_option("","--gpstime", default=None, type='float', help="GPS time to search a week back from")
	parser.add_option("","--collectdir", default=None, type='string', help="Path to directory containing the collected results")
	parser.add_option("","--outdir", default=None, type='string', help="Path to directory in which to output plots")
	parser.add_option("","--ifo-group", default=None, type="string", help="IFO group for which to make summary page (e.g., 'H1L1'")
	parser.add_option("","--label", default=None, type='string', help="Label to describe what search data is being collected for")

	#---------------------------------------------

	opts, args = parser.parse_args()

	gpstime = opts.gpstime
	collectdir = opts.collectdir
	outdir = opts.outdir
	ifo_group = opts.ifo_group
	label = opts.label

	#############################################
	
	#Find ifos in the ifo group
	ifos = ifo_group.strip('1').split('1')
	ifos = ['%s1'%ifo for ifo in ifos]

	#Initialize the week that the summary page will be made to cover
	gpsday = int(float(gpstime)/100000.)
	gps_days = np.arange(start=int(gpsday-5),stop=(gpsday+1))
	
	#Initialize variables that need to be collected
	SNR_lists_0lag = {}
	SNR_lists_0lag[ifo_group] = []
	for ifo in ifos:
		SNR_lists_0lag[ifo] = []
	logBSN_list_0lag = []
	BCI_list_0lag = []
	freq_list_0lag = []
	Q_list_0lag = []
	time_list_0lag = []
	FAR_list_0lag = []
	livetime_0lag = 0
		
	SNR_lists_back = {}
	SNR_lists_back[ifo_group] = []
	for ifo in ifos:
		SNR_lists_back[ifo] = []
	logBSN_list_back = []
	BCI_list_back = []
	freq_list_back = []
	Q_list_back = []
	livetime_back = 0.
	
	#Loop over the gps days in the week, collecting the results and livetime for the 0lag and background
	for day in gps_days:
		#Load in results dictionaries
		dic_0lag = pickle.load(open(???))
		dic_back = pickle.load(open(???))
		
		#Load in livetimes
		livetime_0lag += float(np.genfromtxt(???))
		livetime_back += float(np.genfromtxt(???))
		
		#Loop over all events in 0lag dictionary
		for key in dic_0lag:
			SNR_lists_0lag[ifo_group] += [dic_0lag[key]['Omicron SNR']['Network']]
			for ifo in ifos:
				SNR_lists_0lag[ifo] += [dic_0lag[key]['Omicron SNR'][ifo]]
			logBSN_list_0lag += [dic_0lag[key]['logBSN']]
			BCI_list_0lag += [dic_0lag[key]['BCI']]
			freq_list_0lag += [dic_0lag[key]['frequency']['posterior mean']]
			Q_list_0lag += [dic_0lag[key]['quality']['posterior mean']]
			time_list_0lag += [dic_0lag[key]['gpstime']]
			FAR_list_0lag += [dic_0lag[key]['FAR']]
			
		#Loop over all events in background dictionary
		for key in dic_back:
			SNR_lists_back[ifo_group] += [dic_back[key]['Omicron SNR']['Network']]
			for ifo in ifos:
				SNR_lists_back[ifo] += [dic_back[key]['Omicron SNR'][ifo]]
			logBSN_list_back += [dic_back[key]['logBSN']]
			BCI_list_back += [dic_back[key]['BCI']]
			freq_list_back += [dic_back[key]['frequency']['posterior mean']]
			Q_list_back += [dic_back[key]['quality']['posterior mean']]
			
	#Make necessary plots
	try:
		cumulative_SNR_plot(snr_array_0lag=np.array(SNR_lists_0lag[ifo_group]),snr_array_back=np.array(SNR_lists_back[ifo_group]),livetime_0lag=livetime_0lag,livetime_back=livetime_back,ifos=ifo_group,label=label,outdir=outdir)
	except (NameError,ValueError,IndexError):
		???
	
	try:
		trig_rate_vs_time_plot(time_array=np.array(time_list_0lag),snr_array=np.array(SNR_lists_0lag[ifo_group]),t_start=gps_days[0]*100000.,t_stop=gps_days[-1]*100000.,ifos=ifo_group,label=label,outdir=outdir)
	except (NameError,ValueError,IndexError):
		???
	
	for ifo in ifos:
		try:
			cumulative_SNR_plot(snr_array_0lag=np.array(SNR_lists_0lag[ifo]),snr_array_back=np.array(SNR_lists_back[ifo]),livetime_0lag=livetime_0lag,livetime_back=livetime_back,ifos=ifo,label=label,outdir=outdir)
		except (NameError,ValueError,IndexError):
			???
		
		try:
			trig_rate_vs_time_plot(time_array=np.array(time_list_0lag),snr_array=np.array(SNR_lists_0lag[ifo]),t_start=gps_days[0]*100000.,t_stop=gps_days[-1]*100000.,ifos=ifo,label=label,outdir=outdir)
		except (NameError,ValueError,IndexError):
			???
	
	try:
		cumulative_logBSN_plot(logBSN_array_0lag=np.array(logBSN_list_0lag),logBSN_array_back=np.array(logBSN_list_back),livetime_0lag=livetime_0lag,livetime_back=livetime_back,label=label,outdir=outdir)
	except (NameError,ValueError,IndexError):
		???

	try:
		cumulative_BCI_plot(BCI_array_0lag=np.array(BCI_list_0lag),BCI_array_back=np.array(BCI_list_back),livetime_0lag=livetime_0lag,livetime_back=livetime_back,label=label,outdir=outdir)
	except (NameError,ValueError,IndexError):
		???

	try:
		cumulative_frequency_plot(freq_array_0lag=np.array(freq_list_0lag),freq_array_back=np.array(freq_list_back),livetime_0lag=livetime_0lag,livetime_back=livetime_back,label=label,outdir=outdir)
	except (NameError,ValueError,IndexError):
		???

	try:
		cumulative_Q_plot(Q_array_0lag=np.array(Q_list_0lag),Q_array_back=np.array(Q_list_back),livetime_0lag=livetime_0lag,livetime_back=livetime_back,label=label,outdir=outdir)
	except (NameError,ValueError,IndexError):
		???

	#Check if the oLIB pipeline is currently running
	job_status_file = open(outdir + "/job_status_%s.txt"%label,'wt')
	job_status_file.write("Job is not currently running")
	job_status_file.close()
	proc_list = commands.getstatusoutput('ps -Fu %s | grep %s | grep /usr/bin/python'%(???,???))[1].split('\n')
	for proc in proc_list:
		proc_split = proc.split()
		if not any(['grep' in element for element in proc_split]):
			proc_user = proc_split[0]
			proc_id = proc_split[1]
			proc_loc = commands.getstatusoutput('hostname -f')[1]
			job_status_file = open(outdir + "/job_status_%s.txt"%label,'wt')
			job_status_file.write("Job is currently running.  Job location is %s.  Job ID is %s"%(proc_loc,proc_id))
			job_status_file.close()
			break

	#Save current livetimes
	lt_0lag_file = open(outdir + "/livetime_0lag_%s.txt"%label,'wt')
	lt_0lag_file.write("%s s = %s days = %s years"%(livetime_0lag,livetime_0lag/3600.,livetime_0lag/86400.))
	lt_0lag_file.close()
	
	lt_back_file = open(outdir + "/livetime_back_%s.txt"%label,'wt')
	lt_back_file.write("%s s = %s days = %s years"%(livetime_back,livetime_back/3600.,livetime_back/86400.))
	lt_back_file.close()
	
	#Save 25 most significant FAR triggers
	most_sig_0lag = np.array(sorted(zip(FAR_list_0lag,time_list_0lag,logBSN_list_0lag,BCI_list_0lag,SNR_lists_0lag[ifo_group],freq_list_0lag,Q_list_0lag), key=lambda x:x[0], reverse=True))
	most_sig_0lag_file = open(outdir + "/most_sig_0lag_%s.txt"%label,'wt')
	most_sig_0lag_file.write('Rank\tFAR\tTime\tlogBSN\tBCI\tNetSNR\tFreq\tQ\t\n')
	for i,line in enumerate(array[:25]):
		most_sig_0lag_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n'%(i+1,line[0],line[1],line[2],line[3],line[4],line[5],line[6]))
	most_sig_0lag_file.close()	
	
	#-------------------------------------------------------------------
	
	#Build HTML page
	os.system("rm " + outdir + '/index.html')
	os.system("source " + outdir + '/make-index.sh')
