from scipy import stats
import numpy as np
import stt.chain as c
import random

def generate_involved_activation_patterns(task_set): # Help for UUNIFAST
    dist_num_activation = stats.rv_discrete(values=([1, 2, 3], [0.7, 0.2, 0.1]))
    return list(np.random.choice(
        list(
            set(
                map(lambda task: task.period, task_set))), size=int(dist_num_activation.rvs()), replace=False))


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

def generate_cause_effect_chains_waters15(transformed_task_sets, sort): # WATERS
    distribution_involved_activation_patterns = stats.rv_discrete(values=([1, 2, 3], [0.7, 0.2, 0.1]))
    distribution_number_of_tasks = stats.rv_discrete(values=([2, 3, 4, 5], [0.3, 0.4, 0.2, 0.1]))
    cause_effect_chain_sets = []

    for task_set in transformed_task_sets:
        cause_effect_chain_set = []
        for number_of_cause_effect_chains in range(int(np.random.randint(30, 60))): # 30 to 60 cause-effect chains
            chain = []
            involved_activation_patterns = list(np.random.choice(list(set(map(lambda task: task.period, task_set))),
                                                                 size=int(
                                                                     distribution_involved_activation_patterns.rvs()),
                                                                 replace=False))
            if sort:
                involved_activation_patterns.sort()
            else:
                np.random.shuffle(involved_activation_patterns)

            for period in involved_activation_patterns:
                tasks_with_period = [task for task in task_set if task.period == period]
                try:
                    chain.append(
                        np.random.choice(tasks_with_period, size=distribution_number_of_tasks.rvs(), replace=False))
                except ValueError:
                    chain = []
                    break
            cec_chain = []
            for chain_part in chain:
                for task in chain_part:
                    cec_chain.append(task)
            if chain:
                cause_effect_chain_set.append(c.CauseEffectChain(number_of_cause_effect_chains, cec_chain))
        cause_effect_chain_sets.append(cause_effect_chain_set)
    return cause_effect_chain_sets
