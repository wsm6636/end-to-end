# End-To-End Timing Analysis

The repository is used to reproduce the evaluation from 

*Timing Analysis of Asynchronized Distributed Cause-Effect Chains*

from RTAS 2021.

This document is organized as follows:
1. [Environment Setup](#environment-setup)
2. [How to run the experiments](#how-to-run-the-experiments)
3. [Overview of the corresponding functions](#overview-of-the-corresponding-functions)
4. [Miscellaneous](#miscellaneous)

## Environment Setup
### Requirements

To run the experiments Python 3.7 is required (Python 3.9 might also work). Moreover, the following packages are required:
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

Assuming that Python 3.7 is installed in the targeted machine, to install the required packages:
```
pip3 install scipy numpy matplotlib argparse
```
or
```
python3.7 -m pip install scipy numpy matplotlib argparse
```
In case there is any dependent package missing, please install them accordingly.

### File Structure

TODO: Check the file structure at the end!

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

### Deployment

The following steps explain how to deploy this framework on the machine:

First, clone the git repository or download the [zip file](https://github.com/tu-dortmund-ls12-rt/end-to-end/archive/master.zip)):
```
git clone https://github.com/tu-dortmund-ls12-rt/end-to-end.git
```
Move into the end-to-end folder, change the permissions of the script to be executable, and execute auto.sh natively:
```
cd end-to-end
chmod 777 auto.sh
./auto.sh 10
```
where 10 is maximal number of concurrent jobs ob the machine, it can be set to a higher or lower number depending on the number of available cores.
Please note that the parallization will intensively use the computational resource.
```
'screen -ls' #shows all current screens
'killall screen' #aborts all current screens.
```

## How to run the experiments

- To ease the experiment deployment and parallelize the simulation on our server, we decide to use ```screen``` to manage persistent terminal sessions.
- The script ```auto.sh``` is prepared for running all the experiments. It indicates the progress of the experiments by a displaying short descriptions and timestamps.
- If the experiments have to be aborted at some time (e.g., because a certain package is missing), then the instructions inside the auto.sh file can be used to start step 2 and 3 of the evaluation manually.
- Eventually the plots from Figure 6 and 7 of the paper can be found in the folder output/3plots:

Paper figure | Plot in output/3plots
--- | ---  
Fig. 6 (a) | davare_single_ecu_reaction_g=0.pdf
Fig. 6 (b) | davare_interconnected_reaction_g=0.pdf
Fig. 6 (c) | davare_single_ecu_age_g=0.pdf
Fig. 6 (d) | davare_interconnected_age_g=0.pdf
Fig. 7 (a) | davare_single_ecu_reaction_g=1.pdf
Fig. 7 (b) | davare_interconnected_reaction_g=1.pdf
Fig. 7 (c) | davare_single_ecu_age_g=1.pdf
Fig. 7 (d) | davare_interconnected_age_g=1.pdf

As a reference, we utilize a machine running Debian 4.19.98-1 (2020-01-26) x86_64 GNU/Linux, with 2 x AMD EPYC 7742 64-Core Processor (64 Cores, 128 Threads), i.e., in total 256 Threads with 2,25GHz and 256GB RAM. Running auto.sh to obtain the same plots from the paper takes about X AMOUNT OF TIME with this machine.

TODO: add time

## Overview of the corresponding functions

The following tables describe the mapping between content of our paper and the source code in this repository.

**Section 5.B** (Local analysis):
Paper equation | Source code
--- | ---  
(12) Reaction time | utilities.analyzer.reaction_our()
(13) Data age | utilities.analyzer.max_age_our()

**Section 5.C** (Interconnected analysis):
Paper equation | Source code
--- | ---  
(17) Reaction time | utilities.analyzer.reaction_inter_our()
(18) Data age | utilities.analyzer.max_age_inter_our()

**Section 6** (Reduced data age):
Paper equation | Source code
--- | ---  
(23) Local | utilities.analyzer.max_age_our() with `reduced=True` Flag
(24) Interconnected | utilities.analyzer.max_age_inter_our() with `reduced=True` Flag

**Section 7** (Evaluation):
Benchmark | Source code
--- | ---  
\[18\] Automotive benchmark for task sets | utilities.generator_WATERS.gen_tasksets()
\[18\] Automotive benchmark for cause-effect chains | utilities.generator_WATERS.gen_ce_chains()
\[6\] UUnifast benchmark for task sets | utilities.generator_UUNIFAST.gen_tasksets()

Other analysis | Source code
--- | ---  
\[10\] Dürr: Data age | utilities.analyzer.age_duerr()
\[10\] Dürr: Reaction time | utilities.analyzer.reaction_duerr()
\[17\] Kloda | utilities.analyzer.kloda()
\[9\] Davare | utilities.analyzer.davare()

## Miscellaneous

### Authors

* Mario Günzel
* Marco Dürr
* Niklas Ueter
* Kuan-Hsun Chen
* Georg von der Brüggen
* Jian-Jia Chen

### Acknowledgments

This work has been supported by European Research Council (ERC) Consolidator Award 2019, as part of PropRT (Number 865170), and by Deutsche Forschungsgemeinschaft (DFG), as part of Sus-Aware (Project no. 398602212)

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

# RTAS requirements for AE
1. the system requirements (See [Environment Setup](#environment-setup))
2. how to use the packaged artifact (please reference specific figures and tables in the paper that will be reproduced) (See [How to run the experiments](#how-to-run-the-experiments) and the provided table)
3. how to setup the artifact on a machine different from the provided packaged artifact (e.g., specific versions of software to install on a clean machine) (See [Deployment](#deployment))
