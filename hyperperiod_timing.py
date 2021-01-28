#!/usr/bin/env python3
"""Measure timing behavior for the single ECU case depending on hyperperiod."""

import argparse
import random
import math
import time
import numpy as np
import matplotlib.pyplot as plt
import utilities.generator_UUNIFAST as uunifast
import utilities.transformer as trans
import utilities.chain as ch
import utilities.analyzer as ana
import utilities.event_simulator as es

###
# Argument Parser
###
parser = argparse.ArgumentParser()

# number of the run:
parser.add_argument("-n", type=int, default=-1)

# number of tasks:
parser.add_argument("-t", type=int, default=50)

# number of tasks from list:
parser.add_argument("-tindex", type=int, default=-1)

# hyperperiod:
parser.add_argument("-p", type=int, default=2000)

# hyperperiod from list:
parser.add_argument("-pindex", type=int, default=-1)

# number of runs:
parser.add_argument("-r", type=int, default=1)

# flag to plot results in list:
# - j=1 hyperperiod on xaxis
# - j=2 number of tasks on xaxis
# --> for plotting, the max number of runs has to be specified by args.n
parser.add_argument("-j", type=int, default=0)

args = parser.parse_args()
del parser


###
# Main function.
###

def main():
    """Main Function."""

    # hyperperiod_factorizations = [
    #     [2, 2, 2, 2, 5, 5, 5, 5],  # 10000
    #     [2, 2, 2, 2, 2, 5, 5, 5, 5],  # 20000
    #     [2, 2, 2, 2, 3, 5, 5, 5, 5],  # 30000
    #     [2, 2, 2, 2, 2, 2, 5, 5, 5, 5],  # 40000
    #     [2, 2, 2, 2, 5, 5, 5, 5, 5],  # 50000
    #     [2, 2, 2, 2, 2, 3, 5, 5, 5, 5],  # 60000
    #     [2, 2, 2, 2, 5, 5, 5, 5, 7],  # 70000
    #     [2, 2, 2, 2, 2, 2, 2, 5, 5, 5, 5],  # 80000
    #     [2, 2, 2, 2, 3, 3, 5, 5, 5, 5],  # 90000
    #     [2, 2, 2, 2, 2, 5, 5, 5, 5, 5]  # 100000
    #     ]

    # hyperperiod_factorizations = [
    #     [2, 5],  # 10
    #     [2, 2, 5, 5],  # 10^2
    #     [2, 2, 2, 5, 5, 5],  # 10^3
    #     [2, 2, 2, 2, 5, 5, 5, 5],  # 10^4
    #     ]

    hyperperiod_factorizations = [
        [2, 2, 2, 2, 5, 5, 5],  # 2000
        [2, 2, 2, 2, 2, 5, 5, 5],  # 4000
        [2, 2, 2, 2, 3, 5, 5, 5],  # 6000
        [2, 2, 2, 2, 2, 2, 5, 5, 5],  # 8000
        [2, 2, 2, 2, 5, 5, 5, 5]  # 10000
        ]

    hyperperiod_factorizations = []

    task_numbers = [
        20,
        40,
        60,
        80,
        100
    ]

    ###
    # Plotting. (j != 0)
    ###

    if args.j != 0:
        if args.n == -1:
            print("ERROR: The number of runs is not specified.")
            return

        # Plot with hyperperiods on xaxis.
        if args.j == 1:
            # Compute predefined hyperperiods.
            pred_hyperperiods = []
            for fac in hyperperiod_factorizations:
                hyp = 1
                for val in fac:
                    hyp *= val
                pred_hyperperiods.append(hyp)
            # plot
            plot_results_hyperperiod(
                    pred_hyperperiods,
                    args.t,
                    args.n)
            return

        # Plot with number of tasks on xaxis.
        if args.j == 2:
            # compute predefined hyperperiods
            pred_hyperperiods = []
            for fac in hyperperiod_factorizations:
                hyp = 1
                for val in fac:
                    hyp *= val
                pred_hyperperiods.append(hyp)
            # plot
            plot_results_numbertasks(
                    args.p,
                    task_numbers,
                    args.n)
            return

        return

    ###
    # Experiment. (j == 0)
    ###

    # Choose hyperperiod:
    try:
        if args.pindex == -1:
            prime = prime_factorization(args.p)
        else:
            prime = hyperperiod_factorizations[args.pindex]
    except Exception as e:
        print(e)
        print("ERROR: Hyperperiod could not be chosen.")
        return

    # Choose number of tasks:
    try:
        if args.tindex == -1:
            num_tasks = args.t
        else:
            num_tasks = task_numbers[args.tindex]
    except Exception as e:
        print(e)
        print("ERROR: Number of tasks could not be chosen.")
        return

    # Other variables:
    utilization = 50.0  # in percent

    ###
    # Task set generation.
    ###
    print("Task set generation.")
    task_sets = []
    for _ in range(args.r):
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

        task_sets.append(task_set)

    ###
    # Cause-effect chain generation.
    ###

    chain_len = 5  # number of tasks per chain

    ce_chains = []

    for task_set in task_sets:
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

        ce_chains.append(ce_chain)

    ###
    # Time measurements.
    ###
    if len(task_sets) != len(ce_chains):
        print("ERROR: Number of task sets and ce chains is different.")
        return

    timings = []

    for task_set, ce_chain in zip(task_sets, ce_chains):
        # Start timer.
        tick = time.time()

        # Preperation.
        analyzer = ana.Analyzer("0")
        for idx in range(len(task_set)):
            task_set[idx].rt = analyzer.tda(task_set[idx], task_set[:idx])
            if task_set[idx].rt > task_set[idx].deadline:
                print("ERROR: Task set not schedulable.")
                return

        analyzer.davare([[ce_chain]])

        # Event-based simulation.
        print("Simulation.")

        simulator = es.eventSimulator(task_set)

        # Determination of the variables used to compute the stop
        # condition of the simulation
        max_e2e_latency = ce_chain.davare
        max_phase = 0  # by definition
        hyperperiod = analyzer.determine_hyper_period(task_set)
        max_period = hyperperiod  # by definition of task_set_dic

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

        # Stop timer.
        tock = time.time()

        # Time difference.
        timing = tock-tick
        print(timing, 'seconds')

        timings.append(timing)

    ###
    # Save data.
    ###

    try:
        # compute hyperperiod to display
        hyperperiod = 1
        for p in prime:
            hyperperiod *= p
        np.savez("output/timing/"
                 + "hyper_" + str(hyperperiod)
                 + "_#tasks_" + str(num_tasks)
                 + "_run_" + str(args.n)
                 + ".npz",
                 timings=timings)
    except Exception as e:
        print(e)
        print("ERROR: save")
        breakpoint()

    return


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


def prime_factorization(number):
    if number < 1 or number % 1 != 0:
        print("ERROR: No prime factorization possible")
        return []
    prime_list = []
    idx = 2
    while number > 1:
        while number % idx == 0:
            prime_list.append(idx)
            number = number / idx
        idx += 1
    return prime_list


def plot_results_hyperperiod(
        hyperperiods,
        number_tasks,
        number):  # number of runs to collect data from

    try:
        ###
        # Load data.
        ###
        results = []  # lists of timing results (one list for each hyperperiod)
        for hyperperiod in hyperperiods:
            hyper_results = []  # results for one specific hyperperiod
            for idx in range(number):
                data = np.load("output/timing/"
                               + "hyper_" + str(hyperperiod)
                               + "_#tasks_" + str(number_tasks)
                               + "_run_" + str(idx)
                               + ".npz",
                               allow_pickle=True)

                # Interconnected.
                hyper_results += list(data.f.timings)

                # Close data file and run the garbage collector.
                data.close()
            results.append(hyper_results)
    except Exception as e:
        print(e)
        print("ERROR: inputs for plotter are missing")
        breakpoint()

    ###
    # Plot result.
    ###
    draw_boxplots(
            results, "output/timing/results_hyper.pdf",
            xlabels=hyperperiods,
            xaxis_label="hyperperiod",
            yaxis_label="time for execution [s]")


def plot_results_numbertasks(
        hyperperiod,
        numbers_tasks,
        number):  # number of runs to collect data from

    try:
        ###
        # Load data.
        ###
        results = []  # lists of timing results (one list for each hyperperiod)
        for number_tasks in numbers_tasks:
            number_results = []  # results for one specific task number
            for idx in range(number):
                data = np.load("output/timing/"
                               + "hyper_" + str(hyperperiod)
                               + "_#tasks_" + str(number_tasks)
                               + "_run_" + str(idx)
                               + ".npz",
                               allow_pickle=True)

                # Interconnected.
                number_results += list(data.f.timings)

                # Close data file and run the garbage collector.
                data.close()
            results.append(number_results)
    except Exception as e:
        print(e)
        print("ERROR: inputs for plotter are missing")
        breakpoint()

    ###
    # Plot result.
    ###
    draw_boxplots(
            results, "output/timing/results_number.pdf",
            xlabels=numbers_tasks,
            xaxis_label="number of tasks",
            yaxis_label="time for execution [s]")


def draw_boxplots(
        results,
        filename,
        xlabels=["", "", ""],
        xaxis_label="",
        yaxis_label="",
        ylimits=None  # [ylim_min, ylim_max]
        ):
    """Boxplot: Draw given results.
    """

    # Plotting.
    # Blue box configuration:
    boxprops = dict(linewidth=4, color='blue')
    # Median line configuration:
    medianprops = dict(linewidth=4, color='red')
    whiskerprops = dict(linewidth=4, color='black')
    capprops = dict(linewidth=4)
    # Size parameters:
    plt.rcParams.update({'font.size': 18})
    plt.rcParams.update({'figure.subplot.top': 0.99})
    plt.rcParams.update({'figure.subplot.bottom': 0.25})
    plt.rcParams.update({'figure.subplot.left': 0.18})
    plt.rcParams.update({'figure.subplot.right': 0.99})
    plt.rcParams.update({'figure.figsize': [7, 4.8]})

    # Draw plots:
    fig1, ax1 = plt.subplots()
    if ylimits is not None:
        ax1.set_ylim(ylimits)
    ax1.set_ylabel(yaxis_label, fontsize=25)

    my_plot = ax1.boxplot(
            results,
            labels=xlabels,
            showfliers=False,
            boxprops=boxprops,
            medianprops=medianprops,
            whiskerprops=whiskerprops,
            capprops=capprops,
            widths=0.6)
    # ax1.set_yticks([0, 20, 40, 60, 80, 100])
    # ax1.set_yticklabels(("0", "20", "40", "60", "80", "100"))
    # ax1.tick_params(axis='x', rotation=0, labelsize=35)
    # ax1.tick_params(axis='y', rotation=0, labelsize=35)
    ax1.set_xlabel(xaxis_label, fontsize=25)
    plt.tight_layout()

    # Save.
    plt.savefig(filename)


if __name__ == '__main__':
    main()
