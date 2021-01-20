import gc
import stt.task as t
import stt.scheduler as s
import stt.analyser as a
import stt.generator_WATERS as g
import stt.chain as c
import stt.transformer as trans
from stt.niklas import generate_cause_effect_chains_waters15
# from stt.niklas import generate_distributed_chain
from stt.niklas import generate_cause_effect_chains_from_transformed_task_sets
import stt.communication as communication
import csv
import argparse
import stt.evaluation as eva
import stt.generator_UUNIFAST as gm
import stt.eventSimulator as es
import math
import numpy as np

import random
import time

# Global Variables
task_sets = []
task_sets_communication = []
schedules = []
cause_effect_chain_sets = {"all": [], "ordered": [], "unordered": []}
cause_effect_chains_interconnected = {"all": [], "ordered": [], "unordered": []}

no_task_sets = 10
no_tasks = 50
total_time = 0.0

for util in [50,60,70,80,90]:
    print("Util:", util)

    ###
    # UUnifast by KHCHEN
    ###
    # task_sets_generator = gm.generate_tasksets(5, args.r, 1, 100, args.u, rounded=True)
    task_sets_generator = gm.generate_tasksets_predefined(no_tasks, no_task_sets, 1, 2000, float(util)/100.0, [1,2,5,10,20,50,100,200,500,1000])
    # Transform tasks and cause-effect chains into framework structure
    trans2 = trans.Transformer("transformer2", task_sets_generator, 10000000)
    # Transform tasks into framework model
    task_sets = trans2.transform_tasks(False) # we created all tasks to have bcet=0, we do not use this value in any analysis
    # Create cause-effect chains w.r.t the task sets
    # breakpoint()
    print("create cause-effect chains")
    cause_effect_chain_sets = generate_cause_effect_chains_from_transformed_task_sets(task_sets)


    # Create an analyzer to determine response times with TDA
    analyzer = a.Analyser("0")
    # TDA for each task set
    for idxx in range(len(task_sets)):
        # If TDA fails, remove task and chain set and continue
        try:
            # TDA
            i = 1
            for task in task_sets[idxx]:
                # Compute the worse case response time of the current task by TDA
                task.rt = analyzer.tda(task, task_sets[idxx][:(i - 1)])
                if task.rt > task.deadline or task.rt == 0:
                    # breakpoint()
                    raise ValueError("TDA Result: WCRT bigger than deadline or 0!")
                i += 1
        except ValueError: # if WCRT is bigger than deadline, then this task is removed from task set and cause effect chains
            task_sets.remove(task_sets[idxx])
            cause_effect_chain_sets.remove(cause_effect_chain_sets[idxx])
            # breakpoint()
            continue
    # Sporadic End-to-End Analyses
    print("test: davare")
    analyzer.davare(cause_effect_chain_sets) # e2e_latency
    print("test: reaction CASES19")
    analyzer.reaction_sporadic(cause_effect_chain_sets) #jj_react
    print("test: age CASES19")
    analyzer.age_sporadic(cause_effect_chain_sets) #jj_age

    tick = time.time()

    """
    Second Analyses (Simulation, Job Chains)
    """
    print("SIM TESTS")
    i = 0
    for task_set in task_sets:
        print("\ttask set ", i+1)
        print("\tsimulate")
        # Event-based simulator
        simulator = es.eventSimulator(len(task_set), task_set)
        # Determination of the variables used to compute the stop condition of the simulation
        max_e2e_latency = max(cause_effect_chain_sets[i], key=lambda chain: chain.e2e_latency).e2e_latency
        max_phase = max(task_set, key=lambda task: task.phase).phase
        max_period = max(task_set, key=lambda task: task.period).period
        hyper_period = analyzer.determine_hyper_period(task_set)
        period_lowest_priority_task = task_set[-1].period
        print("\t\tno of tasks: ", len(task_set))
        print("\t\thyperperiod: ", hyper_period)
        no_of_jobs = 0
        for task in task_set:
            no_of_jobs += (((2 * hyper_period + max_phase + max_period) / task.period) + max_e2e_latency / task.period)
        print("\t\tno of jobs to schedule:", no_of_jobs)
        # Stop condition is the max number of jobs from the lowest priority task; Note: this is just an estimation of the right end of both testing intervals plus job chain length; Since the schedule repeats, we can make this estimation
        simulator.dispatcher(int(math.ceil((2 * hyper_period + max_phase # interval to be scheduled
                                            + max_period + max_e2e_latency) # for convinience # TODO maybe one additional max_period ?
                                            / period_lowest_priority_task )))
        # Simulate
        schedule = simulator.e2e_result() # Note: the schedule is created without early completion
        #breakpoint()
        schedules.append(schedule)
        # for task in task_set:
        #    task.jobs = schedule[task]
        # Analyze the cause-effect chains
        chain = random.choice(cause_effect_chain_sets[i])
        # OUR RESULTS
        # print("\t\tCASES20: max age")
        # res0 = analyzer.max_age_CASES(schedule, chain, max_phase, hyper_period, args.s, extended=True) # CASES20 - our analysis
        # res0b = analyzer.max_age_CASES(schedule, chain, max_phase, hyper_period, args.s, extended=False) # CASES20 - our analysis
        print("\t\tOUR: max age")
        analyzer.max_age_OUR(schedule, task_set, chain, max_phase, hyper_period, shortened=False)
        # analyzer.max_age_OUR(schedule, task_set, chain, max_phase, hyper_period, shortened=True)
        print("\t\tOUR: reaction")
        analyzer.reaction_OUR(schedule, task_set, chain, max_phase, hyper_period)

        # # Kloda analysis, assuming synchronous releases
        # print("\t\tKloda for synchr")
        # for release_time_first_task_in_chain in range(0, max(1, hyper_period), chain.chain[0].period):
        #     kloda = analyzer.kloda(chain.chain, release_time_first_task_in_chain, beginning=True)
        #     if chain.kloda < kloda:
        #         chain.kloda = kloda # Kloda
        # # Note: additional period of the first task is already in the computation of kloda
        #
        # ###
        # if chain.kloda < chain.sim_react:
        #     breakpoint()
        i += 1
    tock=time.time()

    total_time += (tock-tick)

print(total_time)
print(total_time/(no_task_sets*5))
breakpoint()
