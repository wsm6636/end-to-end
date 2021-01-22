"""Task set and cause-effect chain generation with UUNIFAST benchmark.

From the paper: 'Measuring the performance of schedulability tests.' (2005).
"""
import numpy as np
from scipy import stats
import stt.chain as c
import random


# Main functions.

def gen_tasksets(num_tasks, num_tasksets, min_period, max_period, utilization,
                 rounded=False):
    """Generate task sets.

    Variables:
    num_tasks: number of tasks per set
    num_tasksets: number of sets
    min_period: minimal period
    max_period: maximal period
    utilization: desired utilization
    rounded: flag to round periods to integers
    """
    # Create periods.
    tasksets_periods = generate_periods_loguniform(
            num_tasks, num_tasksets, min_period, max_period, rounded)
    # Create utilizations.
    tasksets_utilizations = generate_utilizations_uniform(
            num_tasks, num_tasksets, utilization)
    # Create tasksets by matching both of the above.
    tasksets = []
    for i in range(num_tasksets):
        taskset = []
        for j in range(num_tasks):
            task = {
                    'execution': (tasksets_periods[i][j]
                                  * tasksets_utilizations[i][j]),
                    'period': tasksets_periods[i][j],
                    'deadline': tasksets_periods[i][j]
                    }
            taskset.append(task)
        tasksets.append(taskset)

    return tasksets


def gen_tasksets_pred(num_tasks, num_tasksets, min_period, max_period,
                      utilization, round_down_set):
    """Generate task sets with predefined period values.

    Variables:
    num_tasks: number of tasks per set
    num_tasksets: number of sets
    min_period: minimal period
    max_period: maximal period
    utilization: desired utilization
    round_down_set: predefined periods

    Note: max_period has to be higher than the highest entry in round_down_set
    to get periods also for the highest value.
    """
    # Create periods.
    tasksets_periods = generate_periods_loguniform_discrete(
            num_tasks, num_tasksets, min_period, max_period, round_down_set)
    # Create utilizations.
    tasksets_utilizations = generate_utilizations_uniform(
            num_tasks, num_tasksets, utilization)
    # Creating tasksets by matching both of the above.
    tasksets = []
    for i in range(num_tasksets):
        taskset = []
        for j in range(num_tasks):
            task = {
                    'execution': (tasksets_periods[i][j]
                                  * tasksets_utilizations[i][j]),
                    'period': tasksets_periods[i][j],
                    'deadline': tasksets_periods[i][j]
                    }
            taskset.append(task)
        tasksets.append(taskset)

    return tasksets


# help functions

def generate_periods_loguniform(num_tasks, num_tasksets, min_period,
                                max_period, rounded=False):
    """Generate log-uniformly distributed periods to create tasks.

    Variables:
    num_tasks: number of tasks per set
    num_tasksets: number of sets
    min_period: minimal period
    max_period: maximal period
    rounded: flag to round periods to integers
    """
    # Create random periods.
    periods = np.exp(np.random.uniform(
            low=np.log(min_period),
            high=np.log(max_period),
            size=(num_tasksets, num_tasks)))
    # Make list out of them
    if rounded:  # round periods to nearest integer
        return np.rint(periods).tolist()
    else:
        return periods.tolist()


def generate_periods_uniform(num_tasks, num_tasksets, min_period,
                             max_period, rounded=False):
    """Generate uniformly distributed periods to create tasks.

    Variables:
    num_tasks: number of tasks per set
    num_tasksets: number of sets
    min_period: minimal period
    max_period: maximal period
    rounded: flag to round periods to integers
    """
    # Create random periods.
    periods = np.random.uniform(
            low=min_period,
            high=max_period,
            size=(num_tasksets, num_tasks))
    # Make list out of them.
    if rounded:  # round periods to nearest integer
        return np.rint(periods).tolist()
    else:
        return periods.tolist()


def generate_utilizations_uniform(num_tasks, num_tasksets, utilization):
    """Generate utilizations with UUNIFAST.

    Variables:
    num_tasks: number of tasks per set
    num_tasksets: number of sets
    utilization: desired utilization
    """
    def uunifast(num_tasks, utilization):
        """UUNIFAST utilization pulling."""
        utilizations = []
        cumulative_utilization = utilization
        for i in range(1, num_tasks):
            # Randomly set next utilization.
            cumulative_utilization_next = (
                    cumulative_utilization
                    * random.random() ** (1.0/(num_tasks-i)))
            utilizations.append(
                    cumulative_utilization - cumulative_utilization_next)
            # Compute remaining utilization.
            cumulative_utilization = cumulative_utilization_next
        utilizations.append(cumulative_utilization_next)
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

def gen_ce_chains(transformed_task_sets): # UUNIFAST
    dis_number_tasks_in_cause_effect_chain = stats.rv_discrete(values=([2, 3, 4, 5], [0.3, 0.4, 0.2, 0.1]))
    ce_chains = []
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
        ce_chains.append(cause_effect_chain_set)
    return ce_chains

# help function

def generate_involved_activation_patterns(task_set): # Help for UUNIFAST
    dist_num_activation = stats.rv_discrete(values=([1, 2, 3], [0.7, 0.2, 0.1]))
    return list(np.random.choice(
        list(
            set(
                map(lambda task: task.period, task_set))), size=int(dist_num_activation.rvs()), replace=False))
