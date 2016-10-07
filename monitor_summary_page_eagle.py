#!/bin/bash

#get options
while getopts ":u:i:d:l:g:" opt; do
  case $opt in
    u) user="$OPTARG"
    ;;
    i) infodir="$OPTARG"
    ;;
    d) rundic="$OPTARG"
    ;;
    l) runlabel="$OPTARG"
    ;;
    g) ifogroup="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

#check whether process is alive or not
process=`ps -Fu $user | grep summary_page_eagle.py | grep $runlabel`

if [ -z "${process}" ]  #if process is an empty string, no realtime job exists
then

	current_gps_time=`lalapps_tconvert`

	nohup $infodir/summary_page_eagle.py -r $rundic -g $current_gps_time -i $ifogroup --run-label $runlabel > /dev/null 2>&1 &

fi
