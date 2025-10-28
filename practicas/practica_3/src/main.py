from hardware import *
from so import *
import log

##
##  MAIN 
##
if __name__ == '__main__':
    log.setupLogger()
    log.logger.info('Starting emulator')

    # set up our hardware with 50 memory cells
    HARDWARE.setup(50)

    ## turn on the computer
    HARDWARE.switchOn()

    ## new create the Operative System Kernel
    # initialize the operating system
    kernel = Kernel()

    ##  create a single program
    prg = Program("test.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.IO(), ASM.CPU(3)])
    
    # run the program (optional)
    # kernel.run(prg)

    ###################
    prg1 = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.IO(), ASM.CPU(2)])
    prg2 = Program("prg2.exe", [ASM.CPU(4), ASM.IO(), ASM.CPU(1)])
    prg3 = Program("prg3.exe", [ASM.CPU(3)])

    # execute programs "concurrently"
    kernel.run(prg1)
    kernel.run(prg2)
    kernel.run(prg3)