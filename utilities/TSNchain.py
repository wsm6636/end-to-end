"""Representation of cause-effect chains."""


class TSNCauseEffecChain:
    """Cause-effect chain."""

    def __init__(self, id, chain, interconnected=[]):
        """Initialize a cause-effect chain."""
        self.id = id  # unique identifier
        self.chain = chain  # list of all tasks in the chain
        # List of local cause-effect chains and communication tasks. (Only in
        # the interconnected case.)

        self.interconnected = interconnected

        # Analysis results: (Are added during the analysis.)

        self.inter_tsn_age = 0  # TSN 
        self.inter_tsn_react = 0 # TSN 

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
