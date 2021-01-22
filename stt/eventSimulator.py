"""Simulator to create the schedule."""
from __future__ import division  # TODO remove?
# import random
# import math
# import numpy as np
import operator


# for simulator initialization
class eventSimulator:
    """The event simulator."""
    statusTable = []
    eventList = []
    tasks = []
    n = 0  # number of tasks
    h = -1  # index of the active task with the highest workload

    def __init__(self, tasks):
        """Initialize the event simulator.

        We assume that the tasks are sorted by their priority (highest priority
        first).
        """
        self.statusTable = [[float(0.0) for x in range(5)] for y in range(n)]
        self.eventList = []
        # tasks = sorted(tasks, key=operator.attrgetter('priority'))
        # it is sorted already
        self.tasks = tasks
        self.h = -1
        self.n = len(tasks)
        # This is for sporadic
        # self.systemTick = float(0)

        # This is for periodic with specific phases
        tmp = range(len(self.tasks))
        tmp = tmp[::-1]
        tmpMin = self.tasks[0].phase
        tmpMinIdx = 0
        for idx in tmp:
            if tmpMin > self.tasks[idx].phase:
                tmpMin = self.tasks[idx].phase
                tmpMinIdx = idx
        self.firstPhase = tmpMin
        self.systemTick = float(0)
        # print("system tick:"+str(self.systemTick))
        self.firstIdx = tmpMinIdx

        # Now the first task is decided with the lowest phase among all the tasks.

        # this is used for e2e anaylsis
        self.raw_result = dict()

        self.initState()

    class eventClass(object):
        # This is the class of events
        def __init__(self, case, delta, idx):
            self.eventType = case
            self.delta = delta
            self.idx = idx

        def case(self):
            if self.eventType == 0:
                return "release"
            elif self.eventType == 1:
                return "deadline"

        def updateDelta(self, elapsedTime):
            self.delta = self.delta - elapsedTime

    """
    The status table for the simulator with 5 rows per column:
    0. workload of task
    1. # of release
    2. # of misses
    3. # of deadlines = this should be less than release
    4. flag for init the first execution of job
    """

    def tableReport(self):
        for i, e in enumerate(self.eventList):
            print("Event " + str(i) + " from task " + str(e.idx))
            print(e.case())
            print(e.delta)

        print
        for x in range(self.n):
            print("task" + str(x) + ": ")
            for y in range(5):
                print(self.statusTable[x][y])
        print

    def findTheHighestWithWorkload(self):
        # Assume that the fixed priority is given in the task set.
        # if there is no workload in the table, returns -1
        hidx = -1
        for i in range(self.n):
            if self.statusTable[i][0] != 0:
                hidx = i
                break
            else:
                pass

        return hidx

    def release(self, idx):
        # create deadline event to the event list
        # print ("Add deadline event for "+str(idx))
        # print (idx)
        # print (self.tasks[idx].deadline)
        self.eventList.append(self.eventClass(1, self.tasks[idx].deadline, idx))
        # create release event to the event list
        # print ("Add release event for "+str(idx))
        # sporadic randomness
        # spor=self.tasks[idx]['period']+self.tasks[idx]['period']*random.randint(0,20)/100
        # self.eventList.append(eventClass(0, spor, idx))
        # periodic setup
        self.eventList.append(self.eventClass(0, self.tasks[idx].period, idx))
        # sort the eventList
        self.eventList = sorted(self.eventList, key=operator.attrgetter('delta'))

        # add the workload to the table corresponding entry
        self.statusTable[idx][0] += float(self.tasks[idx].wcet)
        # print ("workload of task:"+str(idx)+" is "+str(self.statusTable[idx][0]))
        # print (self.tasks[idx].wcet)
        # print (self.statusTable[ idx ][ 0 ])
        # init the flag to indicate the first execution
        self.statusTable[idx][4] = 1

        # decide the highest priority task in the system
        self.h = self.findTheHighestWithWorkload()
        if self.h == -1:
            print("BUG: after release, there must be at least one task with workload.")
        self.statusTable[idx][1] += 1
        # print "Table in task"+str(idx)+" release event with h"+str(self.h)
        # self.tableReport()

    def deadline(self, idx):
        # check if the targeted task in the table has workload.
        # print "Table in task"+str(idx)+" deadline event with h"+str(self.h)
        # self.tableReport()
        if self.workload(idx) != 0:
            print("task" + str(idx) + " misses deadline")
            self.statusTable[idx][2] += 1
        self.statusTable[idx][3] += 1
        # print

        ##If there is no backlog in the lowest priority task,
        ##init the simulator again to force the worst release pattern.
        ##TODO this should be done in the release of higher priority task
        # if idx == len(self.tasks)-1 and self.workload( idx ) == 0:
        #    #print "Relase the worst pattern"
        #    self.eventList = []

        #    self.initState()

    def event_to_dispatch(self, event):
        # take out the delta from the event
        self.elapsedTime(event)

        # execute the corresponding event functions
        switcher = {
            0: self.release,
            1: self.deadline,
        }
        func = switcher.get(event.eventType, lambda: "ERROR")
        # execute the event
        func(event.idx)

    def elapsedTime(self, event):
        delta = event.delta

        # update the deltas of remaining events in the event list.
        # if len(self.eventList) == 0:
        # print ("BUG: there is no event in the list to be updated.")
        for e in self.eventList:
            e.updateDelta(delta)
        # update the workloads in the table
        while (delta):
            self.h = self.findTheHighestWithWorkload()
            if self.h == -1:
                # processor Idle
                # print ("delta "+str(delta))
                self.systemTick += delta
                delta = 0
            elif delta >= self.statusTable[self.h][0]:
                # this is the first time execution of task hidx
                if (self.h > -1 and self.statusTable[self.h][4] == 1):
                    # print ("First Time to run task:"+str(self.h)+" Tick now is:"+str(self.systemTick))
                    self.raw_result[self.tasks[self.h]].append(self.systemTick)
                    self.statusTable[self.h][4] = 0

                # print ("remaining work:"+str(self.statusTable[self.h][0]))
                delta = delta - self.statusTable[self.h][0]
                self.systemTick += self.statusTable[self.h][0]
                self.statusTable[self.h][0] = 0
                # the moment that a job is finished, since the workload is 0 now.
                self.raw_result[self.tasks[self.h]].append( self.systemTick )
                #print ("Finish Time of task:"+str(self.h)+" Tick now is:"+str(self.systemTick))
            elif delta < self.statusTable[self.h][0]:
                # this is the first time execution of task hidx
                if (self.h > -1 and self.statusTable[self.h][4] == 1):
                    # print ("First Time to run task:"+str(self.h)+" Tick now is:"+str(self.systemTick))
                    self.raw_result[self.tasks[self.h]].append(self.systemTick)
                    self.statusTable[self.h][4] = 0

                self.statusTable[self.h][0] -= delta
                self.systemTick += delta
                delta = 0

    def getNextEvent(self):
        # get the next event from the event list
        event = self.eventList.pop(0)
        # print "Get Event: "+event.case() + " from " + str(event.idx)
        return event

    def e2e_result(self):
        # this is for e2e analysis
        # The results is pre-handled to represent in [start, end] format (result[task] is a list of tuples describing the start and end of each job)
        result = dict()
        for task in self.tasks:
            result[task] = []
            # print (self.raw_result[task])
        for task in self.tasks:
            # print (str(idx), str(task))
            # traverse the raw_result
            job_start = -1
            job_end = -1
            # print ("number of timepoints: "+str(len(self.raw_result[task])))
            for x in self.raw_result[task]:
                if (job_start < 0):
                    job_start = x
                else:
                    job_end = x
                if job_start > -1 and job_end > -1:
                    result[task].append((job_start, job_end))
                    job_start = -1
                    job_end = -1
            # print (result[task])
        self.raw_result = dict()
        return result

    def missRate(self, idx):
        # return the miss rate of task idx
        return self.statusTable[idx][2] / self.statusTable[idx][1]

    def totalMissRate(self):
        # return the total miss rate of the system
        sumRelease = 0
        sumMisses = 0
        for idx in range(self.n):
            sumRelease += self.statusTable[idx][1]
            sumMisses += self.statusTable[idx][2]
        return sumMisses / sumRelease

    def releasedJobs(self, idx):
        # return the number of released jobs of idx task in the table
        # print "Released jobs of " + str(idx) + " is " + str(statusTable[ idx ][ 1 ])
        return self.statusTable[idx][1]

    def numDeadlines(self, idx):
        # return the number of past deadlines of idx task in the table
        # print "Deadlines of " + str(idx) + " is " + str(statusTable[ idx ][ 1 ])
        return self.statusTable[idx][3]

    def releasedMisses(self, idx):
        # return the number of misses of idx task in the table
        return self.statusTable[idx][2]

    def workload(self, idx):
        # return the remaining workload of idx task in the table
        return self.statusTable[idx][0]

    def initState(self):
        # init
        for task in self.tasks:
            self.raw_result[task] = []

        # print self.tasks
        self.eventList = []

        # task release together at 0 without delta / release from the lowest priority task
        tmp = range(len(self.tasks))
        tmp = tmp[::-1]
        for idx in tmp:
            self.statusTable[idx][0] = 0
            self.statusTable[idx][3] = self.statusTable[idx][1]
            # The first job injector for the tasks
            self.eventList.append(self.eventClass(0, self.tasks[idx].phase, idx))
        self.eventList = sorted(self.eventList, key=operator.attrgetter('delta'))
        #print(len(self.eventList))

        # self.tableReport()
        # print

    def dispatcher(self, targetedNumber):
        # Stop when the number of released jobs in the lowest priority task is equal to the targeted number.

        while (targetedNumber != self.numDeadlines(self.n - 1)):
            if len(self.eventList) == 0:
                print("BUG: there is no event in the2e_resulte dispatcher")
                break
            else:
                e = self.getNextEvent()
                # print(e.case())
                self.event_to_dispatch(e)
            # print(self.systemTick)
            # print ("Number of events in the queue")
            # print (len(self.eventList))
        # print "Stop at task "+str(e.idx)
        # self.tableReport()
