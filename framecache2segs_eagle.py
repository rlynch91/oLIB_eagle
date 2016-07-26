#!/usr/bin/python

import numpy as np
import os
import commands
from pylal import Fr

#=======================================================================

###
def framecache2segs(framecache_file, chname, abs_start, abs_stop, outdir, ifo, run_bitmask, inj_bitmask):
	"""
	Takes a file containing the data quality state vetor and converts it to segments of a desired bitmask, returning injection status
	"""
	#Initialize injection status as True (will change if 'No injection' bits are on)
	inj_flag = False
	
	#Open framecache file and segment file to write to
	cache = open(framecache_file, 'rt')
	segfile = open(outdir+'/%s_%s_%s.seg'%(ifo,abs_start,abs_stop),'wt')

	#Define start and stop of current segment
	current_start = None
	current_stop = None

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
				
			#Check if state vector corresponds to desired bitmask
			elif (int(value) & run_bitmask) == run_bitmask:  #(e.g., 0b00011 = 3 and we want bits 0 and 1 to be on, so we do & with 3)
				#Data is good, start new seg if needed
				if not current_start:
					current_start = int(np.ceil(frame_start + i/float(samp_rate) ))  #data good starting at ith sample, use ceiling so don't underestimate start
			else:
				#Data not good, end current seg if needed
				if current_start:
					current_stop = int(np.floor(frame_start + i/float(samp_rate) ))  #data goes bad at ith sample but good until then, use floor so don't overestimate stop
					if current_start < current_stop:
						segfile.write('%s %s\n'%(current_start, current_stop))
					#Wait to start next segment until find good data
					current_start = None
					current_stop = None

			#Check if state vector denotes that an injection is present
			if ((int(value) & inj_bitmask) != inj_bitmask):  #(e.g., we might want bits 5, 6, 7, or 8 to be on if there are no HW injections)
				inj_flag = True

		#Write final segment for this frame if needed
		if current_start:
			if (current_start < int(frame_start+frame_stride)) and (int(frame_start+frame_stride) < abs_stop):
				segfile.write('%s %s\n'%(current_start, int(frame_start+frame_stride)))
			elif (current_start < int(frame_start+frame_stride)) and (current_start < abs_stop):
				segfile.write('%s %s\n'%(current_start, int(abs_stop)))
			#Wait to start next segment until find good data
			current_start = None
			current_stop = None

	cache.close()
	segfile.close()
	
	#Return injection flag
	return inj_flag

###
def merge_segs(seg_file):
	"""
	For a time-sorted segment list, combine segments that are divided at a common start/stop time
	"""
	#Load segments into an array
	seg_array = np.genfromtxt(seg_file).reshape((-1,2))
	
	#Open seg_file for overwriting
	write_seg_file = open(seg_file,'wt')
	
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
def executable(ifo, run_dic):
	"""
	"""
	#Grab necessary variables from run_dic
	framecache_file = run_dic['data']['cache files'][ifo]
	chname = run_dic['ifos'][ifo]['state channel name']
	abs_start = run_dic['times']['start']
	abs_stop = run_dic['times']['stop']
	outdir = '%s/segments/'%run_dic['seg dir']
	run_bitmask = run_dic['config']['run bitmask']
	inj_bitmask = run_dic['config']['inj bitmask']
	
	#Produce and merge segments from framecache state vectors
	inj_status = framecache2segs(framecache_file=framecache_file, chname=chname, abs_start=abs_start, abs_stop=abs_stop, outdir=outdir, ifo=ifo, run_bitmask=run_bitmask, inj_bitmask=inj_bitmask)
	try:
		merge_segs(seg_file='%s/%s_%s_%s.seg'%(outdir,ifo,abs_start,abs_stop))
	except IOError:
		pass
	return inj_status


##############################################
if __name__=='__main__':
	from optparse import OptionParser

	usage = None
	parser = OptionParser(usage=usage)

	parser.add_option("","--cache-file", default=None, type='string', help="Path to framecache file")
	parser.add_option("","--state-channel", default=None, type='string', help="Name of channel containing ifo state vector")
	parser.add_option("","--start", default=None, type='int', help="Absolute start time of segments")
	parser.add_option("","--stop", default=None, type='int', help="Absolute stop time of segments")
	parser.add_option("-o","--outdir", default=None, type="string", help="Path to directory in which to output segments")
	parser.add_option("-I","--IFO", default=None, type="string", help="Name of ifo, e.g., H1")
	parser.add_option("","--run-bitmask", default=None, type="int", help="Number corresponding to bitmask to search for")
	parser.add_option("","--inj-bitmask", default=None, type="int", help="Number corresponding to bitmask that signifies no injections are in the data")

	#---------------------------------------------

	opts, args = parser.parse_args()

	framecache_file = opts.cache_file
	chname = opts.state_channel
	abs_start = opts.start
	abs_stop = opts.stop
	outdir = opts.outdir
	ifo = opts.IFO
	run_bitmask = opts.run_bitmask
	inj_bitmask = opts.inj_bitmask
	
	#---------------------------------------------
	
	inj_status = framecache2segs(framecache_file=framecache_file, chname=chname, abs_start=abs_start, abs_stop=abs_stop, outdir=outdir, ifo=ifo, run_bitmask=run_bitmask, inj_bitmask=inj_bitmask)
	try:
		merge_segs(seg_file='%s/%s_%s_%s.seg'%(outdir,ifo,abs_start,abs_stop))
	except IOError:
		pass
	print inj_status

