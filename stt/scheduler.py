"""Representation of a schedule.

:Filename: scheduler.py
:Author: Marco Dürr (marco.duerr@tu-dortmund.de)
:Date: 15.06.18
"""
import math


class Scheduler:
    """Class Scheduler

        **Global Variables**
            :cvar id: Unique identifier.
            :type id: String
            :cvar tasks: Task set that need to be scheduled.
            :type tasks: List
            :cvar preemptive: Describes if released jobs of a task are preemptive or not.
            :type preemptive: Boolean
            :cvar trace_length: Defines for how long the schedule is executed.
            :type trace_length: Integer
            :cvar step_size: Resolution of the represented schedule (1/10 time units).
            :type step_size: Integer

        **Usage**
            >>> import stt.scheduler as scheduler
            >>> import stt.task as task
            >>> t1 = task.Task()
            >>> t2 = task.Task()
            >>> myScheduler = scheduler.Scheduler("s1", [t1, t2], [t1, t2], True)
    """
    id = None
    tasks = []
    chains = []
    preemptive = True
    trace_length = 0
    step_size = 0.1
    epsilon = 0.0000001
    hyper_period = 0
    max_offset = 0
    schedule_exe = None

    def __init__(self, s_id, s_tasks, s_preemptive):
        """Creates a scheduler represented by ID, Tasks.
                :param s_id: Unique identifier.
                :type s_id: String
                :param s_tasks: Set of tasks that need to be scheduled.
                :type s_tasks: Set
                :param s_preemptive: Defines if the jobs are preemptive.
                :type s_preemptive: Boolean
        """
        self.id = s_id
        self.preemptive = s_preemptive
        periods = []
        offsets = []
        # The tasks are sorted w.r.t. the periods of each task.
        # The list is in the order from task with the lowest period to highest period
        #s_tasks.sort(key=lambda task: task.period, reverse=False)
        i = 1
        for task in s_tasks:
            # Collect all periods and offsets of a task set
            periods.append(task.period)
            offsets.append(task.phase)
            # Set priority for each task accordingly to its order
            task.priority = i
            blocking_time = 0
            for blocking_task in s_tasks[i:]:
                if blocking_task.wcet > blocking_time:
                    blocking_time = blocking_task.wcet
            task.blocking_time = blocking_time
            # Compute the worse case response time of the current task
            if s_preemptive:
                task.rt = self.tda(task, s_tasks[:(i - 1)])
            else:
                task.rt = self.tda_blocking(task, s_tasks[:(i - 1)])
            if task.rt > task.deadline or task.rt == 0:
                raise ValueError("TDA Result: WCRT bigger than deadline!")
            i += 1
        # Determine hyper-period and maximum offset of the task set
        # if periods and 0 not in periods:
        #     n = n0 = max(periods)
        #     periods.remove(n)
        #     while any(n % m for m in periods):
        #         n += n0
        #     self.hyper_period = n
        # Determine maximum offset
        self.max_offset = max(offsets)
        self.tasks = s_tasks
        # Determine trace length
        self.trace_length = 1000

    @staticmethod
    def workload(period, c, t):

        return c * math.ceil(float(t) / period)

    def tda(self, task, hp_tasks):
        """Implementation of TDA to calculate worst case response time
           source: https://github.com/kuanhsunchen/MissRateSimulator/blob/master/TDA.py

            :return: WCRT
            """
        c = task.wcet
        r = c
        while True:
            i = 0
            for itask in hp_tasks:
                i = i + self.workload(itask.period, itask.wcet, r)

            if r < i + c:
                r = i + c
            else:
                return r

    def tda_blocking(self, task, hp_tasks):
        """Implementation of TDA to calculate worst case response time
           source: https://github.com/kuanhsunchen/MissRateSimulator/blob/master/TDA.py

            :return: WCRT
            """
        c = task.wcet
        r = c
        b = task.blocking_time
        while True:
            i = 0
            for itask in hp_tasks:
                i = i + b + self.workload(itask.period, itask.wcet, r)

            if r < i + c + b:
                r = i + c + b
            else:
                return r

    def schedule(self):
        """Example schedule, fixed priority and preemptive with a resolution of 1 time unit

        :return: A dict with {task: [(discrete time values of execution)]}
        """

        # Initialise result dict
        result = dict()
        for task in self.tasks:
            result[task] = []
        # Determine explicit execution times of each jobs
        for time in range(self.trace_length * 10):
            curr_job = None
            # Select the task with highest priority that is not already completed
            for task1 in self.tasks:
                # Reset execution progress for new period
                if float(format((time - task1.phase) / 10, ".1f")) % task1.period == 0:
                    task1.exec_progress = 0
                if task1.execution == 0 and time < task1.phase:
                    continue
                for task2 in self.tasks:
                    prio = 9999
                    if curr_job:
                        prio = curr_job.priority
                    if (task1.id is not task2.id and task1.priority < task2.priority
                            and task1.exec_progress < task1.wcet and task1.priority < prio) or\
                            (task1.priority > task2.priority and task2.exec_progress >= task2.wcet and
                             task1.exec_progress < task1.wcet and task1.priority < prio) or\
                            (time >= task1.phase and task1.phase < task2.phase and task1.priority > task2.priority and
                             task1.exec_progress < task1.wcet and task1.priority < prio):
                        curr_job = task1
            if not curr_job:
                continue
            curr_job.exec_progress = float(format(curr_job.exec_progress + 0.1, ".1f"))
            curr_job.execution += 1
            result[curr_job].append(float(format(time / 10, ".1f")))
        self.schedule_exe = result
        return result

    def simplify(self, inp):
        """This method joins coherend execution times.

        :return: indices of execution times of the jobs (start, end)
        """
        if len(inp) == 0:
            return []
        if len(inp) == 1:
            return [(0, 0)]
        lower_limit = self.step_size - self.epsilon
        upper_limit = self.step_size + self.epsilon
        res = []
        start_id = inp[0]
        prev_val = inp[0]
        for i in range(1, len(inp)):
            val = inp[i]
            diff = val - prev_val
            if diff < lower_limit or diff > upper_limit:
                res.append((start_id, float(format(inp[i - 1] + 0.1, ".1f"))))
                start_id = inp[i]
            prev_val = val
        res.append((start_id, float(format(inp[i] + 0.1, ".1f"))))
        return res

    def simplify_schedule(self, schedule):
        result = dict()
        for task in schedule:
            result[task] = []
            i_res = self.simplify(schedule[task])
            same_period = []
            for execution in i_res:
                if not same_period:
                    same_period.append(execution)
                elif math.floor(float(format((execution[1] - task.phase / 10) / task.period, ".1f"))) ==\
                        math.floor(float(format((same_period[0][0] - task.phase/10) / task.period, ".1f"))):
                    same_period.append(execution)
                else:
                    result[task].append((same_period[0][0], same_period[-1][1]))
                    same_period = [execution]
            result[task].append((same_period[0][0], same_period[-1][1]))
        return result
