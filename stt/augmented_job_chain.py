"""Augmented job chains."""


class AugJobChain:
    """Augmented job chain."""
    job_chain = []  # list of jobs
    ext_activity = 0.0  # external activity
    actuation = 0.0  # actuation

    def __init__(self, job_chain=None, ext_activity=None, actuation=None):
        """Create an augmented job chain."""
        if job_chain is not None:
            self.job_chain = job_chain
        if ext_activity is not None:
            self.ext_activity = ext_activity
        if actuation is not None:
            self.actuation = actuation

    def add_job(self, job):
        """Add a job to the job chain."""
        self.job_chain.append(job)

    def set_ext_activity(self, value):
        """Set external activity of the augmented job chain."""
        self.ext_activity = value

    def set_actuation(self, value):
        """Set actuation of the augmented job chain."""
        self.actuation = value

    def length(self):
        """Return the length of the augmented job chain."""
        return (self.actuation-self.ext_activity)
