#!/bin/bash
#

###
# Specify number of concurrent instances.
###
if [ $# -eq 0 ]
then
  echo "Specify maximal number of concurrent instances for the experiment (e.g. './auto.sh 5' )."
  exit 1
else
  var=$1
  echo "with $var concurrent instances"
fi


###
# Timing.
###
echo "===Run Experiment"
date

num_tries=2
runs_per_screen=5

num_task_ind=4

for ((j=0;j<num_task_ind;j++))
do
  echo "task index $j"
  for ((i=0;i<4*num_tries;i+=4))
  do
    echo "start instance $i"
    screen -dmS ascr$i python3.7 runtime_tasks.py -n$i -timeout=5 -tindex=$j -r$runs_per_screen -hypermin=0 -hypermax=1000

    # wait until variable is reached
    numberrec=$(screen -list | grep -c ascr.*)
    while (($numberrec >= $var))
    do
      sleep 1
      numberrec=$(screen -list | grep -c ascr.*)
    done

    echo "start instance $((i+1))"
    screen -dmS ascr$i python3.7 runtime_tasks.py -n$((i+1)) -timeout=5 -tindex=$j -r$runs_per_screen -hypermin=1000 -hypermax=3000

    # wait until variable is reached
    numberrec=$(screen -list | grep -c ascr.*)
    while (($numberrec >= $var))
    do
      sleep 1
      numberrec=$(screen -list | grep -c ascr.*)
    done

    echo "start instance $((i+2))"
    screen -dmS ascr$i python3.7 runtime_tasks.py -n$((i+2)) -timeout=5 -tindex=$j -r$runs_per_screen -hypermin=3000 -hypermax=5000

    # wait until variable is reached
    numberrec=$(screen -list | grep -c ascr.*)
    while (($numberrec >= $var))
    do
      sleep 1
      numberrec=$(screen -list | grep -c ascr.*)
    done

    echo "start instance $((i+3))"
    screen -dmS ascr$i python3.7 runtime_tasks.py -n$((i+3)) -timeout=5 -tindex=$j -r$runs_per_screen -hypermin=5000 -hypermax=-1

    # wait until variable is reached
    numberrec=$(screen -list | grep -c ascr.*)
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
python3.7 runtime_tasks.py -j1 -n=$((4*num_tries))


echo "DONE"
date
