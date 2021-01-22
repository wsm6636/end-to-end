"""Task set and cause-effect chain generation with WATERS benchmark.

From the paper: 'Real world automotive benchmark for free' (WATERS 2015).
"""
from scipy import stats
import numpy as np
import random
from scipy.stats import exponweib
import stt.chain as c


###
# Task set generation.
###

class task (dict):
    """A task according to our task model.
    Used only for the purpose of task creation.
    """
    def __init__(self, execution, period, deadline):
        """Initialize a task."""
        dict.__setitem__(self, "execution", float(execution))
        dict.__setitem__(self, "period", float(period))
        dict.__setitem__(self, "deadline", float(deadline))
        dict.__setitem__(self, "id", 0)  # task id  # TODO: remove ?


def sample_runnable_acet(period, amount=1, scalingFlag=False):
    """Create runnables according to the WATERS benchmark.
    scalingFlag: make WCET out of ACET with scaling
    """
    # Parameters from WATERS 'Real World Automotive Benchmarks For Free'
    if period == 1:
        scaling = np.random.uniform(1.3, 29.11, amount)  # between fmin fmax
        dist = exponweib(1, 1.044, loc=0, scale=1.0/0.214)  # TODO where does that come from?
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.34 or samples[i] > 30.11:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
               continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 2:
        scaling = np.random.uniform(1.54, 19.04, amount)
        dist = exponweib(1, 1.0607440083, loc=0, scale=1.0/0.2479463059)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.32 or samples[i] > 40.69:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
               continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 5:
        scaling = np.random.uniform(1.13, 18.44, amount)
        dist = exponweib(1, 1.00818633, loc=0, scale=1.0/0.09)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.36 or samples[i] > 83.38:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
               continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 10:
        scaling = np.random.uniform(1.06, 30.03, amount)
        dist = exponweib(1, 1.0098, loc=0, scale=1.0/0.0985)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.21 or samples[i] > 309.87:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
               continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 20:
        scaling = np.random.uniform(1.06, 15.61, amount)
        dist = exponweib(1, 1.01309699673984310, loc=0, scale=1.0/0.1138186679)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.25 or samples[i] > 291.42:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
               continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 50:
        scaling = np.random.uniform(1.13, 7.76, amount)
        dist = exponweib(1, 1.00324219159296302, loc=0, scale=1.0/0.05685450460)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.29 or samples[i] > 92.98:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
               continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 100:
        scaling = np.random.uniform(1.02, 8.88, amount)
        dist = exponweib(1, 1.00900736028318527, loc=0, scale=1.0/0.09448019812)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.21 or samples[i] > 420.43:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
               continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 200:
        scaling = np.random.uniform(1.03, 4.9, amount)
        dist = exponweib(1, 1.15710612360723798, loc=0, scale=1.0/0.3706045664)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.22 or samples[i] > 21.95:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
               continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 1000:
        scaling = np.random.uniform(1.84, 4.75, amount)
        if scalingFlag:
            return list(0.001 * np.random.uniform(0.37, 0.46, amount) *scaling)
        else:
            return list(0.001 * np.random.uniform(0.37, 0.46, amount))


def gen_tasksets(number_of_sets = 100, util_max = 1.0, period_pdf = [0.03, 0.02, 0.02, 0.25, 0.40, 0.03, 0.2, 0.01, 0.04], scalingFlag = False, threshold = 0.1, cylinder = 4, mode = 'sporadic'):
    while True:
        taskset = []
        dist = stats.rv_discrete(name='periods', values = ([1,2,5,10,20,50,100,200,1000], period_pdf))
        runnables = (30000*number_of_sets)



        sys_runnable_periods = dist.rvs(size=runnables)

        sys_runnables_period_0001_amount = 0
        sys_runnables_period_0002_amount = 0
        sys_runnables_period_0005_amount = 0
        sys_runnables_period_0010_amount = 0
        sys_runnables_period_0020_amount = 0
        sys_runnables_period_0050_amount = 0
        sys_runnables_period_0100_amount = 0
        sys_runnables_period_0200_amount = 0
        sys_runnables_period_1000_amount = 0

        for period in sys_runnable_periods:
            if period == 1:
                sys_runnables_period_0001_amount += 1
            elif period == 2:
                sys_runnables_period_0002_amount += 1
            elif period == 5:
                sys_runnables_period_0005_amount += 1
            elif period == 10:
                sys_runnables_period_0010_amount += 1
            elif period == 20:
                sys_runnables_period_0020_amount += 1
            elif period == 50:
                sys_runnables_period_0050_amount += 1
            elif period == 100:
                sys_runnables_period_0100_amount += 1
            elif period == 200:
                sys_runnables_period_0200_amount += 1
            elif period == 1000:
                sys_runnables_period_1000_amount += 1
            else:
                print("ERROR")

            # build tasks from runnables (PERIOD = 1)
        wcets = sample_runnable_acet(1, sys_runnables_period_0001_amount, scalingFlag)
        for i in range(sys_runnables_period_0001_amount):
            # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(wcets[i], 1, 1))

            # build tasks from runnables (PERIOD = 2)
        wcets = sample_runnable_acet(2, sys_runnables_period_0002_amount, scalingFlag)
        for i in range(sys_runnables_period_0002_amount):
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(wcets[i], 2, 2))

            # build tasks from runnables (PERIOD = 5)
        wcets = sample_runnable_acet(5, sys_runnables_period_0005_amount, scalingFlag)
        for i in range(sys_runnables_period_0005_amount):
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(wcets[i], 5, 5))#

            # build tasks from runnables (PERIOD = 10)
        wcets = sample_runnable_acet(10, sys_runnables_period_0010_amount, scalingFlag)
        for i in range(sys_runnables_period_0010_amount):
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(wcets[i], 10, 10))

            # build tasks from runnables (PERIOD = 20)
        wcets = sample_runnable_acet(20, sys_runnables_period_0020_amount, scalingFlag)
        for i in range(sys_runnables_period_0020_amount):
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(wcets[i], 20, 20))

            # build tasks from runnables (PERIOD = 50)
        wcets = sample_runnable_acet(50, sys_runnables_period_0050_amount, scalingFlag)
        for i in range(sys_runnables_period_0050_amount):
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(wcets[i], 50, 50))

            # build tasks from runnables (PERIOD = 100)
        wcets = sample_runnable_acet(100, sys_runnables_period_0100_amount, scalingFlag)
        for i in range(sys_runnables_period_0100_amount):
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(wcets[i], 100, 100))

            # build tasks from runnables (PERIOD = 200)
        wcets = sample_runnable_acet(200, sys_runnables_period_0200_amount, scalingFlag)
        for i in range(sys_runnables_period_0200_amount):
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(wcets[i], 200, 200))

            # build tasks from runnables (PERIOD = 1000)
        wcets = sample_runnable_acet(1000, sys_runnables_period_1000_amount, scalingFlag)
        for i in range(sys_runnables_period_1000_amount):
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(wcets[i], 1000, 1000))

        random.shuffle(taskset)
        sets = []

        for j in range(number_of_sets):
            thisset = taskset[:3000]
            taskset = taskset[3000:]
            util = 0.0
            i = 0
            for tasks in thisset:
                if tasks['period'] == 0.5:
                    util += tasks['execution']/tasks['deadline']
                else:
                    util += tasks['execution']/tasks['period']
                i = i + 1
                if util > util_max:
                    break

            if(util <= util_max + threshold):
                thisset = thisset[:i]
            else:
                i = i - 1
                initialSet = thisset[:i]
                remainingTasks = thisset[i:]
                tasks = remainingTasks[0]
                if (tasks['period'] == 0.5):
                    util -= tasks['execution']/tasks['deadline']
                else:
                    util -= tasks['execution']/tasks['period']
                while (util < util_max):
                    tasks = remainingTasks[0]
                    if (tasks['period'] == 0.5):
                        if (util + tasks['execution']/tasks['deadline'] <= util_max + threshold):
                            util += tasks['execution']/tasks['deadline']
                            initialSet.append(tasks)
                        remainingTasks = remainingTasks[1:]

                    else:
                        if (util + tasks['execution']/tasks['period'] <= util_max + threshold):
                            util += tasks['execution']/tasks['period']
                            initialSet.append(tasks)
                        remainingTasks = remainingTasks[1:]

                thisset = initialSet
            sets.append(thisset)
        # Remove task sets that contain just one task
        for task_set in sets:
            if len(task_set) < 2:
                sets.remove(task_set)
        return sets

""" cause effect chains
"""


def gen_ce_chains(transformed_task_sets, sort): # WATERS
    distribution_involved_activation_patterns = stats.rv_discrete(values=([1, 2, 3], [0.7, 0.2, 0.1]))
    distribution_number_of_tasks = stats.rv_discrete(values=([2, 3, 4, 5], [0.3, 0.4, 0.2, 0.1]))
    ce_chains = []

    for task_set in transformed_task_sets:
        cause_effect_chain_set = []
        for number_of_cause_effect_chains in range(int(np.random.randint(30, 60))): # 30 to 60 cause-effect chains
            chain = []
            involved_activation_patterns = list(np.random.choice(list(set(map(lambda task: task.period, task_set))),
                                                                 size=int(
                                                                     distribution_involved_activation_patterns.rvs()),
                                                                 replace=False))
            if sort:
                involved_activation_patterns.sort()
            else:
                np.random.shuffle(involved_activation_patterns)

            for period in involved_activation_patterns:
                tasks_with_period = [task for task in task_set if task.period == period]
                try:
                    chain.append(
                        np.random.choice(tasks_with_period, size=distribution_number_of_tasks.rvs(), replace=False))
                except ValueError:
                    chain = []
                    break
            cec_chain = []
            for chain_part in chain:
                for task in chain_part:
                    cec_chain.append(task)
            if chain:
                cause_effect_chain_set.append(c.CauseEffectChain(number_of_cause_effect_chains, cec_chain))
        ce_chains.append(cause_effect_chain_set)
    return ce_chains
