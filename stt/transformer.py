"""The transformer is used to import scheduling data of other frameworks.

:Filename: transformer.py
:Author: Marco Dürr (marco.duerr@tu-dortmund.de)
:Date: 03.02.19
"""
import stt.task as t
import stt.chain as cec
from scipy import stats


class Transformer:
    """Class Transformer

            **Global Variables**
                :cvar id: Unique identifier.
                :type id: String
            **Usage**
                >>> import stt.transformer as transformer
                >>> myTask = transformer.Transformer("trans1", [0], [1])
        """

    id = ""
    task_sets = []
    chain_sets = []
    time_scale = 1

    def __init__(self, t_id, t_task_sets, time_scale):
        """Creates a transformer represented by an unique ID, Task Set and Cause-Effect Set.

        :param t_id: Unique identifier
        :type t_id: String
        :param t_task_sets: task sets
        :type t_task_sets: List
        :param t_chain_sets: cause-effect chain sets
        :type t_chain_sets: List
        """
        self.id = str(t_id)
        self.task_sets = t_task_sets
        self.time_scale = time_scale

    def transform_tasks(self, phase):
        # Distribution of task phases
        distribution_phase = stats.uniform()
        # Initialization of the transformed task sets
        transformed_task_sets = []

        for task_set in self.task_sets:
            sorted_task_set = sorted(task_set, key=lambda task: task['period']) # sort by period
            transformed_task_set = []
            i = 0
            for task in sorted_task_set:
                if phase:
                    phase = int(float(format(distribution_phase.rvs() * 1000, ".7f")) * self.time_scale)
                else:
                    phase = 0
                transformed_task_set.append(
                    t.Task(i, phase, 0,
                           int(float(format(task['execution'], ".7f")) * self.time_scale),
                           int(float(format(task['period'], ".7f")) * self.time_scale),
                           int(float(format(task['period'], ".7f")) * self.time_scale), i))
                i += 1
            transformed_task_sets.append(transformed_task_set)
        return transformed_task_sets

    # def transform_ce_chains_random(self):
    #     # Initialization of the cause-effect chain sets
    #     chain_sets = []
    #     # loop for all chain sets
    #     for j in range(len(self.chain_set_random)):
    #         # Initialization of the transformed chain_set for one task_set
    #         chain_set = []
    #         # loop for all chains in a single task set
    #         for k in range(len(self.chain_set_random[j])):
    #             chain = []
    #             # loop for tasks in a cause-effect chain
    #             for l in range(len(self.chain_set_random[j][k])):
    #                 for task in self.task_set[j]:
    #                     if task.id == str(self.chain_set_random[j][k][l]['id']):
    #                         chain.append(task)
    #             if len(chain) > 1:
    #                 chain_set.append(cec.CauseEffectChain(str(j), chain))
    #         chain_sets.append(chain_set)
    #     return chain_sets

    # def transform_ce_chains_order(self):
    #     # Initialization of the cause-effect chain sets
    #     chain_sets = []
    #     # loop for all chain sets
    #     for j in range(len(self.chain_set_order)):
    #         # Initialization of the transformed chain_set for one task_set
    #         chain_set = []
    #         # loop for all chains in a single task set
    #         for k in range(len(self.chain_set_order[j])):
    #             chain = []
    #             # loop for tasks in a cause-effect chain
    #             for l in range(len(self.chain_set_order[j][k])):
    #                 for task in self.task_set[j]:
    #                     if task.id == str(self.chain_set_order[j][k][l]['id']):
    #                         chain.append(task)
    #             if len(chain) > 1:
    #                 chain_set.append(cec.CauseEffectChain(str(j), chain))
    #         chain_sets.append(chain_set)
    #     return chain_sets
