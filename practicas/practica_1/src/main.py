from src.hardware import *
from src.so import *
import src.log as log

##
##  MAIN 
##
if __name__ == '__main__':
    log.setupLogger()
    log.logger.info('Starting emulator')

    # setup hardware with memory size of 20 "cells"
    HARDWARE.setup(20)
    
    # create the Operative System Kernel
    kernel = Kernel()

    # create a single program
    prg = Program("test.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.IO(), ASM.CPU(3)])
    
    # execute the program
    kernel.run(prg)

    ##
    ##  execute a batch of 3 programs
    prg1 = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3)])
    prg2 = Program("prg2.exe", [ASM.CPU(4), ASM.IO(), ASM.CPU(1)])
    prg3 = Program("prg3.exe", [ASM.CPU(3)])

    batch = [prg1, prg2, prg3]
    
    # execute the batch
    kernel.executeBatch(batch)