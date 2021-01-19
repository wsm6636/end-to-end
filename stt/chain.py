"""Representation of a CauseEffectChain.

:Filename: chain.py
:Author: Marco Dürr (marco.duerr@tu-dortmund.de)
:Date: 28.09.18?
"""


class CauseEffectChain:
    """Class CauseEffectChain

        **Global Variables**
            :cvar id: Unique identifier.
            :type id: String
            :cvar chain: Irreflexive set of tasks that form the cause-effect chain.
            :type chain: Set

        **Usage**
            >>> import stt.chain
            >>> myCEC = chain.CauseEffectChain("t1", 0, 1, 3, 10, 10)
    """
    id = ""
    chain = []
    age_rt_last_job = 0
    age_rt_first_job = 0
    react_rt_last_job = 0
    react_rt_first_job = 0
    interconnected = []
    length = 0
    periods = 0
    e2e_latency = 0
    jj_age = 0
    jj_react = 0
    sim_age = 0
    sim_react = 0
    sim_sh_age = 0
    sim_ext_age = 0
    interconnected_age = 0
    interconnected_react = 0
    kloda = 0
    deadline = 0
    disorder=None

    def __init__(self, cec_id, cec_chain, interconnected=[]):
        self.id = cec_id
        self.chain = cec_chain
        self.length = len(cec_chain)
        self.disorder = None
        periods = []
        for chain in cec_chain:
            if chain.period not in periods:
                periods.append(chain.period)
        self.periods = len(periods)
        for period in periods:
            self.deadline += period
        self.interconnected = interconnected

    @property
    def chain_disorder(self):
        """
        An disorder of a chain is the number of priority inversions along
        the data propagation path.
        """
        if not self.disorder:
            return sum(1 if self.chain[i].priority > self.chain[i+1].priority else 0  for i in range(len(self.chain)-1))
        else:
            return self.disorder
