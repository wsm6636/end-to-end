"""Representation of cause-effect chains."""


class CauseEffectChain:
    """Cause-effect chain."""

    def __init__(self, id, chain, interconnected=[]):
        # ,tsntask=False
        """Initialize a cause-effect chain."""
        self.id = id  # unique identifier
        self.chain = chain  # list of all tasks in the chain
        # List of local cause-effect chains and communication tasks. (Only in
        # the interconnected case.)
        
        # if tsntask:
        #     self.tsntask = interconnected
        # else:
        self.interconnected = interconnected

        # Analysis results: (Are added during the analysis.)
        self.davare = 0  # Davare
        self.duerr_age = 0  # Duerr max data age
        self.duerr_react = 0  # Duerr max reaction time
        self.Gunzel_age = 0  # Gunzel max data age
        self.Gunzel_react = 0  # Gunzel max reaction time
        self.Gunzel_red_age = 0  # Gunzel reduced max data age
        self.inter_Gunzel_age = 0  # Gunzel max data age for interconn
        self.inter_Gunzel_red_age = 0  # Gunzel reduced max data age for interconn
        self.inter_Gunzel_react = 0  # Gunzel max reaction time for interconn
        self.kloda = 0  # Kloda
        self.inter_tsn_age = 0  # TSN 
        self.inter_tsn_react = 0 # TSN 
        self.davare_tsn = 0 

    def length(self):
        """Compute the length of a cause-effect chain."""
        return len(self.chain)

    @property
    def chain_disorder(self):
        """Compute the chain disorder. (Not explained in Gunzel paper.)
        The disorder of a chain is the number of priority inversions along
        the data propagation path.
        """
        return sum(1 if self.chain[i].priority > self.chain[i+1].priority
                   else 0 for i in range(len(self.chain)-1))
