#!/usr/bin/python

import sys
sys.path.insert(1,'/home/ryan.lynch/numpy/numpy-1.8.2-INSTALL/lib64/python2.7/site-packages')
import os
import tarfile

#############################################
if __name__=='__main__':
		
	#Parse user options
	from optparse import OptionParser

	usage = None
	parser = OptionParser(usage=usage)

	#general options
	parser.add_option("-r", "--run-dic", default=None, type="string", help="Path to run_dic (containing all info about the runs")

	#----------------------------------------------

	opts, args = parser.parse_args()

	run_dic = pickle.load(open(opts.run_dic))
	segdir = run_dic['seg dir']
	
	#----------------------------------------------
	
	#MAIN

	#----------------------------------------------

	#Check if results need to be tar'd
	if run_dic['run mode']['tar results']:
		
		#Tar Omicron trigger folder
		if os.path.exists("%s/raw/"%segdir):
			with tarfile.open('%s/raw.tar.gz'%segdir, "w:gz") as tar:
				tar.add('%s/raw'%segdir)
			os.system('rm %s/raw -r'%segdir)
		if os.path.exists("%s/raw_sig_train/"%segdir):
			with tarfile.open('%s/raw_sig_train.tar.gz'%segdir, "w:gz") as tar:
				tar.add('%s/raw_sig_train'%segdir)
			os.system('rm %s/raw_sig_train -r'%segdir)

		#Tar LIB folder
		if os.path.exists("%s/LIB/"%segdir):
			with tarfile.open('%s/LIB.tar.gz'%segdir, "w:gz") as tar:
				tar.add('%s/LIB'%segdir)
			os.system('rm %s/LIB -r'%segdir)
	
		#Tar signal training injection folder
		if os.path.exists("%s/training_injections/"%segdir):
			with tarfile.open('%s/training_injections.tar.gz'%segdir, "w:gz") as tar:
				tar.add('%s/training_injections'%segdir)
			os.system('rm %s/training_injections -r'%segdir)
			
		#Tar PostProc folders
		if os.path.exists("%s/PostProc/"%segdir):
			with tarfile.open('%s/PostProc.tar.gz'%segdir, "w:gz") as tar:
				tar.add('%s/PostProc'%segdir)
			os.system('rm %s/PostProc -r'%segdir)
		if os.path.exists("%s/PostProc_sig_train/"%segdir):
			with tarfile.open('%s/PostProc_sig_train.tar.gz'%segdir, "w:gz") as tar:
				tar.add('%s/PostProc_sig_train'%segdir)
			os.system('rm %s/PostProc_sig_train -r'%segdir)
		
