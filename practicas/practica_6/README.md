# Práctica 6
## Paginación

Ahora que tenemos un sistema multiprogramación con diferentes schedulers para elegir, necesitamos optimizar el uso de la __Memoria__.

Para esto vamos a tener que administrar la memoria física como vimos en la teoría. Debemos cargar los programas en una memoria paginada y liberar ese espacio una vez que terminen los programas


## Lo que tenemos que hacer es:


- __1:__ Vamos a usar nuevamente el código de la práctica anterior como base de la actual.... hacer copy/paste de la practica anterior y reemplazar solo el hardware

- __2:__ Implementar el componente __MemoryManager__ que será el encargado de administrar la __memoria lógica__ y los __frames__ libres. 

- __3:__ Implementar un __FileSystem__ básico.

- __4:__ Modificar el __Loader__ para cargar todas las paginas del programa en la memoria. 

- __5:__ El __Dispatcher__  debe cargar la page table del programa en ejecución en el  __MMU__  al momento del context switch.

- __6:__ Modificar el __#New__ Handler para cargar el programa desde un path. 

- __7:__ Modificar el __#Kill__ Handler para que se libere la memoria del programa, una vez que se termina su ejecución.

