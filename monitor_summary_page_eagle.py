#!/bin/bash

### check whether process is alive or not
process=`ps -Fu ryan.lynch | grep summary_page_beta.py | grep /usr/bin/python`

if [ -z "${process}" ] ### if process is an empty string, no realtime job exists
then
	timestamp_gps=`lalapps_tconvert`
	timestamp_utc=`lalapps_tconvert -d`
	echo 'GPS: ' $timestamp_gps > /home/ryan.lynch/public_html/O1_summary_live/timestamp.txt
	echo 'UTC: ' $timestamp_utc >> /home/ryan.lynch/public_html/O1_summary_live/timestamp.txt

	nohup /home/ryan.lynch/2nd_pipeline/pipeline_O1/summary_page_beta.py --gpstime=$timestamp_gps --datadir=/home/ryan.lynch/public_html/O1_0lag/ --outdir=/home/ryan.lynch/public_html/O1_summary_live/ --label=full &

fi
