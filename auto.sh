#!/bin/bash
#
# Automatic Evaluation for the paper 'Timing Analysis of Asynchronized Distributed Cause-Effect Chains' (2021).

########################################
# Start this shell script with
# 	screen -dmS auto ./auto.sh
# We use the screen command to parallelize the execution.
# 'screen -ls' shows all current screens
# 'killall screen' aborts all current screens.
########################################

###
# Single ECU analysis
###

echo "===Start single ECU analysis"
date
# g=0 r=10 with different utilization
for util in {50..90..10}
do
	echo "utilization: $util"
	date
	# Start the first 50 screens.
	echo "start screens 1 - 50"
	for i in {1..50}
	do
	   screen -dmS ascr$i python3.7 main.py -j1 -u=$util -g0 -r10 -n="run$i"
	done

	while screen -list | grep -q ascr.*
	do
		sleep 1
	done
	echo "done 1 - 50"
	date

	# Start the second 50 screens.
	echo "start screens 51 - 100"
	for i in {51..100}
	do
	   screen -dmS ascr$i python3.7 main.py -j1 -u=$util -g0 -r10 -n="run$i"
	done

	while screen -list | grep -q ascr.*
	do
		sleep 1
	done
	echo "done 51 - 100"
	date
  echo " "
done

# g=1 r=10 with different utilization
for util in {50..90..10}
do
	echo "utilization: $util"
	date
	# Start the first 50 screens.
	echo "start screens 1 - 50"
	for i in {1..50}
	do
	   screen -dmS ascr$i python3.7 main.py -j1 -u=$util -g1 -r10 -n="run$i"
	done

	while screen -list | grep -q ascr.*
	do
		sleep 1
	done
	echo "done 1 - 50"
	date

	# Start the second 50 screens.
	echo "start screens 51 - 100"
	for i in {51..100}
	do
	   screen -dmS ascr$i python3.7 main.py -j1 -u=$util -g1 -r10 -n="run$i"
	done

	while screen -list | grep -q ascr.*
	do
		sleep 1
	done
	echo "done 51 - 100"
	date
  echo " "
done

###
# Interconnected ECU analysis.
###
# Or manually with:
# 	for i in {50..90..10}; do  screen -dmS g0util_$i python3 main.py -j2 -u=$i -g0; done
# 	for i in {50..90..10}; do  screen -dmS g1util_$i python3 main.py -j2 -u=$i -g1; done
###

echo "===Start interconnected ECU analysis"
date

for i in {50..90..10}
do
  screen -dmS ascrg0util_$i python3.7 main.py -j2 -u=$i -g0
done
for i in {50..90..10}
do
  screen -dmS ascrg1util_$i python3.7 main.py -j2 -u=$i -g1
done
while screen -list | grep -q ascr.*
do
  sleep 1
done

echo " "

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
