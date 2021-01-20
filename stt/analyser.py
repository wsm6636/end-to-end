"""
End-to-End (e2e) Analysis.
"""
import math
import stt.task
import stt.augmented_job_chain as aug

class Analyser:

    id = None # unique identifier
    # schedule_exe = None
    # trace_length = None
    # task = None
    # chain = None
    # chains = []
    # job_chain_age = []
    # job_chain_reaction = []
    # job_chain_current = []
    # key = None
    # flag = False

    def __init__(self, e_id):
        """Creates an analyser represented by ID.
        """
        self.id = e_id

    # @staticmethod
    # def sort_task_set_by_priority(task_set):
    #     return sorted(task_set, key=lambda task: task.priority)

    # @staticmethod
    # def sort_task_set_by_period(task_set):
    #     return sorted(task_set, key=lambda task: task.period)

    # @staticmethod
    # def set_priority_task_set(task_set):
    #     i = 0
    #     for task in task_set:
    #         task.priority = i
    #         i += 1

    # @staticmethod
    # def determine_blocking_time(task_set):
    #     i = 0
    #     for task in task_set:
    #         task.blocking_time = max(task_set[i:], key=lambda blocking_task: blocking_task.wcet)
    #         i += 1

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

    # def tda_task_set(self, task_sets, preemptive):
    #     for task_set in task_sets:
    #         i = 1
    #         for task in task_set:
    #             # Compute the worse case response time of the current task
    #             if preemptive:
    #                 task.rt = self.tda(task, task_set[:(i - 1)])
    #             else:
    #                 task.rt = self.tda_blocking(task, task_set[:(i - 1)])
    #             if task.rt > task.deadline or task.rt == 0:
    #                 raise ValueError("TDA Result: WCRT bigger than deadline!")
    #             i += 1

    @staticmethod
    def workload(period, c, t): # workload function for TDA
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
                    interconnected_age += chain.interconnected[i].sim_sh_age
            interconnected_age += chain.interconnected[len(chain.interconnected)-1].sim_age
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
