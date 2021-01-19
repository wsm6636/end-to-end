#!/bin/bash
for util in {50..90..10}
do
	echo "utilization: $util"
	date
	# 1 - 50
	echo "start screens 1 - 50"
	for i in {1..50}
	do
	   #echo "screen $i"
	   screen -dmS ascr$i python3 main.py -l1 -u=$util -g0 -r10 -n="run$i"
	done

	while screen -list | grep -q ascr.*
	do
		#screen -list
		sleep 1
	done
	echo "done 1 - 50"
	date
	
	# 51 - 100
	echo "start screens 51 - 100"
	for i in {51..100}
	do
	   #echo "screen $i"
	   screen -dmS ascr$i python3 main.py -l1 -u=$util -g0 -r10 -n="run$i"
	done
	
	while screen -list | grep -q ascr.*
	do
		#screen -list
		sleep 1
	done
	echo "done 51 - 100"
	date
done


for util in {50..90..10}
do
	echo "utilization: $util"
	date
	# 1 - 50
	echo "start screens 1 - 50"
	for i in {1..50}
	do
	   #echo "screen $i"
	   screen -dmS ascr$i python3 main.py -l1 -u=$util -g1 -r10 -n="run$i"
	done

	while screen -list | grep -q ascr.*
	do
		#screen -list
		sleep 1
	done
	echo "done 1 - 50"
	date
	
	# 51 - 100
	echo "start screens 51 - 100"
	for i in {51..100}
	do
	   #echo "screen $i"
	   screen -dmS ascr$i python3 main.py -l1 -u=$util -g1 -r10 -n="run$i"
	done
	
	while screen -list | grep -q ascr.*
	do
		#screen -list
		sleep 1
	done
	echo "done 51 - 100"
	date
done



# start high-level screen with:
# 	screen -dmS auto ./auto.sh
# if permission denied:
#	chmod +x test.sh 
#	ls -l

# start l2 with:
# 	for i in {50..90..10}; do  screen -dmS g0util_$i python3 main.py -l2 -u=$i -g0; done
# 	for i in {50..90..10}; do  screen -dmS g1util_$i python3 main.py -l2 -u=$i -g1; done

# start l3 with:
# 	screen -dmS l3g0 python3 main.py -l3 -g0
# 	screen -dmS l3g1 python3 main.py -l3 -g1