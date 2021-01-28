#!/bin/bash
#

###
# Specify number of recurrent jobs
###
if [ $# -eq 0 ]
then
  echo "Specify maximal number of recurrent jobs for the experiment (e.g. './auto.sh 5' )."
  exit 1
else
  var=$1
  echo "with $var recurrent jobs"
fi


###
# Timing
###
echo "===Timing behavior"
date

num_tries=10

for hyper in {0..4}
do
	echo "hyper $hyper"
	date
  for ((i=0;i<=num_tries;i++))
  # for i in {0..$num_tries}
	do
    # start a new screen
    screen -dmS ascr$i python3.7 hyperperiod_timing.py -s$hyper -r10 -n="$i"

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

python3.7 hyperperiod_timing.py -j1 -n$num_tries


echo "DONE"
date
