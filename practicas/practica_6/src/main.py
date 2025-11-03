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

    # set up our hardware with 32 memory cells
    HARDWARE.setup(32)

    # scheduler = FCFSScheduler()
    scheduler = PriorityNonPreemptiveScheduler()
    # scheduler = PriorityPreemptiveScheduler()
    # scheduler = RoundRobinScheduler()
    
    # boot the operating system
    kernel = Kernel(scheduler)

    ## turn on the computer
    HARDWARE.switchOn()

    # store programs in the FileSystem
    prg1 = Program([ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.IO(), ASM.CPU(2)])
    prg2 = Program([ASM.CPU(7)])
    prg3 = Program([ASM.CPU(4), ASM.IO(), ASM.CPU(1)])

    kernel.fileSystem.write("C:/prg1.exe", prg1)
    kernel.fileSystem.write("C:/prg2.exe", prg2)
    kernel.fileSystem.write("C:/prg3.exe", prg3)

    # run programs from their path with a given priority
    kernel.run("C:/prg1.exe", 0)
    kernel.run("C:/prg2.exe", 2)
    kernel.run("C:/prg3.exe", 1)