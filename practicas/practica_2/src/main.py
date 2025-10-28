from hardware import *
from so import *
import log

##
##  MAIN 
##
if __name__ == '__main__':
    log.setupLogger()
    log.logger.info('Starting emulator')

    # set up our hardware with 20 memory cells
    HARDWARE.setup(20)

    ## switch on computer
    HARDWARE.switchOn()

    ## new create the Operative System Kernel
    # initialize the operating ststem
    kernel = Kernel()

    ##  create a single program
    prg = Program("test.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.IO(), ASM.CPU(3)])
    
    # execute the program
    kernel.run(prg)

    ###################

    # execute a batch of 3 programs
    prg1 = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3)])
    prg2 = Program("prg2.exe", [ASM.CPU(4), ASM.IO(), ASM.CPU(1)])
    prg3 = Program("prg3.exe", [ASM.CPU(3)])

    batch = [prg1, prg2, prg3]
    
    # execute the batch
    kernel.executeBatch(batch)
