import unittest
import stt.task as t
import stt.chain as c
import stt.analyser as a
import stt.eventSimulator as es
import math


class TestTask(unittest.TestCase):

    def test_two_interconnected_task_sets(self):
        task_sets = []
        task_set_interconnected = []
        schedules = []
        cause_effect_chain_sets = []
        cause_effect_chain_set_interconnected = []
        """
        Create Task Sets
        """
        # Create task set 0: t0 = (50, 10, 0), t1 = (50, 10, 0)
        task_set_0 = [t.Task("0", 0, 5, 5, 10, 10, 0), t.Task("1", 0, 5, 5, 10, 10, 1)]
        self.assertEqual(len(task_set_0), 2)
        # Create task set 1: t0 = (10, 60, 0), t1 = (30, 100, 0)
        task_set_1 = [t.Task("0", 0, 10, 10, 60, 60, 0), t.Task("1", 0, 30, 30, 100, 100, 1)]
        self.assertEqual(len(task_set_1), 2)
        # Add tasks to task set
        task_sets.append(task_set_0)
        task_sets.append(task_set_1)
        # Create and append communication-task set C: t0 = (1, 200, 0)
        task_set_interconnected.append(t.Task("0", 0, 1, 1, 200, 200, 0, message=True))
        self.assertEqual(len(task_sets), 2)
        """
        Create Cause-Effect Chains
        """
        # Create cause-effect chain set 0: E0 = (t0 -> t1)
        cause_effect_chain_set_0 = [c.CauseEffectChain("0", [task_sets[0][0], task_sets[0][1]])]
        # Create cause-effect chain set 1: E0 = (t1 -> t0)
        cause_effect_chain_set_1 = [c.CauseEffectChain("0", [task_sets[1][1], task_sets[1][0]])]
        # Add cause effect-chains to cause effect-chain set
        cause_effect_chain_sets.append(cause_effect_chain_set_0)
        cause_effect_chain_sets.append(cause_effect_chain_set_1)
        # Create and add interconnected cause-effect chain set: E01 = (E00 -> tc0 -> E10)
        cause_effect_chain_set_interconnected.append(
            c.CauseEffectChain("0", [task_sets[0][0], task_sets[0][1],
                                     task_set_interconnected[0], task_sets[1][1],
                                     task_sets[1][0]],
                               [cause_effect_chain_sets[0][0],
                                task_set_interconnected[0],
                                cause_effect_chain_sets[1][0]]))
        """
        First Analyses (TDA, Sporadic End-to-End)
        """
        # Create an analyzer to determine response times with TDA
        analyzer = a.Analyser("0")
        analyzer.tda_task_set(task_sets, True)
        self.assertEqual(task_sets[0][0].rt, 5)
        self.assertEqual(task_sets[0][1].rt, 10)
        self.assertEqual(task_sets[1][0].rt, 10)
        self.assertEqual(task_sets[1][1].rt, 40)
        i = 1
        for task in task_set_interconnected:
            task.rt = analyzer.tda_blocking(task, task_set_interconnected[:(i - 1)])
            if task.rt > task.deadline or task.rt == 0:
                raise ValueError("TDA Result: WCRT bigger than deadline!")
            i += 1
        # Sporadic End-to-End Analyses
        analyzer.davare(cause_effect_chain_sets)
        self.assertEqual(cause_effect_chain_sets[0][0].e2e_latency, 35)
        self.assertEqual(cause_effect_chain_sets[1][0].e2e_latency, 210)
        analyzer.reaction_sporadic(cause_effect_chain_sets)
        self.assertEqual(cause_effect_chain_sets[0][0].jj_react, 30)
        self.assertEqual(cause_effect_chain_sets[1][0].jj_react, 210)
        analyzer.age_sporadic(cause_effect_chain_sets)
        self.assertEqual(cause_effect_chain_sets[0][0].jj_age, 20)
        self.assertEqual(cause_effect_chain_sets[1][0].jj_age, 150)
        """
        Second Analyses (Exact Simulation, Exact End-to-End)
        """
        i = 0
        for task_set in task_sets:
            # Event-based simulator
            simulator = es.eventSimulator(len(task_set), task_set)
            # Determination of the variables used to compute the stop condition of the simulation
            max_e2e_latency = max(cause_effect_chain_sets[i], key=lambda chain: chain.e2e_latency).e2e_latency
            max_phase = max(task_set, key=lambda task: task.phase).phase
            hyper_period = analyzer.determine_hyper_period(task_set)
            period_lowest_priority_task = task_set[-1].period
            # Stop condition is the max number of jobs from the lowest priority task
            simulator.dispatcher(
                math.ceil(int(((2 * hyper_period + max_phase / period_lowest_priority_task) + max_e2e_latency) / 10)))
            # Simulate
            schedule = simulator.e2e_result()
            schedules.append(schedule)
            for task in task_set:
                task.jobs = schedule[task]
            # Analyze the cause-effect chains
            for chain in cause_effect_chain_sets[i]:
                analyzer.max_age(schedule, chain)
                analyzer.reaction(schedule, chain),
                # Kloda Analysis
                for release_time_first_task_in_chain in range(0, hyper_period - chain.chain[0].period,
                                                              chain.chain[0].period):
                    kloda = analyzer.kloda(chain.chain, release_time_first_task_in_chain)
                    if chain.kloda < kloda:
                        chain.kloda = kloda
                chain.kloda += chain.chain[0].period
            i += 1
        """
        Interconnected Analysis
        """
        # GALS Analysis
        analyzer.age_interconnected(cause_effect_chain_set_interconnected)
        # Sporadic End-to-End Analyses for interconnected chains
        analyzer.davare([cause_effect_chain_set_interconnected])
        self.assertEqual(cause_effect_chain_set_interconnected[0].e2e_latency, 446)
        analyzer.reaction_sporadic([cause_effect_chain_set_interconnected])
        self.assertEqual(cause_effect_chain_set_interconnected[0].jj_react, 441)
        analyzer.age_sporadic([cause_effect_chain_set_interconnected])
        self.assertEqual(cause_effect_chain_set_interconnected[0].jj_age, 381)
        print("breakpoint")


if __name__ == '__main__':
    unittest.main()
