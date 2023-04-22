"""End-to-End (e2e) Analysis."""

import math
import utilities.task
import utilities.augmented_job_chain as aug
import utilities.TSNtask

debug_flag = False  # flag to have breakpoint() when errors occur


class Analyzer:
    """Analyzer to do the analysis."""

    def __init__(self, e_id):
        """Creates an analyzer represented by ID."""
        self.id = e_id  # unique identifier

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
    # Gunzel analyses from 'Timing Analysis of Asynchronized Distributed
    # Cause-Effect Chains' (2021).
    ###

    def max_age_Gunzel(self, schedule, task_set, chain, max_phase, hyper_period,
                    reduced=False):
        """Gunzel maximum data age time analysis.

        We construct all immediate backward augmented job chains and then
        choose the maximal length of them.
        Note: The schedule has to be build beforehand with the event scheduler.
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
                if debug_flag:
                    breakpoint()
                else:
                    return

            # Last job in the job chain:
            next_job = schedule.get(chain.chain[-1])[position]

            # Find actuation.
            if reduced:
                actuation = schedule.get(chain.chain[-1])[position][1]
            else:
                actuation = schedule.get(chain.chain[-1])[position+1][1]

            # Construct augmented job chain with help function.
            job_chain = self.imm_bw_jc(next_job, chain.length()-1, schedule,
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
                if debug_flag:
                    breakpoint()
                else:
                    return
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
            candidates.append(aug.AugJobChain(
                    job_chain=job_chain,
                    ext_activity=ext_activity,
                    actuation=actuation))

        # Compare length of candidates.
        max_cand = max(candidates, key=lambda cand: cand.length())
        max_length = max_cand.length()

        # Results.
        if reduced:
            chain.Gunzel_red_age = max_length
        else:
            chain.Gunzel_age = max_length
        return max_length

    def imm_bw_jc(self, current_job, c_len, schedule, chain, key=0):
        """Compute immediate forward job chain recursively.

        Used as help function for max_age_Gunzel(). Returns None if the job chain
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

    def reaction_Gunzel(self, schedule, task_set, chain, max_phase, hyper_period):
        """Gunzel maximum reaction time analysis.

        We construct all immediate forward augmented job chains and then
        choose the maximal length of them.
        Note: The schedule has to be build beforehand with the event scheduler.
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
                if debug_flag:
                    breakpoint()
                else:
                    return

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
            job_chain = self.imm_fw_jc(next_job, chain.length()-1, schedule,
                                       chain, key=0)

            # Compute actuation.
            actuation = job_chain[-1][1]

            # Add augmented job chain to candidates.
            candidates.append(aug.AugJobChain(
                    job_chain=job_chain,
                    ext_activity=ext_activity,
                    actuation=actuation))

        # Compare length of candidates.
        max_cand = max(candidates, key=lambda cand: cand.length())
        max_length = max_cand.length()

        # Results.
        chain.Gunzel_react = max_length
        return max_length

    def imm_fw_jc(self, current_job, c_len, schedule, chain, key=0):
        """Compute immediate forward job chain recursively

        Used as help function for reaction_Gunzel().
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

    def reaction_inter_Gunzel(self, chain_set):
        """Gunzel maximum reaction time analysis for interconnected cause-effect
        chains.

        Input: chain_set is a list of cause-effect chains with entry at
        interconnected.
        Note: The chains have to be analyzed by Gunzel single ECU maximum reaction
        time analysis beforehand. ( reaction_Gunzel() )
        """
        for chain in chain_set:
            inter_Gunzel_react = 0  # total reaction time
            for i in range(0, len(chain.interconnected)):
                # Case: i is a communication task.
                if isinstance(chain.interconnected[i], utilities.task.Task):
                    inter_Gunzel_react += (chain.interconnected[i].period
                                        + chain.interconnected[i].rt)
                # Case: i is a cause-effect chain.
                else:
                    inter_Gunzel_react += chain.interconnected[i].Gunzel_react
                    
            # Store result.
            chain.inter_Gunzel_react = inter_Gunzel_react
            

    def max_age_inter_Gunzel(self, chain_set, reduced=False):
        """Gunzel reduced maximum data age analysis for interconnected
        cause-effect chains.

        Input: chain_set is a list of cause-effect chains with entry at
        interconnected.
        Note: The chains have to be analyzed by Gunzel single ECU maximum data age
        analysis beforehand. ( max_age_Gunzel() and max_age_Gunzel(reduced=True) )
        """

        for chain in chain_set:
            m = len(chain.interconnected)  # chain length
            inter_Gunzel_age = 0  # total data age
            for i in range(0, m-1):
                # Case: i is a communication task.
                if isinstance(chain.interconnected[i], utilities.task.Task):
                    inter_Gunzel_age += (chain.interconnected[i].period
                                          + chain.interconnected[i].rt)
                    #这里改成TSN的rt，response time
                # Case: i is a cause-effect chain.
                else:
                    inter_Gunzel_age += chain.interconnected[i].Gunzel_age

            # Handle the last cause-effect chain in the list.
            if reduced:
                inter_Gunzel_age += chain.interconnected[m-1].Gunzel_red_age
            else:
                inter_Gunzel_age += chain.interconnected[m-1].Gunzel_age

            # Store result.
            chain.inter_Gunzel_age = inter_Gunzel_age
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
            for i in range(0, len(chain.interconnected)):
                # Case: i is a communication task.
                if isinstance(chain.interconnected[i], utilities.TSNtask.tsnTask):
                    inter_tsn_react += (chain.interconnected[i].period_tsn
                                        + chain.interconnected[i].rt_tsn)
                    # print("rt")
                    # print(chain.interconnected[i].rt_tsn)
                # Case: i is a cause-effect chain.
                else:
                    inter_tsn_react += chain.interconnected[i].Gunzel_react
                    
            # Store result.
            chain.inter_tsn_react = inter_tsn_react

    def max_age_inter_tsn(self, chain_set, reduced=False):
        """Gunzel reduced maximum data age analysis for interconnected
        cause-effect chains.

        Input: chain_set is a list of cause-effect chains with entry at
        interconnected.
        Note: The chains have to be analyzed by Gunzel single ECU maximum data age
        analysis beforehand. ( max_age_Gunzel() and max_age_Gunzel(reduced=True) )
        """

        for chain in chain_set:
            m = len(chain.interconnected)  # chain length
            inter_tsn_age = 0  # total data age
            for i in range(0, m-1):
                # Case: i is a communication task.
                if isinstance(chain.interconnected[i], utilities.TSNtask.tsnTask):
                    inter_tsn_age += (chain.interconnected[i].period_tsn
                                            + chain.interconnected[i].rt_tsn)
                    #这里改成TSN的rt，response time
                # Case: i is a cause-effect chain.
                else:
                    inter_tsn_age += chain.interconnected[i].Gunzel_age

            # Handle the last cause-effect chain in the list.
            if reduced:
                inter_tsn_age += chain.interconnected[m-1].Gunzel_red_age
            else:
                inter_tsn_age += chain.interconnected[m-1].Gunzel_age

            # Store result.
            chain.inter_tsn_age = inter_tsn_age
    ###
    # Davare analysis from 'Period Optimization for Hard Real-time Distributed
    # Automotive Systems' (2007).
    ###

    def davare(self, chain_sets):
        """End-to-end latency analysis from Davare.

        Input: chain_sets is a list of lists of chains.
        """
        for chain_set in chain_sets:
            for chain in chain_set:
                # Compute the latency for chain.
                latency = 0
                for task in chain.chain:
                    latency += task.period + task.rt
                # Store result.
                chain.davare = latency
    def davare_tsn(self, chain_sets):
        """End-to-end latency analysis from Davare.

        Input: chain_sets is a list of lists of chains.
        """
        for chain_set in chain_sets:
            for chain in chain_set:
                # Compute the latency for chain.
                latency = 0
                for task in chain.chain:
                    latency += task.period + task.rt
                # Store result.
                chain.davare_tsn = latency

