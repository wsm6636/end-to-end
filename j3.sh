#!/bin/bash
#
# Automatic Evaluation for the paper 'Timing Analysis of Asynchronized Distributed Cause-Effect Chains' (2021).

########################################
# Start this shell script with
# 	./auto.sh x
# where x should be replace by the number of maximal concurrent jobs (typically not more than free processor of the machine that is used)
###
# We use the screen command to parallelize the execution.
# 'screen -ls' shows all current screens
# 'killall screen' aborts all current screens.
########################################

###
# Specify number of concurrent jobs
# 最大并发作业量
###
if [ $# -eq 0 ]
then
  echo "Specify maximal number of concurrent jobs for the experiment (e.g. './auto.sh 5' )."
  exit 1
else
  var=$1
  echo "with $var concurrent jobs"
fi

num_tries=100  # number of runs，跑多少次,原来是100
runs_per_screen=10  # number of runs per screen，一次跑几个screen


###
# Draw plots.
###
# Or manually with:
# 	screen -dmS j3g0 python3 main.py -j3 -g0
# 	screen -dmS j3g1 python3 main.py -j3 -g1
###

echo "===Draw plots."
date

screen -dmS ascrj3g0 python3.7 main.py -j3 -g0
screen -dmS ascrj3g1 python3.7 main.py -j3 -g1
while screen -list | grep -q ascr.*
do
  sleep 1
done

echo "DONE"
date

# echo "rm ./output/1single/*.npz"
# rm ./output/1single/*.npz
# date

# echo "rm ./output/2interconn/*.npz"
# rm ./output/2interconn/*.npz
# date