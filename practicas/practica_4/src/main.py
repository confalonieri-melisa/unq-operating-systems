from hardware import *
from so import *
from scheduler import *
import log

##
##  MAIN 
##
if __name__ == '__main__':
    log.setupLogger()
    log.logger.info('Starting emulator')

    # set up our hardware with 25 memory cells
    HARDWARE.setup(25)

    ## turn on the computer
    HARDWARE.switchOn()

    # uncomment the scheduler you want to test
    scheduler = FCFSScheduler()
    #scheduler = PriorityNonPreemptiveScheduler()
    #scheduler = PriorityPreemptiveScheduler()
    #scheduler = RoundRobinScheduler()

    # boot the operating system
    kernel = Kernel(scheduler)

    prg1 = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.IO(), ASM.CPU(2)])
    prg2 = Program("prg2.exe", [ASM.CPU(7)])
    prg3 = Program("prg3.exe", [ASM.CPU(4), ASM.IO(), ASM.CPU(1)])

    # execute all programs
    kernel.run(prg1, 1)  ## 1 = process priority 
    kernel.run(prg2, 2)  ## 2 = process priority 
    kernel.run(prg3, 3)  ## 3 = process priority