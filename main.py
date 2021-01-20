#!/usr/bin/env python3
"""Main module for the Evaluation.

It includes (1) local analysis (2) global analysis and (3) plotting of the
results.
"""

import gc  # garbage collector
# import stt.task as t
import stt.analyzer as a
import stt.generator_WATERS as waters
import stt.chain as c
import stt.transformer as trans
import stt.communication as comm
import csv
import argparse
import stt.evaluation as eva
import stt.generator_UUNIFAST as uunifast
import stt.eventSimulator as es
import math
import numpy as np


def main():
    """Main Function."""
    ###
    # Argument Parser
    ###
    parser = argparse.ArgumentParser()
    # which part of code should be executed:
    parser.add_argument("-l", type=int, default=0)
    # utilization in 0 to 100 [percent]:
    parser.add_argument("-u", type=float, default=50)
    # task generation (0: WATERS Benchmark, 1: UUnifast):
    parser.add_argument("-g", type=int, default=0)

    # only for l==1:
    # name of the run:
    parser.add_argument("-n", type=str, default="run0")
    # number of task sets to generate:
    parser.add_argument("-r", type=int, default=1)

    args = parser.parse_args()
    del parser

    ###
    # Global Variables
    ###
    task_sets = []
    schedules = []
    ce_chains = {"all": [], "ordered": [], "unordered": []}

    if args.l == 1:
        """ Single ECU analysis.

        Required arguments:
        -l1
        -u : utilization
        -g : task generation setting
        -r : number of runs
        -n : name of the run

        Create task sets and cause-effect chains, use TDA, Davare, Duerr, our
        analysis, Kloda, and save the Data
        """

        ###
        # Task set and cause-effect chain generation.
        ###
        print("=Task set and cause-effect chain generation.=")
        if args.g == 0:
            # WATERS benchmark
            print("WATERS benchmark.")

            # Statistical distribution for task set generation from table 3 of
            # WATERS free benchmark paper.
            profile = [0.03 / 0.85, 0.02 / 0.85, 0.02 / 0.85, 0.25 / 0.85,
                       0.25 / 0.85, 0.03 / 0.85, 0.2 / 0.85, 0.01 / 0.85,
                       0.04 / 0.85]
            # Required utilization:
            req_uti = args.u/100.0
            # Maximal difference between required utilization and actual
            # utilization is set to 0.1 percent:
            threshold = 0.1

            # Create task sets from the generator.
            print("Create task sets.")
            task_sets_waters = []
            while len(task_sets_waters) < args.r:
                task_sets_gen = waters.gen_tasksets(
                        1, req_uti, profile, True, threshold / 100.0, 4,
                        'sporadic')
                task_sets_waters.append(task_sets_gen[0])

            # Transform tasks into framework structure.
            trans1 = trans.Transformer("1", task_sets_waters, 10000000)
            task_sets = trans1.transform_tasks(False)

            # Create cause effect chains.
            print("Create cause-effect chains")
            ce_chains = waters.gen_ce_chains(task_sets, False)

        if args.g == 1:
            # UUnifast benchmark.
            print("UUnifast benchmark.")

            # Create task sets from the generator.
            print("Create task sets.")

            # # Generate log-uniformly distributed task sets:
            # task_sets_generator = uunifast.gen_tasksets(
            #         5, args.r, 1, 100, args.u, rounded=True)

            # Generate log-uniformly distributed task sets with predefined
            # periods:
            periods = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
            min_pull = 1
            max_pull = 2000
            task_sets_uunifast = uunifast.gen_tasksets_pred(
                    50, args.r, min_pull, max_pull, args.u/100.0, periods)

            # Transform tasks into framework structure.
            trans2 = trans.Transformer("2", task_sets_uunifast, 10000000)
            task_sets = trans2.transform_tasks(False)

            # Create cause-effect chains.
            print("Create cause-effect chains")
            ce_chains = uunifast.gen_ce_chains(task_sets)
            # ce_chains contains one set of cause effect chains for each task
            # set in task_sets.

        ###
        # First analyses (TDA, Davare, Duerr).
        ###
        print("=First analyses (TDA, Davare, Duerr).=")
        analyzer = a.Analyzer("0")

        # TDA for each task set.
        print("\tTDA.")
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
        print("\tTest: Davare.")
        analyzer.davare(ce_chains)

        print("\tTest: Duerr Reaction Time.")
        analyzer.reaction_sporadic(ce_chains)

        print("\tTest: Duerr Data Age.")
        analyzer.age_sporadic(ce_chains)

        ###
        # Second analyses (Simulation, Our, Kloda).
        ###
        print("Second analyses (Simulation, Our, Kloda).")
        i = 0
        for task_set in task_sets:
            print("Task set ", i+1)

            # Event-based simulation.
            print("\tSimulation.")
            simulator = es.eventSimulator(len(task_set), task_set)
            # Determination of the variables used to compute the stop condition of the simulation
            max_e2e_latency = max(ce_chains[i], key=lambda chain: chain.e2e_latency).e2e_latency
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
            for chain in ce_chains[i]:
                # OUR RESULTS
                # print("\t\tCASES20: max age")
                print("\t\tOUR: max age")
                analyzer.max_age_OUR(schedule, task_set, chain, max_phase, hyper_period, shortened=False)
                analyzer.max_age_OUR(schedule, task_set, chain, max_phase, hyper_period, shortened=True)
                print("\t\tOUR: reaction")
                analyzer.reaction_OUR(schedule, task_set, chain, max_phase, hyper_period)

                # Kloda analysis, assuming synchronous releases
                print("\t\tKloda for synchr")
                for release_time_first_task_in_chain in range(0, max(1, hyper_period), chain.chain[0].period):
                    kloda = analyzer.kloda(chain.chain, release_time_first_task_in_chain, beginning=True)
                    if chain.kloda < kloda:
                        chain.kloda = kloda # Kloda
                # Note: additional period of the first task is already in the computation of kloda

                ###
                if chain.kloda < chain.sim_react:
                    breakpoint()
            i += 1
        # Save data (task_sets, chains and schedules)
        print("save data")
        np.savez("output/1single/task_set_u=" + str(args.u) + "_n="+ args.n + "_g=" + str(args.g) + ".npz", task_sets=task_sets, chains=ce_chains)

    ###
    # l=="2": Interconnected analysis; args: -l2 -u_ -g_
    # Load data
    elif args.l==2:
        utilization=args.u
        no_interconn_cechains = 10000
        chains_single_ECU=[]
        chains_interconnected = []
        for i in range(1, 101):
            name_of_the_run = "run" + str(i)
            data = np.load("output/1single/task_set_u=" + str(utilization) + "_n="+ name_of_the_run + "_g=" + str(args.g) + ".npz", allow_pickle=True)
            for chain_set in data.f.chains:
                for chain in chain_set:
                    order = ""
                    prev_id = None
                    chains_single_ECU.append(chain)
            data.close()
            del data
            gc.collect()
        print("Finished loading chains")

        # create interconnected cause-effect chains
        print("create interconnected chains")
        for j in range(0, no_interconn_cechains):
            chain_all = []
            i_chain_all = []
            com_tasks = comm.generate_communication_taskset(20, 10, 1000, True) # generate communication tasks
            k = 0
            for chain in list(np.random.choice(chains_single_ECU, 5, replace=False)):
                i_chain_all.append(chain)
                for task in chain.chain:
                    chain_all.append(task)
                if k < 4:
                    chain_all.append(com_tasks[k])
                    i_chain_all.append(com_tasks[k])
                k += 1
            chains_interconnected.append(c.CauseEffectChain(0, chain_all, i_chain_all)) # Creates a chain ch with ch.chain = (tasks) and ch.interconnected=(chain,task,chain,task,chain)
            if j%100==0:
                print("\t", j)

        # Do Analyses for chains_interconnected; no kloda since we assume that clocks are not synchronized
        print("do analyses")
        analyzer = a.Analyzer("0")
        analyzer.age_interconnected(chains_interconnected) # OUR
        analyzer.reaction_interconnected(chains_interconnected) # OUR
        analyzer.davare([chains_interconnected])
        analyzer.reaction_sporadic([chains_interconnected])
        analyzer.age_sporadic([chains_interconnected])
        # breakpoint()
        # Save chains
        print("save chains utilization: " + str(utilization))
        np.savez("./output/2interconn/chains_" + "u=" + str(utilization) + "_g=" + str(args.g) + ".npz", chains_interconnected=chains_interconnected, chains_single_ECU=chains_single_ECU)
        return


    ###
    # l=="3": draw plots; args: -l3 -g_
    ###
    elif args.l == 3:
        """
            Evaluation
        """
        # Load data
        chains_single_ECU = []
        chains_interconnected = []
        for i in [50.0, 60.0, 70.0, 80.0, 90.0]:
            data = np.load("output/2interconn/chains_" + "u=" + str(i) + "_g=" + str(args.g) + ".npz", allow_pickle=True)
            # Single ECU
            for chain in data.f.chains_single_ECU:
                chains_single_ECU.append(chain)
                #if chain.jj_age < chain.sim_age or chain.kloda < chain.sim_age:
                    #breakpoint()
            # Interconnected
            for chain in data.f.chains_interconnected:
                chains_interconnected.append(chain)
            # Close the data file and run the garbage collector
            data.close()
            del data
            gc.collect()

        # Plotting
        myeva = eva.Evaluation()

        # Single ECU Plot
        myeva.davare_boxplot_age(chains_single_ECU, "output/3plots/davare_single_ecu_age" + "_g=" + str(args.g) + ".pdf", xaxis_label="", ylabel="Latency reduction [%]")
        myeva.davare_boxplot_reaction(chains_single_ECU, "output/3plots/davare_single_ecu_reaction" + "_g=" + str(args.g) + ".pdf", xaxis_label="", ylabel="Latency reduction [%]")

        # Interconnected ECU Plot
        myeva.davare_boxplot_age_interconnected(chains_interconnected, "output/3plots/davare_interconnected_age" + "_g=" + str(args.g) + ".pdf", xaxis_label="", ylabel="Latency reduction [%]")
        myeva.davare_boxplot_reaction_interconnected(chains_interconnected, "output/3plots/davare_interconnected_reaction" + "_g=" + str(args.g) + ".pdf", xaxis_label="", ylabel="Latency reduction [%]")

        # # Heatmap
        # myeva.heatmap_improvement_disorder_age(chains_single_ECU, "output/3plots/heatmap" + "_sim_age"+ "_g=" + str(args.g) + ".pdf", yaxis_label="")
        # myeva.heatmap_improvement_disorder_react(chains_single_ECU, "output/3plots/heatmap" + "_sim_react"+ "_g=" + str(args.g) + ".pdf", yaxis_label="")

        return

    else:
        pass


if __name__ == '__main__':
    main()
