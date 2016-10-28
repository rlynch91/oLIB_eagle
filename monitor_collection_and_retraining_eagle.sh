#!/bin/bash

#get options
while getopts ":u:i:d:l:" opt; do
  case $opt in
    u) user="$OPTARG"
    ;;
    i) infodir="$OPTARG"
    ;;
    d) rundic="$OPTARG"
    ;;
    l) runlabel="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

#check whether process is alive or not
process=`ps -Fu $user | grep collection_and_training_scheduler_eagle.py | grep $runlabel`

if [ -z "${process}" ]  #if process is an empty string, no realtime job exists
then

	current_gps_day=$((`lalapps_tconvert` / 100000))

	nohup $infodir/collection_and_training_scheduler_eagle.py -r $rundic -g None --run-label $runlabel > /dev/null 2>&1 &

fi

