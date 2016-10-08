#!/usr/bin/python

import sys
sys.path.insert(1,'/home/ryan.lynch/numpy/numpy-1.8.2-INSTALL/lib64/python2.7/site-packages')
import numpy as np
from pylal import Fr

#=======================================================================

###
def checkDQ(framecache_file, chname, abs_start, abs_stop, ifo, bitmask):
	"""
	Takes a file containing the data quality state vetor and converts it to segments of a desired bitmask, returning injection status
	"""
	#Initialize data-quality veto status as False (will change if 'No veto' bits are off)
	DQV_flag = False
	
	#Open framecache file
	cache = open(framecache_file, 'rt')

	#Loop over frames in the cache
	for line in cache:
		#Get frame_start, frame_stride, and frame_file
		words = line.split()
		frame_start = int(words[2])
		frame_stride = int(words[3])
		frame_file = words[4].split('file://localhost')[1]
					
		#Open state vector as array
		state_array = Fr.frgetvect1d(filename=frame_file,channel='%s:%s'%(ifo,chname))[0]
		
		#Calculate sample rate
		samp_rate = len(state_array)/float(frame_stride)
		
		#Loop over state vetor
		for i, value in enumerate(state_array):
			#Check to make sure we've passed the absolute start
			if (frame_start + i/float(samp_rate)) < abs_start:
				continue
				
			#Check to make sure we haven't passed the absolute stop
			elif (frame_start + i/float(samp_rate)) > abs_stop:
				break
				
			#Check if DQ vector denotes that a veto is present
			if ((int(value) & bitmask) != bitmask) or (int(value)<0):  #(e.g., we might want bits ??, ??, or ?? to be on if there are no data-quality vetoes)
				DQV_flag = True

	cache.close()
	
	#Return injection flag
	return DQV_flag

###
def executable(ifo, dq_chname, dq_bitmask, run_dic):
	"""
	"""
	#Grab necessary variables from run_dic
	framecache_file = run_dic['data']['cache files'][ifo]
	abs_start = run_dic['times']['start']
	abs_stop = run_dic['times']['stop']
	
	#Produce and merge segments from framecache state vectors
	dqv_status = checkDQ(framecache_file=framecache_file, chname=dq_chname, abs_start=abs_start, abs_stop=abs_stop, ifo=ifo, bitmask=dq_bitmask)

	return dqv_status


##############################################
if __name__=='__main__':
	from optparse import OptionParser

	usage = None
	parser = OptionParser(usage=usage)

	parser.add_option("","--cache-file", default=None, type='string', help="Path to framecache file")
	parser.add_option("","--dq-channel", default=None, type='string', help="Name of channel containing ifo DQ vector")
	parser.add_option("","--start", default=None, type='int', help="Absolute start time of segments")
	parser.add_option("","--stop", default=None, type='int', help="Absolute stop time of segments")
	parser.add_option("","--IFO", default=None, type="string", help="Name of ifo, e.g., H1")
	parser.add_option("","--dq-bitmask", default=None, type="int", help="Number corresponding to bitmask that signifies no DQV are in the data")

	#---------------------------------------------

	opts, args = parser.parse_args()

	framecache_file = opts.cache_file
	dq_chname = opts.dq_channel
	abs_start = opts.start
	abs_stop = opts.stop
	ifo = opts.IFO
	dq_bitmask = opts.dq_bitmask
	
	#---------------------------------------------
	
	#Produce and merge segments from framecache state vectors
	dqv_status = checkDQ(framecache_file=framecache_file, chname=dq_chname, abs_start=abs_start, abs_stop=abs_stop, ifo=ifo, bitmask=dq_bitmask)

	print dqv_status

