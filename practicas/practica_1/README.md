# Práctica 1 
## Introducción: Un Simulador "Extremadamente" Simplificado

Comenzamos por modelar un __programa__. Un programa tiene un nombre y una lista de instrucciones. Las instrucciones pueden ser `CPU`, `IO` o `EXIT` dependiendo si son instrucciones de cpu o entrada/salida o la última instrucción de un programa. Para comodidad queremos poder expresar algo como:

```python
p = Program("test.exe", [ASM.CPU(3), ASM.IO(), ASM.CPU(4)])
```

Qué sería un atajo para escribir:

```python
p = Program('test.exe', ['CPU', 'CPU', 'CPU', 'IO', 'CPU', 'CPU', 'CPU', 'CPU', 'EXIT'])
```

Para que todo esté listo vamos a hacer de compilador. Si creamos un programa cuya última instrucción no es `EXIT`, nosotros la agregaremos por el usuario.

Ahora que tenemos modelado nuestro programa vamos a modelar una __Cpu__ y una __Memoria__.

La __Memoria__ puede verse como un array de N celdas donde se cargan las instrucciones de los programas (comenzando en la posición 0). 

Lo único que sabe hacer una __Cpu__ es obtener una intrucción de la memoria (fetch) y ejecutarla (imprimir en pantalla por ahora). 


Finalemente modelemos un pequeño __Sistema Operativo__(SO) que nos permite ejecutar programas, lo primero que hará nuestro SO será cargar el programa en memoria y luego instruir a la __Cpu__ para que empiece a ejecutar. La __Cpu__ recibe una señal "tick" para indicarle que realice un ciclo de procesamiento (fetch/decode/execute).

Cuando no hay más instrucciones para ejecutar el SO devuelve el control al usuario.

## Código

- El Código del simulador es este: 

  - [log.py](./log.py) Se configura un logger, un logger es una herramienta para imprimir texto en pantalla o algun "output" del sistema, como por ejemplo un archivo de texto. 

  - [hardware.py](./hardware.py) Emula el Hardware en el que va a correr nuestro Sistema Operativo, Ahí está nuestro __CPU__, __Memoria__ y el pseudo lenguaje __ASM__. El hardware es accessible desde cualquier lugar del S.O. accediendo a la constante llamada __HARDWARE__  

  - [so.py](./so.py) Contiene la definicion de __Program__ y un pequeño __Kernel__ (el Kernel es la parte mas importante de un __Sistema Operativo__) 

  - [main.py](./main.py) inicia nuestro emulador de __Sistema Operativo__



Para correr el emulador, debemos ejecutar indicarle a Python (versón 3) que ejecute nuestro programa:

```bash
$ python main.py
```

o sino, dependiendo de nuestro sistema operativo:

```bash
$ python3 main.py
```

------------------

## Ahora que tenemos todo andando,  vamos a hacer 2 cosas:

1. Entender el código. Entender código de terceros siempre es más difícil que escribirlo, pero también se aprende mucho.

2. Una pequeña modificación. Vamos a hacer que nuestro SO reciba una lista de programas y los ejecute uno después de otro en el orden recibido.

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


