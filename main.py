#!/usr/local/python
"""The tikz schedule drawer generates a schedule by given inputs and provides a latex file as output.

:Filename: main.py
:Author: Marco Dürr (marco.duerr@tu-dortmund.de)
:Date: 15.06.18
"""

import gc
import stt.task as t
import stt.scheduler as s
import stt.analyser as a
import stt.generator as g
import stt.chain as c
import stt.transformer as trans
from stt.niklas import generate_cause_effect_chains_waters15
from stt.niklas import generate_distributed_chain
from stt.niklas import generate_cause_effect_chains_from_transformed_task_sets
import stt.communication as communication
import csv
import argparse
import stt.evaluation as eva
import stt.generator_marco as gm
import stt.eventSimulator as es
import math
import numpy as np



def main():
    # Argumenten Uebergabe
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", type=int, default=0) # which part of code should be executed
    parser.add_argument("-u", type=float, default=50) # utilization in 0 to 100 [percent] !!!!
    parser.add_argument("-g", type=int, default=0) # task generation. 0: WATERS Benchmark, 1: UUnifast
    # only for l==1:
    parser.add_argument("-n", type=str, default="run0") # name of the run
    parser.add_argument("-r", type=int, default=1) # number of task sets to generate
    parser.add_argument("-s", type=int, default=0) # sample scenario. 0: Scenario A, 1: Scenario B
    args = parser.parse_args()
    del parser
    # Global Variables
    task_sets = []
    task_sets_communication = []
    schedules = []
    cause_effect_chain_sets = {"all": [], "ordered": [], "unordered": []}
    cause_effect_chains_interconnected = {"all": [], "ordered": [], "unordered": []}

    ###
    # l=="1": Single ECU Analysis; args: -l1 -u_ -g_ -n_ -r_ -s_
    # Create task sets, cause-effect chains, do TDA, do Davare, do 2019-Marco, do our analysis, do Kloda, save Data
    ###
    # Required arguments : l = "1", u = 50 utilization, r = 10 number of runs, n = "run0" name of the run.
    if args.l == 1:
        print("generate task sets")
        if args.g ==0:
            ###
            # WATERS
            ###
            profile = [0.03 / 0.85, 0.02 / 0.85, 0.02 / 0.85, 0.25 / 0.85, 0.25 / 0.85, 0.03 / 0.85, 0.2 / 0.85,
                       0.01 / 0.85, 0.04 / 0.85] # describes some statistical distribution for task set generation; from table 3 of waters free benchmark paper
            scaling_flag = True
            runs = 1
            threshold = 0.1 # cummulative utilization threshold 0.1 percent, i.e., maximal difference between actual utilization and required utilization
            min_uti = args.u/100.0 # utilization -- why min?
            angel_synchronous_tasks = False
            number_of_cylinders = 4
            angle_mode = 'sporadic'
            task_sets_generator = []
            while len(task_sets_generator) < args.r:
                # Create several task sets from generator
                task_sets_gen = g.generate_taskset_util_number(runs, min_uti, profile, scaling_flag,
                                                               threshold / 100.0, angel_synchronous_tasks,
                                                               number_of_cylinders,
                                                               angle_mode)
                task_sets_generator.append(task_sets_gen[0])
            # Transform tasks and cause-effect chains into framework structure
            trans1 = trans.Transformer("transformer1", task_sets_generator, 10000000)
            # Transform tasks into framework model, create CAN message task
            task_sets = trans1.transform_tasks(False) # we created all tasks to have bcet=0, we do not use this value in any analysis # False=synchronous, True=asynchronous
            cause_effect_chain_sets = generate_cause_effect_chains_waters15(task_sets, False)

        if args.g ==1:
            ###
            # UUnifast by KHCHEN
            ###
                # task_sets_generator = gm.generate_tasksets(5, args.r, 1, 100, args.u, rounded=True)
                task_sets_generator = gm.generate_tasksets_predefined(50, args.r, 1, 2000, args.u/100.0, [1,2,5,10,20,50,100,200,500,1000])
                # Transform tasks and cause-effect chains into framework structure
                trans2 = trans.Transformer("transformer2", task_sets_generator, 10000000)
                # Transform tasks into framework model
                task_sets = trans2.transform_tasks(False) # we created all tasks to have bcet=0, we do not use this value in any analysis
                # Create cause-effect chains w.r.t the task sets
                # breakpoint()
                print("create cause-effect chains")
                cause_effect_chain_sets = generate_cause_effect_chains_from_transformed_task_sets(task_sets)

        """
        First Analyses (TDA, Sporadic End-to-End)
        """
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
            for chain in cause_effect_chain_sets[i]:
                # OUR RESULTS
                # print("\t\tCASES20: max age")
                # res0 = analyzer.max_age_CASES(schedule, chain, max_phase, hyper_period, args.s, extended=True) # CASES20 - our analysis
                # res0b = analyzer.max_age_CASES(schedule, chain, max_phase, hyper_period, args.s, extended=False) # CASES20 - our analysis
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
        np.savez("output/1single/task_set_u=" + str(args.u) + "_n="+ args.n + "_g=" + str(args.g) + ".npz", task_sets=task_sets, chains=cause_effect_chain_sets)

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
            com_tasks = communication.generate_communication_taskset(20, 10, 1000, True) # generate communication tasks
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
        analyzer = a.Analyser("0")
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
