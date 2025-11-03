from hardware import *
from pcb import *

class Dispatcher():
    
    def load(self, pcb):
        HARDWARE.timer.reset()
        HARDWARE.mmu.resetTLB()
        HARDWARE.cpu.pc = pcb.pc

        # load the process page table into the MMU's TLB
        pageTableSize = len(pcb.pageTable)
        for i in range(pageTableSize):
            HARDWARE.mmu.setPageFrame(i, pcb.pageTable[i])
                

    def save(self, pcb):
        pcb.update_pc(HARDWARE.cpu.pc)
        HARDWARE.cpu.pc = -1

