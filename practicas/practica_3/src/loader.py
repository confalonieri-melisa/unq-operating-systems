from hardware import *

class Loader():

    def __init__(self):
        self._proxDir = 0

    def load(self, program):
        progSize = len(program.instructions)
        baseDir = self._proxDir

        for index in range(0, progSize):
            inst = program.instructions[index]
            HARDWARE.memory.write(self._proxDir, inst)
            self._proxDir += 1

        return baseDir