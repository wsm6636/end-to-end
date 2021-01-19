import numpy as np
import random
import math
import stt.task as task

CAN_BUS = {
	'MESSAGE_BIT' : 130,
	'BANDWIDTH_MBPS' : 1,
	'MAX_NODES' : 5
	}


def non_preemptive_response_time(taskset):
	def time_demand_analysis_task(pivot, lower_prio_tasks=[], higher_prio_tasks=[], blocking=False):
		blocked = max(task.wcet for task in lower_prio_tasks) if lower_prio_tasks else 0
		probe = blocked + pivot.wcet + sum((task.wcet for task in higher_prio_tasks))
		workload = 0
		while probe <= pivot.deadline:
			workload = blocked + task.wcet + sum((math.ceil(float(probe)/task.period)*task.wcet for task in higher_prio_tasks))
			if not (workload > probe):
				return workload
			else:
				probe = workload
		return False
	for i, task in enumerate(taskset):
		rt = time_demand_analysis_task(task, taskset[i+1:], taskset[:i], True)
		if rt > task.deadline:
			return False
		task.rt = rt


def generate_communication_candidate_taskset(num_tasks, min_period, max_period, rounded=False):
	taskset = []
	wcet = (float(CAN_BUS['MESSAGE_BIT'])/CAN_BUS['BANDWIDTH_MBPS'])/10**3
	periods = np.exp(
		np.random.uniform(low=np.log(min_period), high=np.log(max_period), size=num_tasks))
	periods = np.rint(periods).tolist() if rounded else periods
	prio = list(range(num_tasks))
	random.shuffle(prio)
	for i in range(num_tasks):
		taskset.append(task.Task(i, 0, wcet, wcet, periods[i], periods[i], prio[i], True))
	return taskset


def generate_communication_taskset(num_tasks, min_period, max_period, rounded=False, max_trials=100):
	taskset = generate_communication_candidate_taskset(num_tasks, min_period, max_period, rounded)
	taskset = sorted(taskset, key=lambda x: x.priority)
	trials = 0
	while True and (trials < max_trials):
		if not (non_preemptive_response_time(taskset) is False):
			return taskset
		trials+=1
	return False
