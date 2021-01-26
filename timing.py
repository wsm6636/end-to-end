#!/usr/bin/env python3
"""Measure timing behavior for the single ECU case."""

import gc  # garbage collector
import argparse
import math
import numpy as np
import utilities.chain as c
import utilities.communication as comm
import utilities.generator_WATERS as waters
import utilities.generator_UUNIFAST as uunifast
import utilities.transformer as trans
import utilities.event_simulator as es
import utilities.analyzer as a
import utilities.evaluation as eva
import random
import time

# Variables:
number_task_sets = 10
number_tasks = 50

total_time = 0.0


for util in [50, 60, 70, 80, 90]:
    print("Util:", util)

    ###
    # Task set and cause-effect chain generation.
    ###
    print("=Task set and cause-effect chain generation.=")

    # UUnifast benchmark.
    print("UUnifast benchmark.")

    # Create task sets from the generator.
    print("\tCreate task sets.")

    # # Generate log-uniformly distributed task sets:
    # task_sets_generator = uunifast.gen_tasksets(
    #         5, args.r, 1, 100, args.u, rounded=True)

    # Generate log-uniformly distributed task sets with predefined
    # periods:
    periods = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    # Interval from where the generator pulls log-uniformly.
    min_pull = 1
    max_pull = 2000

    task_sets_uunifast = uunifast.gen_tasksets_pred(
            50, args.r, min_pull, max_pull, args.u/100.0, periods)

    # Transform tasks to fit framework structure.
    trans2 = trans.Transformer("2", task_sets_uunifast, 10000000)
    task_sets = trans2.transform_tasks(False)

    # Create cause-effect chains.
    print("\tCreate cause-effect chains")
    ce_chains = uunifast.gen_ce_chains(task_sets)
    # ce_chains contains one set of cause effect chains for each task
    # set in task_sets.

    ###
    # First analyses (TDA, Davare, Duerr).
    ###
    print("=First analyses (TDA, Davare, Duerr).=")
    analyzer = a.Analyzer("0")

    # TDA for each task set.
    print("TDA.")
    for idxx in range(len(task_sets)):
        try:
            # TDA.
            i = 1
            for task in task_sets[idxx]:
                task.rt = analyzer.tda(task, task_sets[idxx][:(i - 1)])
                if task.rt > task.deadline:
                    raise ValueError(
                            "TDA Result: WCRT bigger than deadline!")
                i += 1
        except ValueError:
            # If TDA fails, remove task and chain set and continue.
            task_sets.remove(task_sets[idxx])
            ce_chains.remove(ce_chains[idxx])
            continue

    # End-to-End Analyses.
    print("Test: Davare.")
    analyzer.davare(ce_chains)

    print("Test: Duerr Reaction Time.")
    analyzer.reaction_duerr(ce_chains)

    print("Test: Duerr Data Age.")
    analyzer.age_duerr(ce_chains)

    # Start timer.
    tick = time.time()

    ###
    # Second analyses (Simulation, Our, Kloda).
    ###
    print("=Second analyses (Simulation, Our, Kloda).=")
    i = 0  # task set counter
    schedules = []
    for task_set in task_sets:
        print("=Task set ", i+1)

        # Event-based simulation.
        print("Simulation.")

        simulator = es.eventSimulator(task_set)

        # Determination of the variables used to compute the stop condition
        # of the simulation
        max_e2e_latency = max(ce_chains[i], key=lambda chain:
                              chain.davare).davare
        max_phase = max(task_set, key=lambda task: task.phase).phase
        max_period = max(task_set, key=lambda task: task.period).period
        hyper_period = analyzer.determine_hyper_period(task_set)

        sched_interval = (
                2 * hyper_period + max_phase  # interval from paper
                + max_e2e_latency  # upper bound job chain length
                + max_period)  # for convenience

        # Information for end user.
        print("\tNumber of tasks: ", len(task_set))
        print("\tHyperperiod: ", hyper_period)
        number_of_jobs = 0
        for task in task_set:
            number_of_jobs += sched_interval/task.period
        print("\tNumber of jobs to schedule: ", number_of_jobs)

        # Stop condition: Number of jobs of lowest priority task.
        simulator.dispatcher(
                int(math.ceil(sched_interval/task_set[-1].period)))

        # Simulation without early completion.
        schedule = simulator.e2e_result()
        schedules.append(schedule)

        # Analyses.
        for chain in ce_chains[i]:
            print("Test: Our Data Age.")
            analyzer.max_age_our(schedule, task_set, chain, max_phase,
                                 hyper_period, shortened=False)
            # analyzer.max_age_our(schedule, task_set, chain, max_phase,
            #                      hyper_period, shortened=True)

            print("Test: Our Reaction Time.")
            analyzer.reaction_our(schedule, task_set, chain, max_phase,
                                  hyper_period)

            # # Kloda analysis, assuming synchronous releases.
            # print("Test: Kloda.")
            # analyzer.kloda(chain, hyper_period)
            #
            # # Test.
            # if chain.kloda < chain.our_react:
            #     breakpoint()
        i += 1

    # Stop timer.
    tock = time.time()

    # Compute total time.
    total_time += (tock-tick)

# Timing results.
print(total_time)
print(total_time/(number_task_sets*5))
breakpoint()
