#!/bin/bash

### check whether process is alive or not
process=`ps -Fu ryan.lynch | grep collection_and_training_scheduler_eagle.py | grep /usr/bin/python`

if [ -z "${process}" ] ### if process is an empty string, no realtime job exists
then

	current_gps_day=$((`lalapps_tconvert` / 100000))

        nohup /home/ryan.lynch/2nd_pipeline/pipeline_eagle/collection_and_training_scheduler_eagle.py --gps-day-collect $current_gps_day --ifo-groups H1L1 --infodir /home/ryan.lynch/2nd_pipeline/pipeline_eagle/ --rundir /home/ryan.lynch/public_html/S6_replay --collectdir /home/ryan.lynch/2nd_pipeline/pipeline_eagle/test_results --backdir /home/ryan.lynch/2nd_pipeline/pipeline_eagle/test_background_info --retraindir /home/ryan.lynch/2nd_pipeline/pipeline_eagle/test_LLRT_info --last-gps-day-path /home/ryan.lynch/public_html/S6_replay/last_gps_day_collected_and_trained.pkl --bindir /home/salvatore.vitale/lalsuites/burst_dev/o2_lib_20160720/bin/ --max-back-size 5000 --max-signal-size 5000 --max-noise-size 5000 --train-details-dic /home/ryan.lynch/2nd_pipeline/pipeline_eagle/test_LLRT_info/training_details_dictionary.pkl --train-bin low_f &

fi

