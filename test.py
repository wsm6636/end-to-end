# from scipy import stats
# import numpy as np
# xk = np.arange(7)
# pk = (0.1, 0.2, 0.3, 0.1, 0.1, 0.0, 0.2)
# custm = stats.rv_discrete(name='custm', values=(xk, pk))

# import matplotlib.pyplot as plt
# fig, ax = plt.subplots(1, 1)
# ax.plot(xk, custm.pmf(xk), 'ro', ms=12, mec='r')
# ax.vlines(xk, 0, custm.pmf(xk), colors='r', lw=4)
# plt.show()
# plt.savefig('temp.png')
# CAN-bus description.
"""Creation of TSN tasks."""

import gc  # garbage collector
import argparse
import math
import numpy as np
import utilities.chain as c
import utilities.communication as comm
import utilities.Qch as qch
import utilities.generator_WATERS as waters
import utilities.generator_UUNIFAST as uunifast
import utilities.transformer as trans
import utilities.event_simulator as es
import utilities.analyzer as a
import utilities.evaluation as eva
import random
import utilities.TSNtask as qchtask
import utilities.task
import utilities.augmented_job_chain as aug
debug_flag = False  
# Qch description.
QCH = {
    'QUEUE_SIZE': 130, #队列最大数据包容量
    'BANDWIDTH_MBPS': 1, #带宽
    'MTU' : 1, #最大数据包长度
    'HOP_DELAy': 1, #交换机内处理+传播延迟
    'SYNC' : 1, #时钟同步精度
    'SLOT' : 125
}
def reaction_inter_tsn(self, chain_set):
    """tsn maximum reaction time analysis for interconnected cause-effect
    chains.

    Input: chain_set is a list of cause-effect chains with entry at
    interconnected.
    Note: The chains have to be analyzed by Gunzel single ECU maximum reaction
    time analysis beforehand. ( reaction_Gunzel() )
    """
    for chain in chain_set:
        inter_tsn_react = 0  # total reaction time
        for i in range(0, len(chain.tsntask)):
            # Case: i is a communication task.
            if isinstance(chain.tsntask[i], utilities.TSNtask.TSNTask):
                inter_tsn_react += (chain.tsntask[i].period
                                    + chain.tsntask[i].rt)
            # Case: i is a cause-effect chain.
            else:
                inter_tsn_react += chain.tsntask[i].Gunzel_react
        # Store result.
        chain.inter_tsn_react = inter_tsn_react
def main():
    # Help functions
    # print("main")
    utilization = args.u
    gen_setting = args.g
    num_runs = args.n
    number_interconn_ce_chains = 10000

    try:
        ###
        # Load data.
        # 多个ECU互联需要前面单个ECU上的分析结果？
        ###
        print("=Load data.=")
        chains_single_ECU = []
        for i in range(num_runs):
            name_of_the_run = str(i)
            data = np.load(
                    "output/1single/task_set_u=" + str(utilization)
                    + "_n=" + name_of_the_run
                    + "_g=" + str(gen_setting)
                    + ".npz", allow_pickle=True)
            for chain_set in data.f.chains:
                for chain in chain_set:
                    chains_single_ECU.append(chain)

            # Close data file and run the garbage collector.
            data.close()
            del data
            gc.collect()
    except Exception as e:
        print(e)
        print("ERROR: inputs from single are missing")
        if debug_flag:
            breakpoint()
        else:
            return
    print("=Interconnected cause-effect chain generation.=")
    chains_inter = []#存储所有生成的因果链
    chains_inter_tsn = [] #TSN
    for j in range(0, number_interconn_ce_chains):
        chain_all = []  # sequence of all tasks (from chains + comm tasks)
        i_chain_all = []  # sequence of chains and comm_tasks
        chain_all_tsn = []  # #TSN
        i_chain_all_tsn = [] #TSN

        # Generate communication tasks.生成通信任务，需要改成tsn
        com_tasks = comm.generate_communication_taskset(5, 10, 100, True)
        tsn_tasks = qch.generate_tsn_taskset(5, 10, 100, True) #TSN
    
        # Fill chain_all and i_chain_all.
        k = 0
        for chain in list(np.random.choice(
                chains_single_ECU, 5, replace=False)):  # randomly choose 5，选择五个单ECU的因果链
            i_chain_all.append(chain)
            i_chain_all_tsn.append(chain)#TSN
            for task in chain.chain:
                chain_all.append(task)
                chain_all_tsn.append(task)#TSN
            if k < 4:  # communication tasks are only added in between，插入通信任务，当k小于4时，就在相应位置上添加通信任务。
                chain_all.append(com_tasks[k])
                i_chain_all.append(com_tasks[k])
                chain_all_tsn.append(tsn_tasks[k])#TSN
                i_chain_all_tsn.append(tsn_tasks[k])#TSN
            k += 1

        chains_inter.append(c.CauseEffectChain(0, chain_all, i_chain_all,False))#将生成的新因果链条添加
        chains_inter_tsn.append(c.CauseEffectChain(0, chain_all_tsn, i_chain_all_tsn,True))#TSN
 

if __name__ == '__main__':
    main()