
class FileSystem():
    
    def __init__(self):
        self._store = {}

    def write(self, path, program):
        self._store[path] = program

    def read(self, path):
        return self._store[path]