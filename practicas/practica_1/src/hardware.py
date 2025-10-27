#!/usr/bin/env python

from tabulate import tabulate
import src.log as log

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


## emulates the main Central Processor Unit
class Cpu():

    def __init__(self, memory):
        self._memory = memory
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
        self._ir = self._memory.read(self._pc)
        self._pc += 1

    def _decode(self):
        ## decode no hace nada en este caso
        pass

    def _execute(self):
        log.logger.info("cpu - Exec: {instr}, PC={pc}".format(instr=self._ir, pc=self._pc))

    @property
    def pc(self):
        return self._pc

    @pc.setter
    def pc(self, addr):
        self._pc = addr

    def __repr__(self):
        return "CPU(PC={pc})".format(pc=self._pc)


## emulates the Hardware that were the Operative System run
class Hardware():

    ## Setup our hardware
    def setup(self, memorySize):
        ## add the components to the "motherboard" 
        self._memory = Memory(memorySize)

        ## "wire" the components each others
        self._cpu = Cpu(self._memory)


    @property
    def cpu(self):
        return self._cpu

    @property
    def memory(self):
        return self._memory

    def __repr__(self):
        return "HARDWARE state {cpu}\n{mem}".format(cpu=self._cpu, mem=self._memory)


### HARDWARE is a global variable
### can be access from any 
HARDWARE = Hardware()