#!/usr/bin/env python
from hardware import *
from loader import *
from pcb import *
from dispatcher import *
from memoryManager import *
from fileSystem import *
import log


## emulates a compiled program
class Program():

    def __init__(self, instructions):
        #self._name = name
        self._instructions = self.expand(instructions)

    #@property
    #def name(self):
    #    return self._name

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


## emulates an Input/Output device controller (driver)
class IoDeviceController():

    def __init__(self, device):
        self._device = device
        self._waiting_queue = []
        self._currentPCB = None

    def runOperation(self, pcb, instruction):
        pair = {'pcb': pcb, 'instruction': instruction}
        # append: adds the element at the end of the queue
        self._waiting_queue.append(pair)
        # try to send the instruction to hardware's device (if is idle)
        self.__load_from_waiting_queue_if_apply()

    def getFinishedPCB(self):
        finishedPCB = self._currentPCB
        self._currentPCB = None
        self.__load_from_waiting_queue_if_apply()
        return finishedPCB

    def __load_from_waiting_queue_if_apply(self):
        if (len(self._waiting_queue) > 0) and self._device.is_idle:
            pair = self._waiting_queue.pop(0)
            pcb = pair['pcb']
            instruction = pair['instruction']
            self._currentPCB = pcb
            self._device.execute(instruction)

    def __repr__(self):
        return "IoDeviceController for {deviceID} running: {currentPCB} waiting: {waiting_queue}".format(
            deviceID=self._device.deviceId, currentPCB=self._currentPCB, waiting_queue=self._waiting_queue)


## emulates the  Interruptions Handlers
class AbstractInterruptionHandler():
    def __init__(self, kernel):
        self._kernel = kernel

    @property
    def kernel(self):
        return self._kernel

    def execute(self, irq):
        log.logger.error("-- EXECUTE MUST BE OVERRIDEN in class {classname}".format(classname=self.__class__.__name__))


class NewInterruptionHandler(AbstractInterruptionHandler):
    def execute(self, irq):
        parameters = irq.parameters
        path = parameters['path']
        priority = parameters['priority']
        pid = self.kernel.pcbTable.getNewPID()
        pcb = PCB(pid, path, priority)
        self.kernel._loader.load(pcb)

        log.logger.info("-- PCB {pid}: PAGE TABLE {pageTable}".format(pid=pcb.pid, pageTable=pcb.pageTable))
        self.kernel.pcbTable.add(pcb)

        self.kernel.go_ready_or_running(pcb)


class KillInterruptionHandler(AbstractInterruptionHandler):
    def execute(self, irq):
        finished_pcb = self.kernel.runningPCB
        self.kernel._dispatcher.save(finished_pcb)
        finished_pcb.update_state(State.TERMINATED)
        self.kernel.set_runningPCB(None)
        self.kernel.pcbTable.remove(finished_pcb.pid)

        log.logger.info("-- PROGRAM FINISHED {name}".format(name=finished_pcb.path))

        self.kernel.memoryManager.freeFrames(finished_pcb.pageTable)

        self.kernel.load_from_ready_queue_if_apply()


class IoInInterruptionHandler(AbstractInterruptionHandler):
    def execute(self, irq):
        operation = irq.parameters
        former_pcb = self.kernel.runningPCB
        former_pcb.update_state(State.WAITING)
        self.kernel._dispatcher.save(former_pcb)
        self.kernel.set_runningPCB(None)

        self.kernel.ioDeviceController.runOperation(former_pcb, operation)
        log.logger.info(self.kernel.ioDeviceController)

        self.kernel.load_from_ready_queue_if_apply()


class IoOutInterruptionHandler(AbstractInterruptionHandler):
    def execute(self, irq):
        finished_pcb = self.kernel.ioDeviceController.getFinishedPCB()
        self.kernel.go_ready_or_running(finished_pcb)
        log.logger.info(self.kernel.ioDeviceController)


class TimeoutInterruptionHandler(AbstractInterruptionHandler):
    def execute(self, irq):
        former_pcb = self.kernel.runningPCB
        self.kernel._dispatcher.save(former_pcb)
        self.kernel.set_runningPCB(None)
        self.kernel.go_ready_or_running(former_pcb)


class StatInterruptionHandler(AbstractInterruptionHandler):
    def execute(self, irq):
        for pcb in self.kernel.pcbTable.pcbList:
            self.get_pcb_data(pcb)
        if self.kernel.pcbTable.all_terminated():
            HARDWARE.switchOff()
            self.print_statistics()

    def get_pcb_data(self, pcb):
        stats = self.kernel._statistics
        currentTick = HARDWARE.clock.currentTick
        pid = pcb.pid
        if pid not in stats:
            stats[pid] = {'name': pcb.path, 'states': [(currentTick, pcb.state)]}
        else:
            stats[pid]['states'].append((currentTick, pcb.state))

    def print_statistics(self):
        statistics = self.kernel._statistics
        print("\n--- PCB Statistics ---\n")
        for pid, data in statistics.items():
            print(f"Process: {data['name']}")
            print("Tick | State")
            print("-------------")
            for tick, state in data['states']:
                print(f"{tick:4} | {state}")
            print()
        print("--- End of PCB Statistics ---\n")


class Crontab():

    def __init__(self, kernel):
            self._jobs = {} #diccionario
            self._kernel = kernel
            # nos subscribimos al Clock para recibir cada click
            HARDWARE.clock.addSubscriber(self)

    def add_job(self, tickNbr, program, prioridad):
        job = {'program': program, 'prioridad': prioridad}
        # en cada tick se pueden mandar a correr solo un job se decidio asi para evitar complejidad en el emulador
        self._jobs[tickNbr] = job
        log.logger.info("Crontab: add job {job} to Tick {tickNbr} ".format(job = job, tickNbr = tickNbr))

    def tick(self, tickNbr):
        job = self._jobs.get(tickNbr)
        # Si hay algo para correr en este tick lo mandamos a ejecutar
        if job != None:
            log.logger.info("Tick {tickNbr} - Running job: {job}".format(job = job, tickNbr = tickNbr))
            self.run_job(job)

    def run_job(self, job):
        program = job['program']
        prioridad = job['prioridad']
        self._kernel.run(program, prioridad)


# emulates the core of an Operative System
class Kernel():

    def __init__(self, scheduler):
        # setup frame size
        HARDWARE.mmu.frameSize = 4

        ## setup interruption handlers
        killHandler = KillInterruptionHandler(self)
        HARDWARE.interruptVector.register(KILL_INTERRUPTION_TYPE, killHandler)

        ioInHandler = IoInInterruptionHandler(self)
        HARDWARE.interruptVector.register(IO_IN_INTERRUPTION_TYPE, ioInHandler)

        ioOutHandler = IoOutInterruptionHandler(self)
        HARDWARE.interruptVector.register(IO_OUT_INTERRUPTION_TYPE, ioOutHandler)

        newHandler = NewInterruptionHandler(self)
        HARDWARE.interruptVector.register(NEW_INTERRUPTION_TYPE, newHandler)

        timeoutHandler = TimeoutInterruptionHandler(self)
        HARDWARE.interruptVector.register(TIMEOUT_INTERRUPTION_TYPE, timeoutHandler)

        statHandler = StatInterruptionHandler(self)
        HARDWARE.interruptVector.register(STAT_INTERRUPTION_TYPE, statHandler)

        ## controls the Hardware's I/O Device
        self._ioDeviceController = IoDeviceController(HARDWARE.ioDevice)

        self._loader = Loader(self)
        self._dispatcher = Dispatcher()
        self._pcbTable = PCBTable()
        self._runningPCB = None
        self._scheduler = scheduler
        self._crontab = Crontab(self)
        self._fileSystem = FileSystem()
        self._memoryManager = MemoryManager()

        if self._scheduler.isRoundRobin():
            HARDWARE.timer.quantum = 2

        self._statistics = {}
        # HARDWARE.cpu.enable_stats = True   <- trae problemas de concurrencia

    @property
    def ioDeviceController(self):
        return self._ioDeviceController

    @property
    def pcbTable(self):
        return self._pcbTable

    @property
    def runningPCB(self):
        return self._runningPCB

    @property
    def crontab(self):
        return self._crontab
    
    @property
    def fileSystem(self):
        return self._fileSystem

    @property
    def memoryManager(self):
        return self._memoryManager

    def set_runningPCB(self, pcb):
        self._runningPCB = pcb


    ## emulates a "system call" for programs execution
    def run(self, path, priority):
        parameters = {'path': path, 'priority': priority}
        newIRQ = IRQ(NEW_INTERRUPTION_TYPE, parameters)
        HARDWARE.interruptVector.handle(newIRQ)

    def __repr__(self):
        return "Kernel "


    ## manages the ready queue to ensure that there is always a process running on the CPU
    def go_ready_or_running(self, pcbToAdd):
        pcbInCPU = self.runningPCB
        if pcbInCPU is not None and self._scheduler.mustExpropiate(pcbInCPU, pcbToAdd):
            self._dispatcher.save(pcbInCPU)
            self._scheduler.add(pcbInCPU)
        pcbToAdd.update_state(State.READY)
        self._scheduler.add(pcbToAdd)
        self.load_from_ready_queue_if_apply()

    def load_from_ready_queue_if_apply(self):
        scheduler = self._scheduler
        if scheduler.hasElements() and HARDWARE.cpu.pc < 0:
            pcb = scheduler.getNext()
            pcb.update_state(State.RUNNING)
            self.set_runningPCB(pcb)
            self._dispatcher.load(pcb)