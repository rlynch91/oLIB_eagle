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
process=`ps -Fu $user | grep run_oLIB_eagle.py | grep $runlabel`

if [ -z "${process}" ]  #if process is an empty string, no realtime job exists
then
	export X509_USER_CERT=/home/ryan.lynch/2nd_pipeline/pipeline_eagle/robot_certificates/robot_cert.pem
	export X509_USER_KEY=/home/ryan.lynch/2nd_pipeline/pipeline_eagle/robot_certificates/robot_key.pem
	source /etc/profile.d/ligo.sh
	source /home/detchar/opt/virgosoft/environment.v2r1.sh
	source /home/salvatore.vitale/lalsuites/burst_dev/o2_lib_20160720/etc/env.sh

	nohup $infodir/email_if_falied_eagle.py -r $rundic > /dev/null 2>&1 &
	nohup $infodir/run_oLIB_eagle.py -r $rundic --run-label $runlabel > /dev/null 2>&1 &
fi
