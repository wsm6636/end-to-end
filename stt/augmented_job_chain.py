"""Augmented job chains
"""


class aug_job_chain:
    job_chain = []
    ext_activity = 0
    actuation = 0

    def __init__(self, job_chain=None, ext_activity=None, actuation=None):
        if job_chain is not None:
            self.job_chain = job_chain
        if ext_activity is not None:
            self.ext_activity = ext_activity
        if actuation is not None:
            self.actuation = actuation

    def add_job(self, job):
        self.job_chain.append(job)

    def set_ext_activity(self, value):
        self.ext_activity = value

    def set_actuation(self, value):
        self.actuation = value

    def length(self):
        return (self.actuation-self.ext_activity)
