

class Task:
    """Class Task

        **Global Variables**
            :cvar id: Unique identifier.
            :type id: String
            :cvar phase: Indicates when the first job is released.
            :type phase: Integer
            :cvar wcet: Worst Case Execution Time.
            :type wcet: Integer
            :cvar bcet: Best Case Execution Time.
            :type bcet: Integer
            :cvar period: A job is released exactly and periodically by a period.
            :type period: Integer
            :cvar deadline: A relative deadline for each job of the task.
            :type deadline: Integer
            :cvar rt: Response time of the task.
            :type rt: Integer
            :cvar exec_progress: Current value of job execution.
            :type exec_progress: Integer
            :cvar execution: Number of the released jobs.
            :type execution: Integer

        **Usage**
            >>> import stt.task as task
            >>> myTask = task.Task("t1", 0, 1, 3, 10, 10)
    """
    id = None
    priority = None # a lower value means higher priority
    phase = None
    bcet = None
    wcet = None
    period = None
    deadline = None
    rt = 0
    exec_progress = 0
    execution = 0
    message = False
    blocking_time = 0
    jobs = []

    def __init__(self, task_id, task_phase, task_bcet, task_wcet, task_period, task_deadline, priority=0, message=False):
        """Creates a task represented by ID, Phase, BCET, WCET, Period and Deadline.

        :param task_id:
        :type task_id:
        :param task_phase:
        :type task_phase:
        :param task_bcet:
        :type task_bcet:
        :param task_wcet:
        :type task_wcet:
        :param task_period:
        :type task_period:
        :param task_deadline:
        :type task_deadline:
        """
        self.id = str(task_id)
        self.phase = task_phase
        self.bcet = task_bcet
        self.wcet = task_wcet
        self.period = task_period
        self.deadline = task_deadline
        self.priority = priority
        self.message = message

    def set_message(self):
        self.message = True

    def __str__(self):
        return " Type: {type:^} \n ID: {id:^} \n Phase: {phase:^} \n BCET: {bcet:^} \n WCET: {wcet:^} \n Period: {period:^} \n Deadline: {deadline:^} \n Response: {response:^}".format(type=str('Message') if self.message else str('Task'),
        id=self.id, phase = self.phase, bcet=self.bcet, wcet=self.wcet, period=self.period, deadline = self.deadline, response=self.rt)
