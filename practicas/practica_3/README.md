# Práctica 3
## Multiprogramación


En esta versión, la __CPU__ no accede directamente a la __Memoria__, como hace la __CPU__ para fetchear la instruccion?? Por que??

Existe un componente de hardware llamado Memory Management Unit (__MMU__) que se encarga de transformar las direcciones lógicas (relativas)  en direcciones físicas (absolutas)



## Interrupciones de I/O y Devices

En esta version del emulador agregamos los I/O Devices y el manejo de los mismos

Un I/O device es un componente de hardware (interno o externo) que realiza operaciones específicas.

Una particularidad que tienen estos dispositivos es los tiempos de ejecucion son mas extensos que los de CPU, ej: bajar un archivo de internet, imprimir un archivo, leer desde un DVD, etc.
Por otro lado, solo pueden ejecutar una operacion a la vez, con lo cual nuestro S.O. debe garantizar que no se "choquen" los pedidos de ejecucion.

Para ello implementamos un __IoDeviceController__ que es el encargado de "manejar" el device, encolando los pedidos para ir sirviendolos a medida que el dispositivo se libere.


También se incluyeron 2 interrupciones 

- __#IO_IN__
- __#IO_OUT__



## Lo que tenemos que hacer es:

- __1:__ Describir como funciona el __MMU__ y que datos necesitamos para correr un proceso

- __2:__ Entender las clases __IoDeviceController__, __PrinterIODevice__ y poder explicar como funcionan

- __3:__ Explicar cómo se llegan a ejecutar __IoInInterruptionHandler.execute()__ y  __IoOutInterruptionHandler.execute()__

- __4:__    Hagamos un pequeño ejercicio (sin codificarlo):

- __4.1:__ Que esta haciendo el CPU mientras se ejecuta una operación de I/O??

- __4.2:__ Si la ejecucion de una operacion de I/O (en un device) tarda 3 "ticks", cuantos ticks necesitamos para ejecuar el siguiente batch?? Cómo podemos mejorarlo??
    (tener en cuenta que en el emulador consumimos 1 tick para mandar a ejecutar la operacion a I/O)

    ```python
    prg1 = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.IO(), ASM.CPU(2)])
    prg2 = Program("prg2.exe", [ASM.CPU(4), ASM.IO(), ASM.CPU(1)])
    prg3 = Program("prg3.exe", [ASM.CPU(3)])
    ```

- __5:__ Hay que tener en cuenta que los procesos se van a intentar ejecutar todos juntos ("concurrencia"), pero como solo tenemos un solo CPU, vamos a tener que administrar su uso de forma óptima.
      Como el S.O. es una "maquina de estados", donde las cosas "pasan" cada vez que se levanta una interrupcion (IRQ) vamos a tener que programar las 4 interrupciones que conocemos:  
    
    - Cuando se crea un proceso (__#NEW__) se debe intentar hacerlo correr en la CPU, pero si la CPU ya esta ocupada, debemos mantenerlo en la cola de Ready.
    - Cuando un proceso entre en I/O (__#IO_IN__), debemos cambiar el proceso corriendo en CPU (__"running"__) por otro, para optimizar el uso de __CPU__
    - Cuando un proceso sale en I/O (__#IO_OUT__), se debe intentar hacerlo correr en la CPU, pero si la CPU ya esta ocupada, debemos mantenerlo en la cola de Ready.
    - Cuando un proceso termina (__#KILL__), debemos cambiar el proceso corriendo en CPU (__"running"__) por otro, para optimizar el uso de __CPU__

.

- __6:__ Ahora si, a programar... tenemos que "evolucionar" nuestro S.O. para que soporte __multiprogramación__  

- __6.1:__ Implementar la interrupción #NEW
    ```python
    # Kernel.run() debe lanzar una interrupcion de #New para que se resuelva luego por el S.O. 
    ###################

    ## emulates a "system call" for programs execution
    def run(self, program):
        newIRQ = IRQ(NEW_INTERRUPTION_TYPE, program)
        HARDWARE.interruptVector.handle(newIRQ)
    ```

- __6.2:__ Implementar los compoenentes del S.O.: 
    - Loader
    - Dispatcher
    - PCB
    - PCB Table
    - Ready Queue
    - Las 4 interrupciones: 
        - __#NEW__ 
        - __#IO_IN__
        - __#IO_OUT__
        - __#KILL__



- __6.3:__        Implementar una version con __multiprogramación__ (donde todos los procesos se encuentran en memoria a la vez)


    ```python
    # Ahora vamos a intentar ejecutar 3 programas a la vez
    ###################
    prg1 = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.IO(), ASM.CPU(2)])
    prg2 = Program("prg2.exe", [ASM.CPU(4), ASM.IO(), ASM.CPU(1)])
    prg3 = Program("prg3.exe", [ASM.CPU(3)])

    # executamos los programas "concurrentemente"
    kernel.run(prg1)
    kernel.run(prg2)
    kernel.run(prg3)

    ## start
    HARDWARE.switchOn()

    ```
