from hardware import *
from pcb import *

class Dispatcher():
    
    def load(self, pcb):
        HARDWARE.cpu.pc = pcb.pc
        HARDWARE.mmu.baseDir = pcb.baseDir
        HARDWARE.timer.reset()

    def save(self, pcb):
        pcb.update_pc(HARDWARE.cpu.pc)
        HARDWARE.cpu.pc = -1

