from hardware import *

class MemoryManager():

    def __init__(self):
        self._memoryAvailable = HARDWARE.memory.size
        self._framesAvailable = []
        self.generateFrames()


    def generateFrames(self):
        totalFrames = HARDWARE.memory.size // HARDWARE.mmu.frameSize
        for i in range(totalFrames):
            self._framesAvailable.append(i)


    def allocFrames(self, framesRequired):
        if framesRequired > len(self._framesAvailable):
            log.logger.error("No hay suficientes frames libres.")
        else:
            allocatedFrames = []
            for i in range(framesRequired):
                allocatedFrames.append(self._framesAvailable.pop(0))
            self._memoryAvailable -= framesRequired * HARDWARE.mmu.frameSize
            return allocatedFrames


    def freeFrames(self, frames):
        for frame in frames:
            self._framesAvailable.append(frame)
        self._memoryAvailable += len(frames) * HARDWARE.mmu.frameSize
