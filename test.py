#!/usr/bin/env python3
"""Evaluation for the paper 'Timing Analysis of Asynchronized Distributed
Cause-Effect Chains' (2021).

It includes (1) local analysis (2) global analysis and (3) plotting of the
results.
"""

import gc  # garbage collector
import argparse
import numpy as np
import draw as d


def main():
    """Main Function."""
    ###
    # Argument Parser
    ###
    parser = argparse.ArgumentParser()
    #一共三部分，第一部分单ECU，第二部分多ECU，第三部分画图
    # which part of code should be executed:
    # utilization in 0 to 100 [percent]:
    # task generation (0: WATERS Benchmark, 1: UUnifast):
    parser.add_argument("-g", type=int, default=0)

    args = parser.parse_args()
    del parser #释放内存
    """Evaluation.

        Required arguments:
        -j3
        -g : task generation setting (for loading)
        """
        # Variables.
    gen_setting = args.g
    print(gen_setting)
    utilizations = [50.0, 60.0, 70.0, 80.0, 90.0]

    try:
        ###
        # Load data.
        ###
        print("=Load data.=")
        chains_single_ECU = []
        chains_inter = []
        chains_inter_tsn = []
        for ut in utilizations:
            data = np.load(
                    "output/2interconn/chains_" + "u=" + str(ut)
                    + "_g=" + str(gen_setting) + ".npz", allow_pickle=True)

            # Single ECU.
            for chain in data.f.chains_single_ECU:
                chains_single_ECU.append(chain)

            # Interconnected.
            for chain in data.f.chains_inter:
                chains_inter.append(chain)

            for chain in data.f.chains_inter_tsn:
                chains_inter_tsn.append(chain)

            # Close data file and run the garbage collector.
            data.close()
            del data
            gc.collect()
    except Exception as e:
        print(e)
        print("ERROR: inputs for plotter are missing")
        if debug_flag:
            breakpoint()
        else:
            return

    ###
    # Draw plots.
    ###
    print("=Draw plots.=")
    myeva = d.Draw()
    # Interconnected ECU Plot.
    myeva.davare_boxplot_age_interconnected(
            chains_inter,chains_inter_tsn,
            "output/3plots/test_davare_interconnected_age"
            + "_g=" + str(gen_setting) + ".pdf",
            xaxis_label="", ylabel="Latency reduction [%]")
    myeva.davare_boxplot_reaction_interconnected(
            chains_inter,chains_inter_tsn,
            "test_davare_interconnected_reaction"
            + "_g=" + str(gen_setting) + ".pdf",
            xaxis_label="", ylabel="Latency reduction [%]")

if __name__ == '__main__':
    main()

