#!/usr/bin/env python

from src.hardware import *
from time import sleep
import src.log as log

## emulates a compiled program
class Program():

    def __init__(self, name, instructions):
        self._name = name
        self._instructions = self.expand(instructions)

    @property
    def name(self):
        return self._name

    @property
    def instructions(self):
        return self._instructions

    def addInstr(self, instruction):
        self._instructions.append(instruction)

    def expand(self, instructions):
        expanded = []
        for i in instructions:
            if isinstance(i, list):
                expanded.extend(i)
            else:
                expanded.append(i)
            
        # ensure the last instruction is EXIT
        last = expanded[-1]
        if not ASM.isEXIT(last):
            expanded.append(INSTRUCTION_EXIT)

        return expanded

    def __repr__(self):
        return "Program({name}, {instructions})".format(name=self._name, instructions=self._instructions)


## emulates the core of an Operative System
class Kernel():

    def __init__(self):
        pass

    def load_program(self, program):
        # loads the program into main memory  
        progSize = len(program.instructions)
        for index in range(0, progSize):
            inst = program.instructions[index]
            HARDWARE.memory.write(index, inst)

    # emulates a "system call" for programs execution  
    def run(self, program):
        self.load_program(program)
        log.logger.info("\n Executing program: {name}".format(name=program.name))
        log.logger.info(HARDWARE)

        # set CPU program counter at program's first intruction
        HARDWARE.cpu.pc = 0
        progSize = len(program.instructions)
        for i in range(0, progSize):
            HARDWARE.cpu.tick(i)
            sleep(1)

    def __repr__(self):
        return "Kernel "
    
    # execute a batch of programs
    def executeBatch(self, batch):
        for prg in batch:
            self.run(prg)