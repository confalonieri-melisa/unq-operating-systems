from hardware import *

class Loader():
    def __init__(self, kernel):
        self._memoryManager = MemoryManager(kernel)

    def load(self, program):
        progSize = len(program.instructions)
        block = self.memoryManager.getFreeBlock(progSize)
        baseDir = block['baseDirOfBlock']
        sizeBlock = block['sizeOfBlock']
        proxDir = baseDir

        for i in range(sizeBlock):
            inst = program.instructions[i]
            HARDWARE.memory.write(proxDir + i, inst)

        return baseDir
    
    @property
    def memoryManager(self):
        return self._memoryManager



class MemoryManager():
    def __init__(self, kernel):
        self._memoryAvailable = HARDWARE.memory.size
        self._blocksAvailable = [{'baseDirOfBlock': 0, 'sizeOfBlock': self.memoryAvailable}]
        self._kernel = kernel 

    @property
    def memoryAvailable(self):
        return self._memoryAvailable

    @property
    def blocksAvailable(self):
        return self._blocksAvailable
    
    def set_memoryAvailable(self, size):
        self._memoryAvailable = size


    def hasEnoughMemory(self, sizeRequired):
        return sizeRequired <= self.memoryAvailable


    def hasFreeBlock(self, sizeRequired):
        return any(block['sizeOfBlock'] >= sizeRequired for block in self.blocksAvailable)


    def getFreeBlock(self, sizeRequired):
        if self.hasEnoughMemory(sizeRequired):
            self.compactIfNeeded(sizeRequired)
            blockRequired = self.getFirstSatisfy(sizeRequired)
            return blockRequired

    
    def compactIfNeeded(self, sizeRequired):
        if not self.hasFreeBlock(sizeRequired):
            self.compactMemory()


    def getFirstSatisfy(self, sizeRequired):
        blocks = self.blocksAvailable
        for block in blocks:
            if block['sizeOfBlock'] >= sizeRequired:
                baseDir = block['baseDirOfBlock']
                blockRequested = {'baseDirOfBlock': baseDir, 'sizeOfBlock': sizeRequired}
                self.updateFreeBlocks(block, sizeRequired)
                return blockRequested


    def updateFreeBlocks(self, block, sizeRequired):
        self.set_memoryAvailable(self.memoryAvailable - sizeRequired)
        if block['sizeOfBlock'] == sizeRequired:
            self.blocksAvailable.remove(block)
        else:
        # update remaining free space in the block
            block['baseDirOfBlock'] += sizeRequired
            block['sizeOfBlock'] -= sizeRequired
        
        log.logger.info("-- BLOQUES DISPONIBLES {blocks}".format(blocks=self.blocksAvailable))
        log.logger.info("-- Memoria disponible: {memory}".format(memory=self.memoryAvailable))


    def freeBlock(self, baseDir, sizeReleased):
        self.set_memoryAvailable(self.memoryAvailable + sizeReleased)
        blocks = self.blocksAvailable
        newBlock = {'baseDirOfBlock': baseDir, 'sizeOfBlock': sizeReleased}
        blocks.append(newBlock)
        blocks.sort(key=lambda x: x['baseDirOfBlock'])
        self.mergeFreeBlocks()

        log.logger.info("-- BLOQUES DISPONIBLES {blocks}".format(blocks=self.blocksAvailable))
        log.logger.info("-- Memoria disponible: {memory}".format(memory=self.memoryAvailable))
        

    def mergeFreeBlocks(self):
        blocks = self.blocksAvailable
        merged_blocks = []
        current_block = blocks[0]
        for block in blocks[1:]:
            # merge contiguous free blocks
            if current_block['baseDirOfBlock'] + current_block['sizeOfBlock'] == block['baseDirOfBlock']:
                current_block['sizeOfBlock'] += block['sizeOfBlock']
            else:      
                merged_blocks.append(current_block)
                current_block = block
        
        merged_blocks.append(current_block)
        self._blocksAvailable = merged_blocks
    

    def compactMemory(self):
        pcbTable = sorted(self._kernel.pcbTable.pcbList, key=lambda pcb: pcb.baseDir)
        currentDir = 0
        # save the state of the running process before compaction
        running_pcb = self._kernel.runningPCB
        self._kernel._dispatcher.save(running_pcb)

        log.logger.info("Compactando memoria...")
        for pcb in pcbTable:
            if pcb.baseDir != currentDir:
                self.overwriteMemory(pcb, currentDir)
                # update the baseDir with the new memory location
                pcb.update_baseDir(currentDir)
            currentDir += pcb.size
        # treat the remaining memory as a single free block
        self._blocksAvailable = [{'baseDirOfBlock': currentDir, 'sizeOfBlock': HARDWARE.memory.size - currentDir}]
        log.logger.info("Finalizó la compactación")        

        # resume the execution of the process that was running
        self._kernel._dispatcher.load(running_pcb)


    def overwriteMemory(self, pcb, new_dir):
        for i in range(pcb.size):
            inst = HARDWARE.memory.read(pcb.baseDir + i)
            HARDWARE.memory.write(new_dir + i, inst)