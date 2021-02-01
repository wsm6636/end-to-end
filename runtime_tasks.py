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

import signal

###
# Argument Parser
###
parser = argparse.ArgumentParser()

# number of the run:
parser.add_argument("-n", type=int, default=-1)

# number of tasks:
parser.add_argument("-t", type=int, default=1)

# number of tasks from list:
parser.add_argument("-tindex", type=int, default=-1)

# number of runs:
parser.add_argument("-r", type=int, default=1)

# hyperperiod minimum:
parser.add_argument("-hypermin", type=int, default=-1)

# hyperperiod maximum:
parser.add_argument("-hypermax", type=int, default=-1)

# event simulator timeout [s]:
parser.add_argument("-timeout", type=int, default=0)

# flag to plot results:
parser.add_argument("-j", type=int, default=0)

args = parser.parse_args()
del parser


###
# Main function.
###

def main():
    """Main Function."""

    task_numbers = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 30, 40, 50]

    ###
    # Plotting. (j == 1)
    ###

    # Plot with hyperperiods on xaxis.
    if args.j == 1:
        if args.n == -1:
            print("ERROR: The number of runs is not specified.")
            return
        plot_results(args.n, task_numbers)
        return

    ###
    # Measurements. (j == 1)
    ###

    # Other variables:
    # utilization = 50.0  # in percent
    periods_interval = [1, 20]
    num_runs = args.r
    hypermin = args.hypermin
    hypermax = args.hypermax

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

    event_sim_timeout = args.timeout

    if hypermax != -1 and hypermax < hypermin:
        print("ERROR: hypermax has to be higher than hypermin.")
        return

    results = []

    total_succ_runs = 0
    total_tries = 0
    max_total_tries = 100
    while total_succ_runs < num_runs:

        # When max_total_tries are done, increase succesful tries by 1
        if total_tries >= max_total_tries:
            total_succ_runs += 1
            total_tries = 0
            continue

        total_tries += 1

        # random values
        utilization = random.randint(50, 90)  # random utilization in percent

        ###
        # Task set generation.
        ###
        print("Task set generation.")
        task_sets_dic = uunifast.gen_tasksets(  # dictionary task sets
                num_tasks,
                1,
                periods_interval[0],
                periods_interval[1],
                utilization/100.0,
                rounded=True)

        # Transform tasks to fit framework structure.
        accuracy = 10000000
        trans2 = trans.Transformer("0", task_sets_dic, accuracy)
        task_sets = trans2.transform_tasks(False)

        ###
        # Cause-effect chain generation.
        ###

        chain_len = 5  # number of tasks per chain

        ce_chains = []

        task_set = task_sets[0]

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

        try:
            # Start timer.
            tick = time.time()

            # Set timeout.
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(event_sim_timeout)

            # Task and CE-chain Preperation.

            analyzer = ana.Analyzer("0")

            if TDA_check(task_set, analyzer) is False:
                print("Task set not schedulable.")
                signal.alarm(0)
                continue

            analyzer.davare([[ce_chain]])

            # Simulation preperation

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

            # Compute number of jobs.
            number_of_jobs = 0
            for task in task_set:
                number_of_jobs += sched_interval/task.period

            # Check if hyperperiod is in the given range.
            if hypermin != -1 and hyperperiod/accuracy < hypermin:
                signal.alarm(0)
                continue
            if hypermax != -1 and hyperperiod/accuracy > hypermax:
                signal.alarm(0)
                continue

            # Information for end user.
            print("\tNumber of tasks: ", len(task_set))
            print("\tHyperperiod: ", hyperperiod/accuracy)

            print("\tNumber of jobs to schedule: ",
                  "%.2f" % number_of_jobs)

            # Event-based simulation.
            print("Simulation.")
            simulator = es.eventSimulator(task_set)

            # Stop condition: Number of jobs of lowest priority task.
            simulator.dispatcher(
                    int(math.ceil(sched_interval/task_set[-1].period)))

            # Simulation without early completion.
            schedule = simulator.e2e_result()

            analyzer.reaction_our(schedule, task_set, ce_chain, max_phase,
                                  hyperperiod)

            # Stop timeout alarm.
            signal.alarm(0)

            # Stop timer.
            tock = time.time()

            # Time difference.
            timing = tock-tick
            print(timing, 'seconds')

        except Exception as e:
            if str(e) == "end of time":
                timing = event_sim_timeout
                print("Aborted after " + str(event_sim_timeout) + " seconds.")
            else:
                signal.alarm(0)
                print(e)
                breakpoint()

        if timing > event_sim_timeout:
            timing = event_sim_timeout

        # Compute hyperperiod (may not have been done before due to timeout)
        hyperperiod = analyzer.determine_hyper_period(task_set)/accuracy

        results.append([timing, hyperperiod])

        total_succ_runs += 1
        total_tries = 0

    ###
    # Save data.
    ###

    try:
        np.savez("output/timing/result"
                 + "_#tasks_" + str(num_tasks)
                 + "_run_" + str(args.n)
                 + ".npz",
                 results=results)
    except Exception as e:
        print(e)
        print("ERROR: save")
        breakpoint()

    return


###
# Help functions.
###

def TDA_check(task_set, analyzer):
    for idx in range(len(task_set)):
        task_set[idx].rt = analyzer.tda(task_set[idx], task_set[:idx])
        if task_set[idx].rt > task_set[idx].deadline:
            return False
    return True


def plot_results(
        number,  # number of runs to collect data from
        task_numbers):  # list of task numbers

    hyperperiods = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

    result_values = []
    for _ in hyperperiods:
        result_values.append([])

    for num_tasks in task_numbers:
        try:
            ###
            # Load data.
            ###
            results = []  # lists of timing results
            for idx in range(number):
                data = np.load("output/timing/result"
                               + "_#tasks_" + str(num_tasks)
                               + "_run_" + str(idx)
                               + ".npz",
                               allow_pickle=True)
                if data.f is not None:
                    results += list(data.f.results)

                # Close data file and run the garbage collector.
                data.close()

        except Exception as e:
            print(e)
            print("ERROR: inputs for plotter are missing")
            breakpoint()

        ###
        # Sort by hyperperiod and choose worst case.
        ###

        if len(results) == 0:
            print("ERROR: no results are loaded.")
            return

        # Filter results by hyperperiod.
        filtered_results = []
        for _ in hyperperiods:
            filtered_results.append([0])

        for res in results:
            for idx in range(len(hyperperiods)):
                if hyperperiods[idx] == -1 or res[1] <= hyperperiods[idx]:
                    filtered_results[idx].append(res[0])

        # Choose maximal value among them
        for idx in range(len(filtered_results)):
            result_values[idx].append(max(filtered_results[idx]))

    ###
    # Plot result.
    ###
    draw_points(
            task_numbers,
            result_values,
            hyperperiods,
            "output/timing/results_tasks.pdf",
            xaxis_label="#Tasks per set",
            yaxis_label="Runtime [s]",
            convert=True)


def draw_points(
        results_x,
        results_ys,
        names,
        filename,
        xaxis_label="",
        yaxis_label="",
        ylimits=None,  # [ylim_min, ylim_max]
        convert=False):
    """Boxplot: Draw given results.
    """
    markers = ["+", "x", "v", "^", "<", ">", "o", "+", "x", "v", "^", "<", ">",
               "o"]

    # Plotting.

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

    for idx in range(len(results_ys)):
        plt.plot(
                results_x,
                results_ys[idx],
                marker=markers[idx],
                label=str(names[idx]))

    # Show a legend.
    plt.legend()

    ax1.set_xlabel(xaxis_label, fontsize=25)
    plt.tight_layout()

    # Save.
    plt.savefig(filename)


def handler(signum, frame):
    """Timeout handler."""
    raise Exception("end of time")


if __name__ == '__main__':
    main()
