"""Representation of TSN Tasks."""


class tsnTask:
    """A tsn task."""

    def __init__(self, tsntask_id, tsntask_offset, tsntask_hops, tsntask_slot, tsntask_period,
                 tsntask_deadline):
        """Creates a task represented by ID, Phase, BCET, WCET, Period and
        Deadline.
        """
        self.id = str(tsntask_id)
        self.offset = tsntask_offset  # 偏移量，o
        self.hops = tsntask_hops  #  跳数，h
        self.slot = tsntask_slot  # slot长度，d
        self.period_tsn = tsntask_period  # 间隔，p
        self.deadline = tsntask_deadline  # deadline
        # self.prio = prio  # a lower value means higher priority
        # self.message = tsnmessage  # flag for communication tasks

        self.rt_tsn = 0  # Worst-case response time, specified during analysis

    def __str__(self):
        """Print a task."""
        return (" Type: {type:^}\n ID: {id:^}\n"
                + " Offset: {offset:^} \n Hops: {hops:^} \n Slot: {slot:^} \n"
                + " Period: {period:^} \n Deadline: {deadline:^} \n"
                + " Response: {response:^}").format(
                        type=str('TSNTask'),
                        id=self.id, 
                        offset=self.offset,
                        hops=self.hops, slot=self.slot, period=self.period_tsn,
                        deadline=self.deadline, 
                        response=self.rt_tsn)
