from hardware import *
from math import ceil

class Loader():

    def __init__(self, kernel):
        self._kernel = kernel

    def load(self, pcb):
        program = self._kernel.fileSystem.read(pcb.path)
        progSize = len(program.instructions)

        # calculate required frames based on program size
        totalPages = ceil(progSize / HARDWARE.mmu.frameSize)
        frames = self._kernel.memoryManager.allocFrames(totalPages)
        pages = self.paging(program.instructions)
        
        for i in range(totalPages):
            self.loadPageInFrame(pages[i], frames[i])

        pcb.setPageTable(frames)
        

    def paging(self, instructions):
        currentPage = []
        pages = []
        for inst in instructions:
            currentPage.append(inst)
            if len(currentPage) == HARDWARE.mmu.frameSize:
                pages.append(currentPage)
                currentPage = []
        
        # handle the last (incomplete) page
        if currentPage:
            pages.append(currentPage)
        return pages
    

    def loadPageInFrame(self, page, frame):
        baseDir = frame * HARDWARE.mmu.frameSize
        cantInst = len(page)
        for i in range(cantInst):
            inst = page[i]
            HARDWARE.memory.write(baseDir, inst)
            baseDir += 1

