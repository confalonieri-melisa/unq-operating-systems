import log
from hardware import *

class AbstractScheduler():
    def __init__(self):
        self._readyQueue = []
        self._agingLimit = 2
        self._useAging = False

    def add(self, pcbToAdd):
        log.logger.error("-- EXECUTE MUST BE OVERRIDEN in class {classname}".format(classname=self.__class__.__name__))

    def getNext(self):
        if self._useAging:
            self.applyAging()
            self.readyQueue.sort(key=lambda x: x.alt_priority)
        return self.readyQueue.pop(0)

    def mustExpropiate(self, pcbInCPU, pcbToAdd):
        log.logger.error("-- EXECUTE MUST BE OVERRIDEN in class {classname}".format(classname=self.__class__.__name__))

    def hasElements(self):
        return self.readyQueue.__len__() > 0

    def isRoundRobin(self):
        return False
    
    def enableAging(self):
        self._useAging = True
    
    def applyAging(self):
        for pcb in self.readyQueue:
            pcb.waitingTime += 1
            if pcb.waitingTime >= self._agingLimit:
                pcb.alt_priority = max(0, pcb.alt_priority - 1)
                log.logger.info("Aging process: {name} to priority: {alt_priority}".format(name=pcb.path, alt_priority=pcb.alt_priority))
                pcb.waitingTime = 0

    @property
    def readyQueue(self):
        return self._readyQueue


class FCFSScheduler(AbstractScheduler):
    def add(self, pcbToAdd):
        self.readyQueue.append(pcbToAdd)

    def mustExpropiate(self, pcbInCPU, pcbToAdd):
        return False


class PriorityNonPreemptiveScheduler(AbstractScheduler):
    def __init__(self):
        super().__init__()
        self.enableAging()

    def add(self, pcbToAdd):
        self.readyQueue.append(pcbToAdd)
        self.readyQueue.sort(key=lambda x: x.priority)

    def mustExpropiate(self, pcbInCPU, pcbToAdd):
        return False
    

class PriorityPreemptiveScheduler(AbstractScheduler):
    def __init__(self):
        super().__init__()
        self.enableAging()

    def add(self, pcbToAdd):
        self.readyQueue.append(pcbToAdd)
        self.readyQueue.sort(key=lambda x: x.priority)

    def mustExpropiate(self, pcbInCPU, pcbToAdd):
        return pcbInCPU.priority > pcbToAdd.alt_priority


class RoundRobinScheduler(AbstractScheduler):
    def add(self, pcbToAdd):
        self.readyQueue.append(pcbToAdd)

    def mustExpropiate(self, pcbInCPU, pcbToAdd):
        return False
    
    def isRoundRobin(self):
        return True
    
