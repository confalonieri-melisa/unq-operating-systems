#!/usr/bin/env python

from tabulate import tabulate
from time import sleep
from threading import Thread, Lock
import log

##  Estas son la instrucciones soportadas por nuestro CPU
INSTRUCTION_IO = 'IO'
INSTRUCTION_CPU = 'CPU'
INSTRUCTION_EXIT = 'EXIT'


## Helper for emulated machine code
class ASM():

    @classmethod
    def EXIT(self, times):
        return [INSTRUCTION_EXIT] * times

    @classmethod
    def IO(self):
        return INSTRUCTION_IO

    @classmethod
    def CPU(self, times):
        return [INSTRUCTION_CPU] * times

    @classmethod
    def isEXIT(self, instruction):
        return INSTRUCTION_EXIT == instruction

    @classmethod
    def isIO(self, instruction):
        return INSTRUCTION_IO == instruction


##  Estas son la interrupciones soportadas por nuestro Kernel
KILL_INTERRUPTION_TYPE = "#KILL"
IO_IN_INTERRUPTION_TYPE = "#IO_IN"
IO_OUT_INTERRUPTION_TYPE = "#IO_OUT"
NEW_INTERRUPTION_TYPE = "#NEW"

## emulates an Interrupt request
class IRQ:

    def __init__(self, type, parameters = None):
        self._type = type
        self._parameters = parameters

    @property
    def parameters(self):
        return self._parameters

    @property
    def type(self):
        return self._type


## emulates the Interrupt Vector Table
class InterruptVector():

    def __init__(self):
        self._handlers = dict()
        self.lock = Lock()

    def register(self, interruptionType, interruptionHandler):
        self._handlers[interruptionType] = interruptionHandler

    def handle(self, irq):
        log.logger.info("Handling {type} irq with parameters = {parameters}".format(type=irq.type, parameters=irq.parameters ))
        self.lock.acquire()
        self._handlers[irq.type].execute(irq)
        self.lock.release()



## emulates the Internal Clock
class Clock():

    def __init__(self):
        self._subscribers = []
        self._running = False

    def addSubscriber(self, subscriber):
        self._subscribers.append(subscriber)

    def stop(self):
        self._running = False

    def start(self):
        if not self._running:
            log.logger.info("---- :::: START CLOCK  ::: -----")
            self._running = True
            t = Thread(target=self.__start)
            t.start()

    def __start(self):
        tickNbr = 0
        while (self._running):
            self.tick(tickNbr)
            tickNbr += 1

    def tick(self, tickNbr):
        log.logger.info("        --------------- tick: {tickNbr} ---------------".format(tickNbr = tickNbr))
        ## notify all subscriber that a new clock cycle has started
        for subscriber in self._subscribers:
            subscriber.tick(tickNbr)
        ## wait 1 second and keep looping
        sleep(1)

    def do_ticks(self, times):
        log.logger.info("---- :::: CLOCK do_ticks: {times} ::: -----".format(times=times))
        for tickNbr in range(0, times):
            self.tick(tickNbr)



## emulates the main memory (RAM)
class Memory():

    def __init__(self, size):
        self._size = size
        self._cells = [''] * size

    def write(self, addr, value):
        self._cells[addr] = value

    def read(self, addr):
        return self._cells[addr]

    @property
    def size(self):
        return self._size

    def __repr__(self):
        return tabulate(enumerate(self._cells), tablefmt='psql')
        ##return "Memoria = {mem}".format(mem=self._cells)

## emulates the Memory Management Unit (MMU)
class MMU():

    def __init__(self, memory):
        self._memory = memory
        self._baseDir = 0
        self._limit = 999

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, limit):
        self._limit = limit

    @property
    def baseDir(self):
        return self._baseDir

    @baseDir.setter
    def baseDir(self, baseDir):
        self._baseDir = baseDir

    def fetch(self,  logicalAddress):
        if (logicalAddress > self._limit):
            raise Exception("Invalid Address,  {logicalAddress} is higher than process limit: {limit}".format(limit = self._limit, logicalAddress = logicalAddress))

        physicalAddress = logicalAddress + self._baseDir
        return self._memory.read(physicalAddress)


## emulates the main Central Processor Unit
class Cpu():

    def __init__(self, mmu, interruptVector):
        self._mmu = mmu
        self._interruptVector = interruptVector
        self._pc = -1
        self._ir = None


    def tick(self, tickNbr):
        if (self._pc > -1):
            self._fetch()
            self._decode()
            self._execute()
        else:
            log.logger.info("cpu - NOOP")


    def _fetch(self):
        self._ir = self._mmu.fetch(self._pc)
        self._pc += 1

    def _decode(self):
        ## decode no hace nada en este caso
        pass

    def _execute(self):
        if ASM.isEXIT(self._ir):
            killIRQ = IRQ(KILL_INTERRUPTION_TYPE)
            self._interruptVector.handle(killIRQ)
        elif ASM.isIO(self._ir):
            ioInIRQ = IRQ(IO_IN_INTERRUPTION_TYPE, self._ir)
            self._interruptVector.handle(ioInIRQ)
        else:
            log.logger.info("cpu - Exec: {instr}, PC={pc}, MMU={mmu}".format(instr=self._ir,
                                                                             pc=self._pc,
                                                                             mmu=HARDWARE.mmu.baseDir))
    @property
    def pc(self):
        return self._pc

    @pc.setter
    def pc(self, addr):
        self._pc = addr

    def __repr__(self):
        return "CPU(PC={pc})".format(pc=self._pc)


## emulates an Input/output device of the Hardware
class AbstractIODevice():

    def __init__(self, deviceId, deviceTime):
        self._deviceId = deviceId
        self._deviceTime = deviceTime
        self._busy = False

    @property
    def deviceId(self):
        return self._deviceId

    @property
    def is_busy(self):
        return self._busy

    @property
    def is_idle(self):
        return not self._busy


    ## executes an I/O instruction
    def execute(self, operation):
        if (self._busy):
            raise Exception("Device {id} is busy, can't  execute operation: {op}".format(id = self.deviceId, op = operation))
        else:
            self._busy = True
            self._ticksCount = 0
            self._operation = operation


    def tick(self, tickNbr):
        if (self._busy):
            self._ticksCount += 1
            if (self._ticksCount > self._deviceTime):
                ## operation execution has finished
                self._busy = False
                ioOutIRQ = IRQ(IO_OUT_INTERRUPTION_TYPE, self._deviceId)
                HARDWARE.interruptVector.handle(ioOutIRQ)
            else:
                log.logger.info("device {deviceId} - Busy: {ticksCount} of {deviceTime}".format(deviceId = self.deviceId, ticksCount = self._ticksCount, deviceTime = self._deviceTime))



class PrinterIODevice(AbstractIODevice):
    def __init__(self):
        super(PrinterIODevice, self).__init__("Printer", 3)


## emulates the Hardware that were the Operative System run
class Hardware():

    ## Setup our hardware
    def setup(self, memorySize):
        ## add the components to the "motherboard"
        self._memory = Memory(memorySize)
        self._interruptVector = InterruptVector()
        self._clock = Clock()
        self._ioDevice = PrinterIODevice()
        self._mmu = MMU(self._memory)
        self._cpu = Cpu(self._mmu, self._interruptVector)
        self._clock.addSubscriber(self._ioDevice)
        self._clock.addSubscriber(self._cpu)

    def switchOn(self):
        log.logger.info(" ---- SWITCH ON ---- ")
        return self.clock.start()

    def switchOff(self):
        self.clock.stop()
        log.logger.info(" ---- SWITCH OFF ---- ")

    @property
    def cpu(self):
        return self._cpu

    @property
    def clock(self):
        return self._clock

    @property
    def interruptVector(self):
        return self._interruptVector

    @property
    def memory(self):
        return self._memory

    @property
    def mmu(self):
        return self._mmu

    @property
    def ioDevice(self):
        return self._ioDevice


    def __repr__(self):
        return "HARDWARE state {cpu}\n{mem}".format(cpu=self._cpu, mem=self._memory)

### HARDWARE is a global variable
### can be access from any
HARDWARE = Hardware()

