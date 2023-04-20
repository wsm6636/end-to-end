"""Creation of TSN tasks."""

import numpy as np
import random
import math
import utilities.TSNtask as qchtask

# Qch description.
QCH = {
    # 'QUEUE_SIZE': 130, #队列最大数据包容量
    # 'BANDWIDTH_MBPS': 1, #带宽
    # 'MTU' : 1, #最大数据包长度
    # 'HOP_DELAy': 1, #交换机内处理+传播延迟
    # 'SYNC' : 1, #时钟同步精度
    'SLOT' : 125
}


# Main function

def generate_tsn_taskset(num_tasks, min_period, max_period,
                                   rounded=False, max_trials=100):
    """Generate a set of tsn tasks.

    num_tasks: number of tsn tasks in the set
    min_period: lower bound for the periods
    max_period: upper bound for the periods
    rounded: flag for rounding the period values
    max_trials: maximal tries to create a proper task set
    """
    # If no proper taskset was created, we try again.
    trials = 0
    while (trials < max_trials):
        # Create candidates.
        taskset = generate_tsn_candidate_taskset(
                num_tasks, min_period, max_period, rounded)
        taskset = sorted(taskset, key=lambda x: x.priority)

        # Compute WCRT.
        if qch_response_time(taskset):
            return taskset
        trials += 1
    # The creation failed too many times.
    return False


# Help functions
def generate_tsn_candidate_taskset(num_tasks, min_period, max_period,
                                             rounded=False):
    """Generate candidate for the set of tsn tasks.20,10,1000"""
    taskset = []
    # Generate WCET and periods.
    slot = (float(QCH['SLOT']))/10**3
    periods = np.exp(np.random.uniform(
            low=np.log(min_period), high=np.log(max_period), size=num_tasks))
    if rounded:  # round to nearest integer.
        periods = np.rint(periods).tolist()
    # Generate priorities.
    prio = list(range(num_tasks))
    random.shuffle(prio)
    # Create tasks.
    for i in range(num_tasks):
        # hops = random.randint(1, 6)
        hops = 1
        offset = hops * slot
        taskset.append(qchtask.TSNTask(i, offset, hops, slot, periods[i], periods[i], prio[i]))
    return taskset


def qch_response_time(taskset):
    """Compute the worst-case response time of the tsn tasks."""  
    def ddl(pivot):
        time = (pivot.offset + pivot.hops) * pivot.slot
        if (pivot.deadline <= time):  # stop property
            return False

    for task in taskset:
        rt = task.offset + (task.hops + 1) * task.slot
        ddl = ddl(task)
        if rt >= task.deadline:  # WCRT > deadline is not allowed
            return False
        elif ddl is False:
            return False
        else:
            # Set task WCRT
            task.rt = rt

    return True
