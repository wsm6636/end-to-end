"""End-to-End (e2e) Analysis."""

import math
import stt.task
import stt.augmented_job_chain as aug


class Analyzer:

    id = None  # unique identifier

    def __init__(self, e_id):
        """Creates an analyzer represented by ID."""
        self.id = e_id

    @staticmethod
    def determine_hyper_period(task_set):
        """Determine the hyperperiod of task_set."""
        # Collect periods.
        periods = []
        for task in task_set:
            if task.period not in periods:
                periods.append(task.period)
        # Compute least common multiple = hyperperiod.
        lcm = periods[0]
        for i in periods[1:]:
            lcm = int(lcm * i / math.gcd(lcm, i))
        return lcm

    @staticmethod
    def workload(period, wcet, time):
        """Workload function for TDA.

        Help function for tda().
        """
        return wcet * math.ceil(float(time) / period)

    def tda(self, task, hp_tasks):
        """Implementation of TDA to calculate worst-case response time.

        Source:
        https://github.com/kuanhsunchen/MissRateSimulator/blob/master/TDA.py
        """
        c = task.wcet  # WCET
        r = c  # WCRT
        while True:
            i = 0  # interference
            for itask in hp_tasks:
                i = i + self.workload(itask.period, itask.wcet, r)

            if r < i + c:
                r = i + c
            else:
                return r

    ###
    # Our analyses from 'Timing Analysis of Asynchronized Distributed
    # Cause-Effect Chains' (2021).
    ###

    def max_age_our(self, schedule, task_set, chain, max_phase, hyper_period,
                    shortened=False):
        """ Result of our maximum data age time analysis.

        We construct all immediate backward augmented job chains and then
        choose the maximal length of them.
        """
        # Compute maximal first read.
        first_jobs = []
        for task in task_set:
            first_jobs.append(schedule.get(task)[0])
        max_first_read = max(first_jobs, key=lambda first_job: first_job[0])[0]

        # Construct all valid immediate backward augmented job chains.
        candidates = []

        # Position for the last job in the chain.
        position = -1
        while True:
            # We start with position = 0 (1st job).
            position += 1

            # Checking for mistakes.
            if len(schedule.get(chain.chain[-1])) < position:
                breakpoint()

            # Last job in the job chain:
            next_job = schedule.get(chain.chain[-1])[position]

            # Find actuation.
            if shortened:
                actuation = schedule.get(chain.chain[-1])[position][1]
            else:
                actuation = schedule.get(chain.chain[-1])[position+1][1]

            # Construct augmented job chain with help function.
            job_chain = self.imm_bw_jc(next_job, chain.length-1, schedule,
                                       chain, key=0)

            # Handle incomplete job chains.
            if job_chain is None:
                continue

            # Define external activity.
            ext_activity = job_chain[0][0]

            # Find first job after ext_activity
            job_after_ext_activity = None
            flag = False
            for job in schedule.get(chain.chain[0]):
                if job[0] > ext_activity:
                    flag = True
                    break
            if flag is False:  # no event after ext_activity could be found
                breakpoint()
            else:
                job_after_ext_activity = job

            # Check if the augmented job chain is valid.
            if job_after_ext_activity[0] > max_first_read:
                pass
            else:
                continue

            # End condition.
            if ext_activity < max_phase + 2*hyper_period:
                pass
            else:
                break

            # Add augmented job chain to candidates.
            candidates.append(aug.aug_job_chain(
                    job_chain=job_chain,
                    ext_activity=ext_activity,
                    actuation=actuation))

        # Compare length of candidates.
        max_cand = max(candidates, key=lambda cand: cand.length())
        max_length = max_cand.length()

        # Results.
        if shortened:
            chain.sim_sh_age = max_length
        else:
            chain.sim_age = max_length
        return max_length

    def imm_bw_jc(self, current_job, c_len, schedule, chain, key=0):
        """ Compute immediate forward job chain recursively.

        Used as help function for max_age_our(). Returns None if the job chain
        is incomplete.
        """
        # Initial case.
        if key == 0:
            res = self.imm_bw_jc(current_job, c_len, schedule, chain,
                                 key=key+1)
            if res is None:  # incomplete job chain
                return None
            else:
                return res + [current_job]  # build from right to left

        # Intermediate cases. Adding one job.
        elif key <= c_len:
            flag_found = False
            # Search in reversed schedule for next job.
            for next_job in schedule.get(chain.chain[-key-1])[::-1]:
                if current_job[0] >= next_job[1]:  # condition for next job
                    flag_found = True
                    break
            # Case: No job was found.
            if flag_found is False:
                return None  # indicate incomplete job chain
            # Case: Job was found.
            else:
                res = self.imm_bw_jc(next_job, c_len, schedule, chain,
                                     key=key+1)
                if res is None:  # incomplete job chain.
                    return None
                else:
                    return res + [next_job]  # build from right to left

        # Final case. (key > c_len)
        else:
            return []

    def reaction_our(self, schedule, task_set, chain, max_phase, hyper_period):
        """ Result of our maximum reaction time analysis.

        We construct all immediate forward augmented job chains and then
        choose the maximal length of them.
        """
        # Compute maximal first read.
        first_jobs = []
        for task in task_set:
            first_jobs.append(schedule.get(task)[0])
        max_first_read = max(first_jobs, key=lambda first_job: first_job[0])[0]

        # Construct all valid immediate forward augmented job chains.
        candidates = []

        # Position for the first job in the chain.
        position = 0
        while True:
            # We start with position = 1 (2nd job) because we need one previous
            # job for the definition of external activity.
            position += 1

            # Checking for mistakes.
            if len(schedule.get(chain.chain[0])) < position:
                breakpoint()

            # First job in the job chain.
            next_job = schedule.get(chain.chain[0])[position]

            # External activity.
            ext_activity = schedule.get(chain.chain[0])[position-1][0]

            # Check if valid
            if next_job[0] > max_first_read:
                pass
            else:
                continue

            # End condition.
            if ext_activity < max_phase + 2*hyper_period:
                pass
            else:
                break

            # Construct augmented job chain with help function.
            job_chain = self.imm_fw_jc(next_job, chain.length-1, schedule,
                                       chain, key=0)

            # Compute actuation.
            actuation = job_chain[-1][1]

            # Add augmented job chain to candidates.
            candidates.append(aug.aug_job_chain(
                    job_chain=job_chain,
                    ext_activity=ext_activity,
                    actuation=actuation))

        # Compare length of candidates.
        max_cand = max(candidates, key=lambda cand: cand.length())
        max_length = max_cand.length()

        # Results.
        chain.sim_react = max_length
        return max_length

    def imm_fw_jc(self, current_job, c_len, schedule, chain, key=0):
        """ Compute immediate forward job chain recursively

        Used as help function for reaction_our().
        """
        # Initial case.
        if key == 0:
            # Build from left to right:
            return [current_job] + self.imm_fw_jc(current_job, c_len, schedule,
                                                  chain, key=key+1)

        # Intermediate cases. Adding one job.
        elif key <= c_len:
            flag_found = False
            # Search for next job.
            for next_job in schedule.get(chain.chain[key]):
                if current_job[1] <= next_job[0]:  # condition for next job
                    flag_found = True
                    break
            # Case: No job was found.
            if flag_found is False:
                print("ERROR")
            # Case: Job was found.
            else:
                return [next_job] + self.imm_fw_jc(next_job, c_len, schedule,
                                                   chain, key=key+1)

        # Final case. (key > c_len)
        else:
            return []

    def reaction_inter_our(self, chain_set):
        """Maximum reaction time analysis for interconnected cause-effect
        chains as described in our paper.

        Input: chain_set is a list of cause-effect chains with entry at
        interconnected.
        """
        for chain in chain_set:
            interconnected_react = 0  # total reaction time
            for i in range(0, len(chain.interconnected)):
                # Case: i is a communication task.
                if isinstance(chain.interconnected[i], stt.task.Task):
                    interconnected_react += (chain.interconnected[i].period
                                             + chain.interconnected[i].rt)
                # Case: i is a cause-effect chain.
                else:
                    interconnected_react += chain.interconnected[i].sim_react
            # Store result.
            chain.interconnected_react = interconnected_react

    def max_age_inter_our(self, chain_set):
        """Maximum data age analysis for interconnected cause-effect chains as
        described in our paper.

        Input: chain_set is a list of cause-effect chains with entry at
        interconnected.
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


    ###
    # Davare analysis from 'Period Optimization for Hard Real-time Distributed
    # Automotive Systems' (2007).
    ###

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

    ###
    # Duerr analysis from 'End-to-End Timing Analysis of Sporadic Cause-Effect
    # Chains in Distributed Systems' (2019).
    ###

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

    ###
    # Kloda analysis from 'Latency analysis for data chains of real-time
    # periodic tasks' (2018).
    ###

    def kloda(self, chain, hyper_period):
        """Kloda analysis for synchronous releases."""
        for release_first_task_in_chain in range(0, max(1, hyper_period),
                                                 chain.chain[0].period):
            kloda = self.kloda_rec(chain.chain, release_first_task_in_chain,
                                   beginning=True)
            if chain.kloda < kloda:
                chain.kloda = kloda
        return chain.kloda


    def kloda_rec(self, chain, release_time_producer, beginning=True):
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
        return add + release_time_consumer - release_time_producer + self.kloda_rec(chain_minus_one, release_time_consumer, beginning=False)
