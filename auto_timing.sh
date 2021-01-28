#!/bin/bash
#

###
# Specify number of concurrent jobs.
###
if [ $# -eq 0 ]
then
  echo "Specify maximal number of concurrent jobs for the experiment (e.g. './auto.sh 5' )."
  exit 1
else
  var=$1
  echo "with $var concurrent jobs"
fi


###
# Timing.
###
echo "===Timing behavior"
date

num_tries=4
runs_per_screen=2

# # Testing with different hyperperiods.
# for hyper in {0..9}
# do
# 	echo "hyper $hyper"
# 	date
#   for ((i=0;i<num_tries;i++))
# 	do
#     # start a new screen
#     screen -dmS ascr$hyper$i python3.7 hyperperiod_timing.py -pindex=$hyper -r$runs_per_screen -n$i -t50
#
#     numberrec=$(screen -list | grep -c ascr.*)
#
#     # wait until variable is reached
#     while (($numberrec >= $var))
#    	do
#    		sleep 1
#       numberrec=$(screen -list | grep -c ascr.*)
#    	done
# 	done
# done
#
# # wait until all are closed
# while screen -list | grep -q ascr.*
# do
#   sleep 1
# done

# Testing with different number of tasks.
for tasks in {0..9}
do
	echo "tasks $tasks"
	date
  for ((i=0;i<num_tries;i++))
	do
    # start a new screen
    screen -dmS ascr$tasks$i python3.7 hyperperiod_timing.py -tindex=$tasks -r$runs_per_screen -n$i -p4000

    numberrec=$(screen -list | grep -c ascr.*)

    # wait until variable is reached
    while (($numberrec >= $var))
   	do
   		sleep 1
      numberrec=$(screen -list | grep -c ascr.*)
   	done
	done
done

# wait until all are closed
while screen -list | grep -q ascr.*
do
  sleep 1
done

###
# Plotting.
###
echo "===Plot data"
# python3.7 hyperperiod_timing.py -j1 -n$num_tries -t50
python3.7 hyperperiod_timing.py -j2 -n$num_tries -p4000


echo "DONE"
date
