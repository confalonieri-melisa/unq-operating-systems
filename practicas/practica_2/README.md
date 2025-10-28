# Práctica 2 
## Procesos - Clock - Interrupciones 

En la práctica 1 vimos como se puede "simular" un  __Sistema Operativo__ simplificado.

En esta versión del simulador, avanzamos con un __Hardware__ "un poco" mas realista. Ahora el hardware tiene un par de metodos para "prender" y "apagar" el __Hardware__.
Mientras el __Hardware__ esté encendido, el __Clock__ envía constantemente una señal a los distintos componentes para sincronizar los ciclos de ejecución. Este ciclo se repite indefinidamente hasta apagar el hardware ("loop infinito")

```python
## prende la "maquina"
HARDWARE.switchOn()

## apaga la "maquina"
HARDWARE.switchOff()
```

Hasta acá vimos que el Software se puede "comunicar" con el Hardware (ya que para eso fue creado). Ahora vamos a ver como hace el Hardware para "comunicarse" con el S.O.

El hardware contiene un vector de interrupciones __Interrupt Vector Table__, en el mismo se registran la direcciones de las rutinas (de software) a ser ejecutadas cuando una __Interrupción__ es solicitada.

  ej: 
```
  [#IRQ_1, 0001000] --> dir del interrupt hanlder de #IRQ_1
  [#IRQ_2, 0010111] --> dir del interrupt hanlder de #IRQ_2
  [#IRQ_3, 1111000] --> dir del interrupt hanlder de #IRQ_3
```

Los handlers de interrupciones son parte del S.O., El __S.O.__ es el encargado de completar el __Interrupt Vector Table__ para "escuchar" al __Hardware__. 

## Simulador 

Ahora, que nuestro __Clock__ va a estar enviando "ticks" constantemente a la __CPU__ (no vamos a poder controlar cuandos ciclos correr antes de terminar), debemos resolverlo a nivel del __Software__.

Cuando el __CPU__ detecta que el programa terminó (instrucción 'EXIT'), envia una solicitud de interrupción __IRQ__ ( o __Interruption Request__) de __#Kill__

```python
def _execute(self):
    if ASM.isEXIT(self._ir):
        killIRQ = IRQ(KILL_INTERRUPTION_TYPE, 123)
        self._interruptVector.handle(killIRQ)
    else:
        log.logger.info("cpu - Exec: {instr}, PC={pc}".format(instr=self._ir_str, pc=self._pc))
```


En nuestro S.O. tenemos que configurar el __Interrupt Vector Table__ para "handlear" la interrupcion de __#Kill__

```python
## setup interruption handlers
killHandler = KillInterruptionHandler(self)
HARDWARE.interruptVector.register(KILL_INTERRUPTION_TYPE, killHandler)
```

Cuando una iterrupcion es "lanzada", el __Interrupt Vector Table__ llama al "handler" configurado para que la "maneje", en este caso, se llamará al método __execute()__ de la clase __KillInterruptionHandler__:

```python
class KillInterruptionHandler(AbstractInterruptionHandler):
    def execute(self, irq):
        log.logger.info(" Program Finished ")
        HARDWARE.switchOff()
```

## Ahora que tenemos todo andando,  vamos a hacer 4 cosas:

1. Entender las clases __InterruptVector()__ y __Clock()__ y poder explicar como funcionan

2. Explicar cómo se llegan a ejecutar __KillInterruptionHandler.execute()__ 

3. Una pequeña modificación. Vamos a hacer que nuestro SO reciba una lista de programas y los ejecute uno después de otro en el orden recibido.

```python
# Ahora vamos a intentar ejecutar un lote (batch) de 3 programas
###################
prg1 = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3)])
prg2 = Program("prg2.exe", [ASM.CPU(4), ASM.IO(), ASM.CPU(1)])
prg3 = Program("prg3.exe", [ASM.CPU(3)])

batch = [prg1, prg2, prg3]
# execute the program
kernel.executeBatch(batch)
```

4. Hay que modificar el KillInterruptionHandler para que apague la maquina sólo cuando termine el ultimo proceso (solo podemos tocar el __Sistema Operativo__, sin modificar el __Hardware__)
