# End-To-End Timing Analysis

The repository is used to reproduce the evaluation from 

*Timing Analysis of Asynchronized Distributed Cause-Effect Chains*

from RTAS 2021.

This document is organized as follows:
1. [Environment Setup](#environment-setup)
2. [How to run the experiments](#how-to-run-the-experiments)
3. [Overview of the corresponding functions]()
4. [Miscellaneous](#miscellaneous)

## Environment Setup
### Requirements

To run the experiments Python 3.7 is required. Moreover, the following packages are required:
```
gc
argparse
math
numpy
scipy
random
matplotlib.pyplot
operator
```

### File Structure

    .
    ├── output                       # Placeholder for outputs
    │   ├── 1single                  # Single ECU chains + results
    │   ├── 2interconn               # Interconnected ECU chains + result
    │   └── 3plots                   # Plots as in the paper
    ├── utilities                    # Placeholder for additional files
    │   ├── analyzer.py              # Methods to analyze end-to-end timing behavior
    │   ├── augmented_job_chain.py   # Augmented job chains as in the paper
    │   ├── chain.py                 # Cause-effect chains
    │   ├── communication.py         # Communication tasks
    │   ├── evaluation.py            # Methods to draw plots
    │   ├── event_simulator.py       # Event-driven simulator with fixed execution time
    │   ├── generator_UUNIFAST       # Task set generator for uunifast benchmark
    │   ├── generator_WATERS         # Task set and cause-effect chain generator for waters benchmark
    │   ├── task.py                  # Tasks
    │   └── transformer.py           # Connect task creating with the scheduler
    ├── auto.sh                      # Running all experiments automatically
    ├── main.py                      # Main function
    ├── timing.py                    # Measure timing behavior
    └── README.md

The experiments in the main function are splitted into 3 parts:
1. Single-ECU analysis
2. Interconnected ECU analysis
3. Plotting the results

In each step, the machines loads the results from the previous step, randomly creates necessary resources like task sets and cause-effect chains, and saves the results in the corresponsing folder in output.  

## How to run the experiments

- To ease the experiment deployment and parallelize the simulation on our server, we decide to use ```screen``` to manage persistent terminal sessions.
- The script ```auto.sh``` is prepared for running all the experiments. It indicates the progress of the experiments by a displaying short descriptions and timestamps.
- If the experiments have to be aborted at some time (e.g., because a certain package is missing), then the instructions inside the auto.sh file can be used to start step 2 and 3 of the evaluation manually.
- Eventually the plots from Figure 6 and 7 of the paper can be foung in the folder output/3plots:
(Need a table here to show the mapping of file and figure)

As a reference, we utilize a machine running Debian 4.19.98-1 (2020-01-26) x86_64 GNU/Linux, with 2 x AMD EPYC 7742 64-Core Processor (64 Cores, 128 Threads), i.e., in total 256 Threads with 2,25GHz and 256GB RAM. Running auto.sh to obtain the same plots from the paper takes about X AMOUNT OF TIME with this machine.

## Overview of the corresponding functions

(Need a table here to show the mapping of function and equation?)

## Miscellaneous

### Authors

* Mario Günzel
* Marco Dürr
* Niklas Ueter
* Kuan-Hsun Chen
* Georg von der Brüggen
* Jian-Jia Chen

### Acknowledgments

???

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

# RTAS requirements for AE
    1. the system requirements (v)
    2. how to use the packaged artifact (please reference specific figures and tables in the paper that will be reproduced), and (x)
    3. how to setup the artifact on a machine different from the provided packaged artifact (e.g., specific versions of software to install on a clean machine);
