import numpy as np
import math
import random

def generate_periods_loguniform(num_tasks, num_tasksets, min_period, max_period, rounded=False):
    periods = np.exp(np.random.uniform(low=np.log(min_period), high=np.log(max_period), size=(num_tasksets, num_tasks)))
    if rounded:
        return np.rint(periods).tolist()
    else:
        return periods.tolist()

def generate_periods_uniform(num_tasks, num_tasksets, min_period, max_period, rounded=False):
    periods = np.random.uniform(low=min_period, high=max_period, size=(num_tasksets, num_tasks))
    if rounded:
        return np.rint(periods).tolist()
    else:
        return periods.tolist()


def generate_utilizations_uniform(num_tasks, num_tasksets, utilization):
    def uunifast(num_tasks, utilization):
        utilizations = []
        cumulative_utilization = utilization
        for i in range(1, num_tasks):
            cumulative_utilization_next = cumulative_utilization * random.random() ** (1.0 / (num_tasks - i))
            utilizations.append(cumulative_utilization - cumulative_utilization_next)
            cumulative_utilization = cumulative_utilization_next
        utilizations.append(cumulative_utilization_next)
        #print(sum(utilizations))
        return utilizations
    return [uunifast(num_tasks, utilization) for i in range(num_tasksets)]


def min_distance(chain):
    sequence = [task['id'] for task in chain]

def generate_chains(tasksets, min_tasks, max_tasks):
    chain_sets = []
    for taskset in tasksets:
        chain_set = []
        for id, task in enumerate(taskset):
            task['id'] = id
            chain_set.append(list(np.random.choice(taskset, np.random.randint(min_tasks, max_tasks), replace = False)))
        chain_sets.append(chain_set)
    return chain_sets

def generate_tasksets(num_tasks, num_tasksets, min_period, max_period, utilization, min_scale=1, max_scale=1, rounded = False):
    tasksets_periods = generate_periods_loguniform(num_tasks, num_tasksets, min_period, max_period, rounded)
    tasksets_utilizations = generate_utilizations_uniform(num_tasks, num_tasksets, utilization)
    tasksets = []
    for i in range(num_tasksets):
        taskset =  []
        for j in range(num_tasks):
            #task = {'execution' : tasksets_periods[i][j]*tasksets_utilizations[i][j], 'period' : tasksets_periods[i][j], 'inter_arrival_max' : tasksets_periods[i][j] * np.random.uniform(min_scale, max_scale)}
            task = {'execution' : tasksets_periods[i][j]*tasksets_utilizations[i][j], 'period' : tasksets_periods[i][j], 'deadline': tasksets_periods[i][j]}
            taskset.append(task)
        tasksets.append(taskset)
    return tasksets


def generate_periods_loguniform_discrete(num_tasks, num_tasksets, min_period, max_period, round_down_set): # Note: max_period has to be higher than the highest entry in round_down_set to also get periods for the highest value
    # Create periods log-uniformly
    period_sets = generate_periods_loguniform(num_tasks, num_tasksets, min_period, max_period, rounded=False)
    # Round down to the entries of the set
    rounded_period_sets = []
    round_down_set.sort(reverse=True)
    for i in range(len(period_sets)):
        rounded_period_sets.append([])
        for p in period_sets[i]:
            for r in round_down_set:
                if p>=r:
                    rp=r
                    break
            rounded_period_sets[i].append(rp)
    return rounded_period_sets

def generate_tasksets_predefined(num_tasks, num_tasksets, min_period, max_period, utilization, round_down_set, min_scale=1, max_scale=1):
    # Note: max_period has to be higher than the highest entry in round_down_set to also get periods for the highest value
    tasksets_periods = generate_periods_loguniform_discrete(num_tasks, num_tasksets, min_period, max_period, round_down_set)
    tasksets_utilizations = generate_utilizations_uniform(num_tasks, num_tasksets, utilization)
    tasksets = []
    for i in range(num_tasksets):
        taskset =  []
        for j in range(num_tasks):
            #task = {'execution' : tasksets_periods[i][j]*tasksets_utilizations[i][j], 'period' : tasksets_periods[i][j], 'inter_arrival_max' : tasksets_periods[i][j] * np.random.uniform(min_scale, max_scale)}
            task = {'execution' : tasksets_periods[i][j]*tasksets_utilizations[i][j], 'period' : tasksets_periods[i][j], 'deadline': tasksets_periods[i][j]}
            taskset.append(task)
        tasksets.append(taskset)
    return tasksets
