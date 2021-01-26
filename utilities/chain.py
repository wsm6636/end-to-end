"""Representation of cause-effect chains."""


class CauseEffectChain:
    """Cause-effect chain."""

    def __init__(self, id, chain, interconnected=[]):
        """Initialize a cause-effect chain."""
        self.id = id  # unique identifier
        self.chain = chain  # list of all tasks in the chain
        # List of local cause-effect chains and communication tasks. (Only in
        # the interconnected case.)
        self.interconnected = interconnected

        # Analysis results: (Are added during the analysis.)
        davare = 0  # Davare
        duerr_age = 0  # Duerr max data age
        duerr_react = 0  # Duerr max reaction time
        our_age = 0  # Our max data age
        our_react = 0  # Our max reaction time
        our_red_age = 0  # Our reduced max data age
        inter_our_age = 0  # Our max data age for interconnected
        inter_our_red_age = 0  # Our reduced max data age for interconnected
        inter_our_react = 0  # Our max reaction time for interconnected
        kloda = 0  # Kloda

    def length(self):
        """Compute the length of a cause-effect chain."""
        return len(self.chain)

    @property
    def chain_disorder(self):
        """Compute the chain disorder. (Not explained in our paper.)

        The disorder of a chain is the number of priority inversions along
        the data propagation path.
        """
        return sum(1 if self.chain[i].priority > self.chain[i+1].priority
                   else 0 for i in range(len(self.chain)-1))
