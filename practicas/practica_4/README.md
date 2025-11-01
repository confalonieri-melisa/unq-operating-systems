# Práctica 4
## Scheduler

Ahora que tenemos un sistema multiprogramación, necesitamos optimizar el uso del __CPU__.

Para esto vamos a tener que implementar algunos de los algoritmos de planificación de CPU que vimos en la teoría.



## Lo que tenemos que hacer es:


- __1:__ A partir de ahora vamos a usar el codigo de la práctica anterior como base de la actual.... hacer copy/paste del so.py de la practica anterior

- __2:__ Implementar el componente __Scheduler__ que será el encargado de administrar la __ready queue__. 


- __3:__ Implementar al menos estas variantes de scheduling :
  - FCFS
  - Priority no expropiativo 
  - Priority expropiativo 
  - Round Robin

  Nuestro sistema operativo se ejecutará con un solo Scheduler a la vez, pero es requerido que podamos intercambiarlo "en Frio", es decir, bajar el S.O., configurar el Scheduler y volver a levantar todo desde cero con el nuevo algoritmo de planificación 



```python
    prg1 = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.IO(), ASM.CPU(2)])
    prg2 = Program("prg2.exe", [ASM.CPU(7)])
    prg3 = Program("prg3.exe", [ASM.CPU(4), ASM.IO(), ASM.CPU(1)])

    # execute all programs
    kernel.run(prg1, 1)  ## 1 = prioridad del proceso
    kernel.run(prg2, 2)  ## 2 = prioridad del proceso
    kernel.run(prg3, 3)  ## 3 = prioridad del proceso
```

- __4:__ implmentar Aging en los schedulers por Prioridad

- __5:__ __Deseable__: imprimir el Diagrama de Gantt de la ejecucion actual (suma puntos en la nota del TP)



Para implementar esto, pueden agregar un IRQ Handler para el tipo: STAT_INTERRUPTION_TYPE (#STAT)
-  Las estadisticas se habilitan seteando el flag enable_stats del CPU en true:
```python
    HARDWARE.cpu.enable_stats = True
```

- Para saber cual es el tick actual dentro del handler, podemos pedirselo al Clock del Hardware: 
```python
    HARDWARE.clock.currentTick
```



__Nota__ Cuando implementen Priority, debemos extender el modelo de ejecucion y #NewHandler para recibir la priordad como parametro del run

```
class Kernel():
    def run(self, program, priority):
        parameters = {'program': program, 'priority': priority}
        newIRQ = IRQ(NEW_INTERRUPTION_TYPE, parameters)



class NewInterruptionHandler(AbstractInterruptionHandler):
    def execute(self, irq):
	parameters = irq.parameters
	program = parameters['program']
	priority = parameters['priority']

```


