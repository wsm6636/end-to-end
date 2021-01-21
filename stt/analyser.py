"""Representation of the End-to-End (e2e) Analysis.

:Filename: e2eAnalyser.py
:Author: Marco Dürr (marco.duerr@tu-dortmund.de)
:Date: 07.12.18
"""
import math
import stt.task
import stt.augmented_job_chain as aug

class Analyser:
    """Class Drawer

            **Global Variables**
                :cvar id: Unique identifier.
                :type id: String
                :cvar schedule_exe: Start and End times of each job related to the task.
                :type schedule_exe: Dict
                :cvar trace_length: Time how long the schedule is executed.
                :type trace_length: Integer
                :cvar job_chain_age: Includes all valid job chains analysed under max age semantic.
                :type job_chain_age: List
                :cvar job_chain_reaction: Includes all valid job chains analysed under reaction semantic.
                :type job_chain_reaction: List
                :cvar job_chain_current: Current path of the analysed job chain.
                :type job_chain_current: List
                :cvar key: Number of tasks in the schedule.
                :type key: Int

            **Usage**
                >>> import stt.analyser
                >>> myAnalyser = stt.analyser.Analyser("a1", [])
    """

    id = None
    schedule_exe = None
    trace_length = None
    task = None
    chain = None
    chains = []
    job_chain_age = []
    job_chain_reaction = []
    job_chain_current = []
    key = None
    flag = False

    def __init__(self, e_id):
        """Creates an analyser represented by ID and Scheduler.
            :param e_id: Unique identifier.
            :type e_id: String
        """
        self.id = e_id

    @staticmethod
    def sort_task_set_by_priority(task_set):
        return sorted(task_set, key=lambda task: task.priority)

    @staticmethod
    def sort_task_set_by_period(task_set):
        return sorted(task_set, key=lambda task: task.period)

    @staticmethod
    def set_priority_task_set(task_set):
        i = 0
        for task in task_set:
            task.priority = i
            i += 1

    @staticmethod
    def determine_blocking_time(task_set):
        i = 0
        for task in task_set:
            task.blocking_time = max(task_set[i:], key=lambda blocking_task: blocking_task.wcet)
            i += 1

    @staticmethod
    def determine_hyper_period(task_set):
        periods = []
        for task in task_set:
            if task.period not in periods:
                periods.append(task.period)
        lcm = periods[0]
        for i in periods[1:]:
            lcm = int(lcm * i / math.gcd(lcm, i))
            # print(lcm)
        return lcm

    def tda_task_set(self, task_sets, preemptive):
        for task_set in task_sets:
            i = 1
            for task in task_set:
                # Compute the worse case response time of the current task
                if preemptive:
                    task.rt = self.tda(task, task_set[:(i - 1)])
                else:
                    task.rt = self.tda_blocking(task, task_set[:(i - 1)])
                if task.rt > task.deadline or task.rt == 0:
                    raise ValueError("TDA Result: WCRT bigger than deadline!")
                i += 1

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

    # def max_age(self, schedule, chain):
    #     """ Analyses all valid max age End-to-End job chains of the exact schedule. This method triggers the recursive
    #         function, beginning from the last task in the chain to the first (backwards).
    #
    #     :return: All job chains of an exact schedule analysed due to max age semantic.
    #     """
    #     # Clearing of the resulting list before the analysis starts
    #     self.job_chain_age = []
    #     self.schedule_exe = schedule
    #     self.chain = chain
    #     chain_length = chain.length - 1
    #     # Determine maximum phase of the task in the chain
    #     max_phase = 0
    #     for task in chain.chain:
    #         if task.phase > max_phase:
    #             max_phase = task.phase
    #     # The analysis starts with the last job of the last task in chain, hence the schedule is reversed
    #     for job in self.schedule_exe.get(self.chain.chain[chain_length])[::-1]:
    #         self.job_chain_current.append(job)
    #         self.age(chain_length-1, job)
    #         self.job_chain_current = []
    #     max_age = [0, []]
    #     for j_chain in self.job_chain_age[::-1]:
    #         # Consider jobs for job chain only if all tasks released once
    #         if j_chain[0][0] < max_phase:
    #             continue
    #         time = j_chain[chain_length][1] - j_chain[0][0]
    #         if max_age[0] < time:
    #             chain.rt_last_job = int(j_chain[-1][1]) - (math.floor((j_chain[-1][1] - chain.chain[-1].wcet - chain.chain[-1].phase)/chain.chain[-1].period) * chain.chain[-1].period + chain.chain[-1].phase)
    #             max_age = [time, j_chain]
    #     chain.sim_age = max_age[0]
    #     return max_age

    def max_age_OUR(self, schedule, task_set, chain, max_phase, hyper_period, shortened = False):
        """ Result of our maximum reaction time analysis.
            We construct all immediate forward augmented job chains and then
            choose the maximal length of them.
        """
        # compute maximal first read
        first_jobs = []
        for task in task_set:
            first_jobs.append(schedule.get(task)[0])
        max_first_read = max(first_jobs, key=lambda first_job: first_job[0])[0]

        # construct all valid immediate forward augmented job chains
        candidates = [] # all valid imm fw augmented job chains

        # for loop position for immediate forward augmented job chain
        position = 0
        while True:
            position +=1 # we start with position = 1 (=2nd job)

            if len(schedule.get(chain.chain[-1])) < position: # checking for mistakes
                breakpoint()

            actuation = schedule.get(chain.chain[-1])[position][1]
            if shortened:
                next_job = schedule.get(chain.chain[-1])[position]
            else:
                next_job = schedule.get(chain.chain[-1])[position-1]

            # construct augmented job chain
            job_chain = self.imm_bw_jc(next_job, chain.length - 1, schedule, chain, key=0)

            if job_chain is None: # job chain is incomplete
                continue

            # define external activity
            ext_activity = job_chain[0][0]
            # find job after ext_activity
            job_after_ext_activity = None
            flag = False
            for job in schedule.get(chain.chain[0]):
                if job[0] > ext_activity:
                    flag = True
                    break
            if flag == False: # no event after ext_activity could be found
                breakpoint()
            else:
                job_after_ext_activity = job

            # check if valid
            if job_after_ext_activity[0] > max_first_read:
                pass
            else:
                continue

            # check if external activity before max_phase + 2 hyperperiod
            if ext_activity < max_phase + 2*hyper_period:
                pass
            else:
                break

            # add augmented job chain to candidates
            candidates.append(aug.aug_job_chain(job_chain=job_chain, ext_activity=ext_activity, actuation=actuation))

            # Maybe we need to check here if next ext_activity will be above phi + 2 H to prevent bugs?

        # compare length of candidates
        max_length = max(candidates, key=lambda cand: cand.length()).length()

        # results
        if shortened:
            chain.sim_sh_age = max_length
        else:
            chain.sim_age = max_length
        return max_length

    def imm_bw_jc(self, current_job, c_len, schedule, chain, key=0):
        """ Compute immediate forward job chain recursively
        """
        if key == 0: # initial case
            res = self.imm_bw_jc(current_job, c_len, schedule, chain, key = key+1)
            if res is None:
                return None
            else:
                return res + [current_job] # build from right to left

        elif key <= c_len: # adding one job
            flag_found = False
            for next_job in schedule.get(chain.chain[-key-1])[::-1]: # search in reversed schedule and reversed order for backward
                if current_job[0] >= next_job[1]: # condition to add the next job to the list.
                    flag_found = True
                    break
            if flag_found == False: # incomplete (this job could not be found)
                return None
            else:
                res = self.imm_bw_jc(next_job, c_len, schedule, chain, key = key+1)
                if res is None: # incomplete (one of the next jobs could not be found)
                    return None
                else:
                    return res + [next_job] # build from right to left

        else: # final case
            return []

    # def max_age_CASES(self, schedule, chain, max_phase, hyper_period, sample_scenarios = 0, extended = False): # here is some mistake with extended ... everything was viewed as not extended
    #     """ Analyses all valid max age End-to-End job chains of the exact schedule. This method triggers the recursive
    #         function, beginning from the last task in the chain to the first (backwards).
    #     sample_scenarios = 0 (Scenario A in the paper):
    #     the sampling happens at the start of each job of the first task in the cause-effect chain
    #     sample_scenarios = 1 (Scenario B in the paper):
    #     the sampling happens at the release of each job of the first task in the cause-effect chain
    #
    #     :return: All job chains of an exact schedule analysed due to max age semantic.
    #     """
    #     # Clearing of the resulting list before the analysis starts
    #     self.job_chain_age = []
    #     self.schedule_exe = schedule
    #     self.chain = chain
    #     chain_length = chain.length - 1
    #     # The analysis starts with the last job of the last task in chain, hence the schedule is reversed
    #     for job in self.schedule_exe.get(self.chain.chain[chain_length])[::-1]:
    #         self.job_chain_current.append(job)
    #         self.age(chain_length-1, job)
    #         self.job_chain_current = []
    #     max_age = [0, []]
    #     ext_age = [0, []]
    #     for j_chain in self.job_chain_age[::-1]:
    #         # Consider jobs for job chain only if all tasks released once
    #         releasefirst = (math.floor((j_chain[0][1] - chain.chain[0].wcet - chain.chain[0].phase)/chain.chain[0].period) * chain.chain[0].period + chain.chain[0].phase)
    #         if releasefirst < max_phase or releasefirst >= 2 * hyper_period + max_phase:
    #             continue
    #         if sample_scenarios == 0:
    #             time = (j_chain[chain_length][1] # finish of last job in the chain
    #                 - j_chain[0][0]) # start of first job in the chain
    #         else:
    #             time = j_chain[chain_length][1] - releasefirst
    #         if max_age[0] < time: # update values if length of job chain is bigger
    #             chain.age_rt_last_job = int(j_chain[-1][1]) - (math.floor((j_chain[-1][1] - chain.chain[-1].wcet - chain.chain[-1].phase)/chain.chain[-1].period) * chain.chain[-1].period + chain.chain[-1].phase)
    #             chain.age_rt_first_job = j_chain[0][0] - (math.floor((j_chain[0][1] - chain.chain[0].wcet - chain.chain[0].phase)/chain.chain[0].period) * chain.chain[0].period + chain.chain[0].phase)# wrong? j_chain[0][1] at the beginning for response time?
    #             max_age = [time, j_chain]
    #         if extended:
    #             # breakpoint()
    #             try:
    #                 additional = schedule[chain.chain[chain_length]][schedule[chain.chain[chain_length]].index(j_chain[chain_length]) + 1][1] - j_chain[chain_length][1]
    #             except:
    #                 breakpoint()
    #             ext_time = time + additional
    #             if ext_age[0] < ext_time:
    #                 ext_age = [ext_time, j_chain]
    #     chain.sim_age = max_age[0]
    #     if extended:
    #         chain.sim_ext_age = ext_age[0]
    #     return max_age
    #
    # def age(self, key, job):
    #     """ Recursive function that analyses the latest connection between two jobs in related to max age semantic.
    #
    #     :param key: Represents the number of the task that is analysed.
    #     :param job: Previous job of the previous task.
    #     """
    #     if key >= 0:
    #         for c_job in self.schedule_exe.get(self.chain.chain[key])[::-1]:
    #             if c_job[1] <= job[0]:
    #                 for e_job in self.job_chain_age:
    #                     if c_job in e_job:
    #                         self.flag = True
    #                         break
    #                 if not self.flag:
    #                     self.job_chain_current.append(c_job)
    #                     self.age(key-1, c_job)
    #                     break
    #                 break
    #         self.flag = False
    #     else:
    #         # Append the resulting max age job chain in reverse
    #         self.job_chain_age.append(self.job_chain_current[::-1])
    #         self.job_chain_current = []



    # def reaction_CASES(self, schedule, chain, max_phase, hyper_period, sample_scenarios = 0):
    #     """ Analyses all valid reaction time End-to-End job chains of the exact schedule.
    #     sample_scenarios = 0 (Secnario A in the paper):
    #     the sampling happens at the start of each job of the first task in the cause-effect chain
    #     sample_scenarios = 1 (Scenario B in the paper):
    #     the sampling happens at the release of each job of the first task in the cause-effect chain
    #     :return: All job chains of an exact schedule analysed due to reaction time semantic.
    #     """
    #     # Clearing of the resulting list before the analysis starts
    #     self.job_chain_reaction = []
    #     self.schedule_exe = schedule
    #     self.chain = chain
    #     chain_length = chain.length - 1
    #     for job in schedule.get(self.chain.chain[0]):
    #         self.job_chain_current.append(job)
    #         self.react(1, job, chain_length)
    #         self.job_chain_current = []
    #     reaction_time = [0, []]
    #     # Calculate worst-case reaction time
    #     for j_chain in self.job_chain_reaction:
    #         # Consider jobs for job chain only if all tasks released once
    #         releasefirst = (math.floor((j_chain[0][1] - chain.chain[0].wcet - chain.chain[0].phase)/chain.chain[0].period) * chain.chain[0].period + chain.chain[0].phase)
    #         if releasefirst < max_phase + chain.chain[0].period or releasefirst >= 2 * hyper_period + max_phase + chain.chain[0].period:
    #             continue
    #         # The first chain is not considered, since it has no predecessor
    #         if j_chain == self.job_chain_reaction[0]: # can be deleted?
    #             continue
    #         else:
    #             if sample_scenarios == 0:
    #                 # scenario A
    #                 time = (j_chain[chain_length][1] # finishing time of last job in job chain
    #                         - schedule[chain.chain[0]][schedule[chain.chain[0]].index(j_chain[0]) - 1][0]) # start time of the job before the first job in the job chain
    #             else:
    #                 # scenario B
    #                 time = (j_chain[chain_length][1] # finishing time of last job in job chain
    #                         - (math.floor((schedule[chain.chain[0]][schedule[chain.chain[0]].index(j_chain[0]) - 1][1] - chain.chain[0].wcet - chain.chain[0].phase) / chain.chain[0].period) * chain.chain[0].period + chain.chain[0].phase)) # release time of the job before the first job in the job chain
    #         if time > chain.e2e_latency:
    #             breakpoint()
    #         if reaction_time[0] < time: # we replace our values, if the new end-to-end bound is bigger than the existing
    #             # compute the release times of the first and the last job in the job chain
    #             chain.react_rt_last_job = int(j_chain[-1][1]) - (math.floor(
    #                 (j_chain[-1][1] - chain.chain[-1].wcet - chain.chain[-1].phase) / chain.chain[-1].period) * # I dont think that we need to subtract the wcet to obtain the release
    #                                                            chain.chain[-1].period + chain.chain[-1].phase)
    #             chain.react_rt_first_job = j_chain[0][0] - (math.floor(
    #                 (j_chain[0][1] - chain.chain[0].wcet - chain.chain[0].phase) / chain.chain[0].period) * chain.chain[
    #                                                           0].period + chain.chain[0].phase)
    #             #j_chain[0] = (j_chain[1][1] - time, j_chain[0][1]) # why are we doing this? # If we want to replace the start time of the first job in the job chain by the release time, then we have to use j_chain[-1][1]-time
    #             # set new reaction time
    #             reaction_time = [time, j_chain]
    #     chain.sim_react = reaction_time[0]
    #     return reaction_time
    #
    # def react(self, key, job, c_len): # creates job chains and adds them to the list job_chain_reaction of all job chains
    #     """ Recursive function that analyses the latest connection between two jobs in related to reaction time semantic.
    #
    #     :param key: Represents the number of the task that is analysed.
    #     :param job: Previous job of the previous task.
    #     :c_len:
    #     """
    #     if key <= c_len:
    #         for c_job in self.schedule_exe.get(self.chain.chain[key]):
    #             if job[1] <= c_job[0]: # condition to add the next job to the list.
    #                 self.job_chain_current.append(c_job)
    #                 self.react(key+1, c_job, c_len)
    #                 break
    #     else:
    #         self.job_chain_reaction.append(self.job_chain_current)
    #         self.job_chain_current = []


    def reaction_OUR(self, schedule, task_set, chain, max_phase, hyper_period):
        """ Result of our maximum reaction time analysis.
            We construct all immediate forward augmented job chains and then
            choose the maximal length of them.
        """
        # compute maximal first read
        first_jobs = []
        for task in task_set:
            first_jobs.append(schedule.get(task)[0])
        max_first_read = max(first_jobs, key=lambda first_job: first_job[0])[0]

        # construct all valid immediate forward augmented job chains
        candidates = [] # all valid imm fw augmented job chains

        # for loop position for immediate forward augmented job chain
        position = -1
        while True:
            position +=1 # we start with position = 0
            if len(schedule.get(chain.chain[0])) < position+1: # checking for mistakes
                breakpoint()
            ext_activity = schedule.get(chain.chain[0])[position][0]
            next_job = schedule.get(chain.chain[0])[position+1]

            # check if valid
            if next_job[0] > max_first_read:
                pass
            else:
                continue

            # check if external activity before max_phase + 2 hyperperiod
            if ext_activity < max_phase + 2*hyper_period:
                pass
            else:
                break

            # compute immediate forward augmented job chain; if incomplete, PROBLEM
            job_chain = self.imm_fw_jc(next_job, chain.length - 1, schedule, chain, key=0)

            # compute actuation
            actuation = job_chain[-1][1]

            # add augmented job chain to candidates
            candidates.append(aug.aug_job_chain(job_chain=job_chain, ext_activity=ext_activity, actuation=actuation))


        # compare length of candidates
        max_cand = max(candidates, key=lambda cand: cand.length())
        max_length = max_cand.length()

        # results
        chain.sim_react = max_length
        # return max_cand, max_length ###
        return max_length

    def imm_fw_jc(self, current_job, c_len, schedule, chain, key=0):
        """ Compute immediate forward job chain recursively
        """
        if key == 0: # initial case
            return [current_job] + self.imm_fw_jc(current_job, c_len, schedule, chain, key = key+1)

        elif key <= c_len: # adding one job
            for next_job in schedule.get(chain.chain[key]):
                if current_job[1] <= next_job[0]: # condition to add the next job to the list.
                    break
            return [next_job] + self.imm_fw_jc(next_job, c_len, schedule, chain, key = key+1)

        else: # final case
            return []


    def davare(self, chain_sets):
        """ Analysis End-to-End latency for job chain of the exact schedule with the method from Davare.
            This method triggers the recursive function, beginning from the first task in the chain to the last.
        """
        for chain_set in chain_sets:
            for chain in chain_set:
                latency = 0
                for task in chain.chain:
                    # Compute the latency for the current task and store it in the last element of 'end_latency'
                    latency += task.period + task.rt
                chain.e2e_latency = latency

    def reaction_sporadic(self, chain_sets):
        """ Analysis End-to-End latency for job chain of the exact schedule with the method from Marco-2019 paper.
            This method triggers the recursive function, beginning from the first task in the chain to the last.
        """
        for chain_set in chain_sets:
            for chain in chain_set:
                latency = chain.chain[-1].rt + chain.chain[0].period
                for task, next_task in zip(chain.chain[:-1], chain.chain[1:]):
                    # Compute the latency for the current task and store it in the last element of 'end_latency'
                    if task.priority > next_task.priority or next_task.message or task.message:
                        part2 = task.rt
                    else:
                        part2 = 0
                    latency += max(task.rt, next_task.period + part2)
                chain.jj_react = latency

    def reaction_interconnected(self, chain_set):
        """End-to-End analysis for interconnected cause-effect chains as described in our paper.
        """
        for chain in chain_set:
            interconnected_react = 0
            for i in range(0, len(chain.interconnected)):
                if isinstance(chain.interconnected[i], stt.task.Task):
                    interconnected_react += chain.interconnected[i].period + chain.interconnected[i].rt
                else:
                    interconnected_react += chain.interconnected[i].sim_react
            chain.interconnected_react = interconnected_react

    def age_sporadic(self, chain_sets):
        """ Analysis End-to-End latency for job chain of the exact schedule with the method from Marco-2019 paper.
            This method triggers the recursive function, beginning from the first task in the chain to the last.
        """
        for chain_set in chain_sets:
            for chain in chain_set:
                latency = chain.chain[-1].rt
                for task, next_task in zip(chain.chain[:-1], chain.chain[1:]):
                    # Compute the latency for the current task and store it in the last element of 'end_latency'
                    if task.priority > next_task.priority or next_task.message or task.message:
                        part2 = task.rt
                    else:
                        part2 = 0
                    latency += task.period + part2
                chain.jj_age = latency

    def age_interconnected(self, chain_set):
        """End-to-End analysis for interconnected cause-effect chains as described in our paper.
        """
        for chain in chain_set:
            interconnected_age = 0
            for i in range(0, len(chain.interconnected)-1):
                if isinstance(chain.interconnected[i], stt.task.Task):
                    interconnected_age += chain.interconnected[i].period + chain.interconnected[i].rt
                else:
                    interconnected_age += chain.interconnected[i].sim_age
            interconnected_age += chain.interconnected[len(chain.interconnected)-1].sim_sh_age
            chain.interconnected_age = interconnected_age

    def kloda(self, chain, release_time_producer, beginning=True):
        """Recursive function to compute the reaction time by klodas analysis.
        Note: the additional period is already added with the beginning=True option.
        """
        add = 0
        if beginning:
            add += chain[0].period
        producer_task = chain[0]
        if len(chain) == 1:
            return producer_task.rt + add
        chain_minus_one = chain[1::]
        consumer_task = chain_minus_one[0]
        q = 0
        if producer_task.priority > consumer_task.priority or consumer_task.message: # message is an identifier for the communication task (=ECU change)
            q = producer_task.rt
        release_time_consumer = math.ceil((release_time_producer + q) / consumer_task.period) * consumer_task.period
        return add + release_time_consumer - release_time_producer + self.kloda(chain_minus_one, release_time_consumer, beginning=False)
