#!/bin/bash

### check whether process is alive or not
process=`ps -Fu ryan.lynch | grep launch_oLIB_eagle.py | grep /usr/bin/python`

if [ -z "${process}" ] ### if process is an empty string, no realtime job exists
then
	export X509_USER_CERT=/home/ryan.lynch/2nd_pipeline/pipeline_eagle/robot_certificates/robot_cert.pem
	export X509_USER_KEY=/home/ryan.lynch/2nd_pipeline/pipeline_eagle/robot_certificates/robot_key.pem
	source /etc/profile.d/ligo.sh
	source /home/detchar/opt/virgosoft/environment.v2r1.sh
	source /home/salvatore.vitale/lalsuites/burst_dev/o2_lib_20160720/etc/env.sh

	nohup /home/ryan.lynch/2nd_pipeline/pipeline_eagle/launch_oLIB_eagle.py > /dev/null 2>&1 &
fi
