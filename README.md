# Network Simulation

## Librerías necesarios
Python
Anytree
soil
scipy
numpy
pyenchant

## Esquema
El esquema de la simulación se separa en agentes de ambiente y agentes de la red.
En este caso particular, el esquema por defecto (en ```schema.py```) en que se basa nuestra simulación es el siguiente:
### Agente de ambiente
El agente de ambiente ga  
Este también modela el tiempo de conexión de un agente. El tiempo en que se conecta cada gente está modelado con una distribución normal, cuyos parámetros (en unidades de steps) se pueden modificar desde el archivo ```run_and_prompts.ipynb```. Un agente empieza a ser susceptible cuando se conecta a la red, y este se mantiene conectado hasta que el estado cambia a ```died```.

### Agentes de red
En el tiempo 0, ningún agente puede interactuar en la red. Esto se modela en el estado ```time_0```.
Posteriormente, un agente empieza a ser susceptible cuando el tiempo de la red es mayor que su tiempo de conexión. Esto se modela en el estado ```no_susceptible```
Los agentes de red son 3:
#### DumbViewer:


## Parámetros a configurar en las


## Ejecución :computer:

El módulo principal de la tarea a ejecutar es `````. Además se debe crear los siguientes archivos y directorios adicionales:

1.  ```name``` en ```directory```

2.  

  

## Librerías :books:

### Librerías externas utilizadas

La lista de librerías externas que utilicé fue la siguiente:

  

1.  ```name```: ```description ```
 

### Librerías propias

Por otro lado, los módulos que fueron creados fueron los siguientes:

  

1.  ```archivo.py```: Contiene a ```Clases```, ```funciones```


## Funcionamiento general




## Supuestos y consideraciones adicionales


## Referencias de código externo

  

Para realizar mi tarea saqué código de:

1. \<link>: Description.

