"""Representation of TSN Tasks."""


class TSNTask:
    """A tsn task."""

    def __init__(self, tsntask_id, tsntask_offset, tsntask_hops, tsntask_slot, tsntask_period,
                 tsntask_deadline, 
                 priority=0, 
                #  tsnmessage=False,
                 ):
        """Creates a task represented by ID, Phase, BCET, WCET, Period and
        Deadline.
        """
        self.id = str(tsntask_id)
        self.offset = tsntask_offset  # 偏移量，o
        self.hops = tsntask_hops  #  跳数，h
        self.slot = tsntask_slot  # slot长度，d
        self.period = tsntask_period  # 间隔，p
        self.deadline = tsntask_deadline  # deadline
        self.priority = priority  # a lower value means higher priority
        # self.message = tsnmessage  # flag for communication tasks

        self.rt = 0  # Worst-case response time, specified during analysis

    def __str__(self):
        """Print a task."""
        return (" Type: {type:^}\n ID: {id:^}\n Priority: {priority:^}\n"
                + " Offset: {offset:^} \n Hops: {hops:^} \n Slot: {slot:^} \n"
                + " Period: {period:^} \n Deadline: {deadline:^} \n"
                + " Response: {response:^}").format(
                        type=str('TSNTask'),
                        id=self.id, 
                        priority=self.priority, 
                        offset=self.offset,
                        hops=self.hops, slot=self.slot, period=self.period,
                        deadline=self.deadline, 
                        response=self.rt)
