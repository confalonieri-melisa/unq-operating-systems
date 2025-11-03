from enum import Enum

class State(Enum):
    NEW = 1
    READY = 2
    RUNNING = 3
    WAITING = 4
    TERMINATED = 5


class PCB():

    def __init__(self, pid, baseDir, size, path, priority):
        self._pid = pid
        self._baseDir = baseDir
        self._size = size
        self._pc = 0
        self._state = State.NEW
        self._path = path
        self._priority = priority
        self._alt_priority = priority
        self._waitingTime = 0

    def update_state(self, state):
        self._state = state
    
    def update_pc(self, pc):
        self._pc = pc

    def update_baseDir(self, baseDir):
        self._baseDir = baseDir

    @property
    def pid(self):
        return self._pid

    @property
    def state(self):
        return self._state
    
    @property
    def pc(self):
        return self._pc
    
    @property
    def baseDir(self):
        return self._baseDir
    
    @property
    def path(self):
        return self._path

    @property
    def priority(self):
        return self._priority
    
    @property
    def alt_priority(self):
        return self._alt_priority
    
    @property
    def size(self):
        return self._size
    
    @alt_priority.setter
    def alt_priority(self, priority):
        self._alt_priority = priority

    @property
    def waitingTime(self):
        return self._waitingTime

    @waitingTime.setter
    def waitingTime(self, time):
        self._waitingTime = time


class PCBTable():

    def __init__(self):
        self._lastPID = 0
        self._pcbList = []

    def get(self, pid):
        matching_pcb = None
        for pcb in self._pcbList:
            if pcb.pid == pid:
                matching_pcb = pcb
        return matching_pcb
    
    def add(self, pcb):
        self._pcbList.append(pcb)

    def remove(self, pid):
        for pcb in self._pcbList:
            if pcb.pid == pid:
                self._pcbList.remove(pcb)

    def getNewPID(self):
        new_pid = self._lastPID
        new_pid += 1
        self._lastPID = new_pid
        return new_pid

    def all_terminated(self):
        return all(pcb.state == State.TERMINATED for pcb in self.pcbList)

    @property
    def pcbList(self):
        return self._pcbList
    
