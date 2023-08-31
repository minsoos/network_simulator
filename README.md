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
El agente de ambiente es el que modela las probabilidades que coinciden para todos los agentes de red y el tiempo, o sea, el step en que se encuentra la simulación. Este también modela el tiempo de conexión de un agente. El tiempo en que se conecta cada gente está modelado con una distribución normal, cuyos parámetros, ```mean_time_connection``` y ```var_time_connection```, (en unidades de steps) se pueden modificar desde el archivo ```run_and_prompts.ipynb```. Un agente empieza a ser susceptible cuando se conecta a la red, y este se mantiene conectado hasta que el estado cambia a ```died```.

### Agentes de red
Los agentes de red modelan individuos autónomos de la red. Estos tienen estados, funciones que se ejecutan una vez por cada step de la simulación.

En el tiempo 0, ningún agente puede interactuar en la red. Esto se modela en el estado ```time_0```.

Posteriormente, un agente empieza a ser susceptible cuando el tiempo de la red es mayor que su tiempo de conexión. Esto se modela en el estado ```no_susceptible```.

En tercer lugar, el agente puede ser susceptible a contagiarse directamente por la noticia, en el caso que tenga activo su parámetro ```has_tv```, si es así, se contagia con probabilidad ```prob_tv_spread```. También puede empezar a ser contagiado por los nodos infectados con los que está conectado, o sea, sus vecinos en la red; en este caso se contagia con probabilidad ```prob_neighbor_spread```. Esto se modela en el estado ```neutral```

Ahora, cuando el agente ya fue contagiado, adquiere otro comportamiento. En este caso, el agente intenta contagiar a todos sus vecinos con probabilidad ```prob_neighbor_spread```. Por último, se recontagia con probabilidad ```prob_backsliding```. Por último, el nodo muere con probabilidad ```prob_died```.

En el caso de que un agente muera, este deja de participar en la red. Esto se modela en el estado ```died```

Los agentes de red son 3:
#### DumbViewer:
Adquiere el comportamiento base de un agente cualquiera
#### HerdViewer:
Adquiere el comportamiento de un agente Dumb, modificando:
- Pondera la probabilidad de infectarse por un vecino por la cantidad de vecinos infectados que tiene. La probabilidad de infectarse es menor que uno Dumb, pero es igual en el casoen que todos sus vecinos están contagiados.
#### WiseViewer:
Adquiere el comportamiento de un agente Herd, modificando:
- Puede curarse a sí mismo del estado infectado, lo que está modelado por la probabilidad  (Qué significa curarse?)```prob_neighbor_cure```*vecinos_curados/vecinos_infectados. Fuera de esto, el agente adopta el comportamiento de un agente Herd. ()
- Cuando está curado, l...

## Características de una interacción
Stance, response, 

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

