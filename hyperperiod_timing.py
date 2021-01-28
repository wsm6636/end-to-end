#!/usr/bin/env python3
"""Measure timing behavior for the single ECU case depending on hyperperiod."""

import random
import math
import utilities.generator_UUNIFAST as uunifast
import utilities.transformer as trans
import utilities.chain as ch
import utilities.analyzer as ana
import utilities.event_simulator as es


###
# Main function.
###

def main():
    """Main Function."""
    # User specific variables.
    # Hyperperiod as prime factorization:
    prime = [2, 2, 5, 5]  # 2*2*5*5 = 100
    # Number of tasks per task set:
    num_tasks = 10

    utilization = 50.0  # in percent

    # Other variables:
    total_time = 0.0  # count total time

    ###
    # Task set generation.
    ###
    print("Task set generation.")

    task_set_dic = []
    filters = []

    # Create filters.

    # First task filter with all 1 entries.
    filters.append(create_filter(prime, all_one=True))
    # Other task filters randomly.
    for idx in range(num_tasks-1):
        filters.append(create_filter(prime))

    # Translate to period. (Task set as list of dictionaries.)

    for idx in range(len(filters)):
        period = evaluate_filter(prime, filters[idx])
        task = {  # dictionary task
                'execution': 0,
                'period': period,
                'deadline': period
                }
        task_set_dic.append(task)
    if len(task_set_dic) != num_tasks:
        print("ERROR: Incorrect number of tasks.")
        breakpoint()

    # WCET

    # Pull utilizations with UUnifast.
    utils = uunifast.generate_utilizations_uniform(
            num_tasks, 1, utilization/100.0)[0]

    # print("Reached utilization:", sum(utils))

    # Match utilizations and period to get WCET.
    for idx in range(num_tasks):
        task_set_dic[idx]['execution'] = (task_set_dic[idx]['period']
                                          * utils[idx])

    # Task transformation.
    # - task dictionary -> task object
    # - order by period = ordered by priority
    # - set precision (by multiplication + rounding to integers)

    trans1 = trans.Transformer("1", [task_set_dic], 10000000)
    task_set = trans1.transform_tasks(False)[0]

    ###
    # Cause-effect chain generation.
    ###

    chain_len = 5  # number of tasks per chain

    if chain_len > len(task_set):
        print("ERROR: Not enough tasks for required chain length.")
        breakpoint()

    # Choose chain_len different tasks randomly and shuffled.
    ce_chain_as_list = random.sample(task_set, chain_len)

    # Transfer to ce-chain object.
    ce_chain = ch.CauseEffectChain(
            0,  # id of the chain
            ce_chain_as_list
    )

    ###
    # Time measurements.
    ###

    # Preperation.
    analyzer = ana.Analyzer("0")
    for idx in range(len(task_set)):
        task_set[idx].rt = analyzer.tda(task_set[idx], task_set[:idx])
        if task_set[idx].rt > task_set[idx].deadline:
            print("ERROR: Task set not schedulable.")
            return None  # TODO: what to return? or Cotinue/break? see main.py

    analyzer.davare([[ce_chain]])

    # Event-based simulation.
    print("Simulation.")

    simulator = es.eventSimulator(task_set)

    # Determination of the variables used to compute the stop
    # condition of the simulation
    max_e2e_latency = ce_chain.davare
    max_phase = 0
    hyperperiod = analyzer.determine_hyper_period(task_set)
    max_period = hyperperiod  # by definition of the first task in task_set_dic

    sched_interval = (
            2 * hyperperiod + max_phase  # interval from paper
            + max_e2e_latency  # upper bound job chain length
            + max_period)  # for convenience

    # Information for end user.
    print("\tNumber of tasks: ", len(task_set))
    print("\tHyperperiod: ", hyperperiod)
    number_of_jobs = 0
    for task in task_set:
        number_of_jobs += sched_interval/task.period
    print("\tNumber of jobs to schedule: ",
          "%.2f" % number_of_jobs)

    # Stop condition: Number of jobs of lowest priority task.
    simulator.dispatcher(
            int(math.ceil(sched_interval/task_set[-1].period)))

    # Simulation without early completion.
    schedule = simulator.e2e_result()

    analyzer.reaction_our(schedule, task_set, ce_chain, max_phase,
                          hyperperiod)

    breakpoint()


###
# Help functions.
###

def create_filter(prime, all_one=False):
    """Create a random filter for the period creation of a task."""
    filter = []
    for p in prime:
        if all_one:
            filter.append(1)
        else:
            filter_value = random.randint(0, 1)
            filter.append(filter_value)
    return filter


def evaluate_filter(prime, filter):
    """Evaluate a filter to obtain a task period."""
    if len(prime) != len(filter):
        print("ERROR: Filter and prime factorization have different length.")
        return 1
    period = 1
    for idx in range(len(filter)):
        if filter[idx] == 1:
            period = period * prime[idx]
    return period


if __name__ == '__main__':
    main()
