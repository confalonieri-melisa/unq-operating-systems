# Práctica Asignacion Continua

Basado en la practica 4
Usar el Scheduler Prioridad expropiativo


## Lo que tenemos que hacer es:


- __1:__ Crear un componente en el S.O. llamado Crontab


```python
class Crontab():

    def __init__(self, kernel):
        self._kernel = kernel
        # nos subscribimos al Clock para recibir cada click
        HARDWARE.clock.addSubscriber(self)
        ## Completar con lo que se necesite



    def add_job(self, tickNbr, program, prioridad):
        ## Completar



    def tick(self, tickNbr):
        ## Completar




########################################################
class Kernel():

    def __init__(self):
#...
        self._crontab = Crontab(self)

    @property
    def crontab(self):
        return self._crontab
#...
########################################################

```


- __2:__ Implementar el componente __Memory Manager__ que será el encargado de administrar memoria implementando Asignacion Continua.



- __3:__  NEW: pide memoria al Memory Manager (este retorna el baseDir)
```
    memoryManager.getFreeBlock(tamaño) --> baseDir
```

- __4:__  Kill: libera memoria 
```
    memoryManager.freeBlock(baseDir, tamaño) 
```


