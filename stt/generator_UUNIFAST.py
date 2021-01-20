import numpy as np
import math
from scipy import stats
import stt.chain as c
import random

"""task sets
"""

# main functions

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

# help functions

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
        # print(sum(utilizations))
        return utilizations
    return [uunifast(num_tasks, utilization) for i in range(num_tasksets)]


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


"""cause effect chains
"""

# main function

def generate_cause_effect_chains_from_transformed_task_sets(transformed_task_sets): # UUNIFAST
    dis_number_tasks_in_cause_effect_chain = stats.rv_discrete(values=([2, 3, 4, 5], [0.3, 0.4, 0.2, 0.1]))
    cause_effect_chain_sets = []
    for task_set in transformed_task_sets:
        cause_effect_chain_set = []
        for i in range(int(np.random.randint(30, 60))):
            number_tasks_in_cause_effect_chain = dis_number_tasks_in_cause_effect_chain.rvs()
            periods = generate_involved_activation_patterns(task_set)
            np.random.shuffle(periods)
            load = 0
            chain = []
            for period in periods:
                runnables_with_periods = [task for task in task_set if task.period == period]
                size = int(np.ceil(number_tasks_in_cause_effect_chain / len(periods)))
                if load + size > number_tasks_in_cause_effect_chain:
                    size = number_tasks_in_cause_effect_chain - load
                else:
                    load += size
                if size > len(runnables_with_periods):
                    break
                for task in np.random.choice(runnables_with_periods, size=size, replace=False):
                    chain.append(task)
            if len(chain) > 1:
                cause_effect_chain_set.append(c.CauseEffectChain(i, chain))
        cause_effect_chain_sets.append(cause_effect_chain_set)
    return cause_effect_chain_sets

# help function

def generate_involved_activation_patterns(task_set): # Help for UUNIFAST
    dist_num_activation = stats.rv_discrete(values=([1, 2, 3], [0.7, 0.2, 0.1]))
    return list(np.random.choice(
        list(
            set(
                map(lambda task: task.period, task_set))), size=int(dist_num_activation.rvs()), replace=False))
