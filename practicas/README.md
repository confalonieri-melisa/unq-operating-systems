# 🖥️ OS Emulator 
*This Python-based OS emulator implements process scheduling, multiprogramming, memory management (contiguous allocation and paging), I/O devices, and a basic file system. Developed as part of academic projects for the Operating Systems course at UNQ.*

*Below is a detailed description in Spanish.*

## 📚 Descripción del proyecto
Este repositorio contiene los trabajos prácticos realizados en forma grupal para la materia **Sistemas Operativos** de la Universidad Nacional de Quilmes (UNQ). A través de estas prácticas, se simularon e implementaron conceptos clave de un sistema operativo real, incluyendo:

- Gestión de **procesos** y su ciclo de vida.
- **Planificación de CPU** con diferentes algoritmos (FCFS, Prioridad, Round Robin)
- **Multiprogramación** y manejo de colas de procesos.
- **Gestión de memoria**, tanto con asignación contigua como con paginación.

El proyecto está desarrollado en **Python** y utiliza un emulador que reproduce el comportamiento de distintos componentes de hardware, permitiendo experimentar de forma práctica con la ejecución de programas y el manejo de recursos del sistema.

## 📝 Trabajos prácticos
Cada práctica fue construida sobre la anterior, incorporando gradualmente nuevos conceptos:
- **Práctica 1:** Simulación de un sistema operativo y ejecución secuencial.
- **Práctica 2:** Procesos, clock e interrupciones.
- **Práctica 3:** Multiprogramación, I/O devices.
- **Práctica 4:** Schedulers.
- **Práctica 5:** Asignación contigua de memoria.
- **Práctica 6:** Paginación. 

## 🛠️ Tecnologías
- Python 3.x

## 🚀 Cómo ejecutar
1. Clonar el repositorio:
```bash
git clone https://github.com/confalonieri-melisa/os-emulator-python
```
2. Entrar al directorio de la práctica deseada:
```bash
cd practica_4 # ejemplo: scheduler
```
3. Ejecutar el main:
```bash
python main.py
```
*(Opcional: comentar/descomentar el Scheduler que se quiera probar en main.py)*