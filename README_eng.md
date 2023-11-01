# Network Simulation

## Schema
The following simulation schema is splitted into environment agents and network agents.
In this particular case, the schema by default (in ```schema.py```) in which the simulation is based, is as follows (based on soil schema example):
### Environment agents
The environment agent models the probabilities, that coincide for every agents in the network and time. The time is referred to which step the simulation is. Environment agent also model agent's time conection. The time in what each agent entry to the network is modeled by a normal distribution, whose parameters, ```mean_time_connection``` and ```var_time_connection``` (in discrete units), can be modified from the following file: ```run_and_prompts.ipynb```. An agent begin to be susceptible when it is connected to the network, and this it stays connected until the state changes to ```died```

### Agentes de red social
Los agentes de red social modelan individuos autónomos de la red social. Estos tienen estados, funciones que se ejecutan una vez por cada step de la simulación.

En el tiempo 0, ningún agente puede interactuar en la red social. Esto se modela en el estado ```time_0```.

Posteriormente, un agente empieza a ser susceptible cuando el tiempo de la red social es mayor que su tiempo de conexión. Esto se modela en el estado ```no_susceptible```.

En tercer lugar, el agente puede ser susceptible a contagiarse directamente por la noticia, en el caso que tenga activo su parámetro ```has_tv```, si es así, se contagia con probabilidad ```prob_tv_spread```. También puede empezar a ser contagiado por los nodos infectados con los que está conectado, o sea, sus vecinos en la red social; en este caso se contagia con probabilidad ```prob_neighbor_spread```. Esto se modela en el estado ```neutral```.

Ahora, cuando el agente ya fue contagiado, adquiere otro comportamiento. En este caso, el agente intenta contagiar a todos sus vecinos con probabilidad ```prob_neighbor_spread```. Por último, se recontagia con probabilidad ```prob_backsliding```. Por último, el nodo muere con probabilidad ```prob_died```. Es importante notar que el agente siempre 'contagia' con su último mensaje.

En el caso de que un agente muera, este deja de participar en la red social. Esto se modela en el estado ```died```.

Los agentes de red social son 3:
#### DumbViewer:
Adquiere el comportamiento base de un agente cualquiera.
#### HerdViewer:
Adquiere el comportamiento de un agente Dumb, modificando:
1. Pondera la probabilidad de infectarse por un vecino por la cantidad de vecinos infectados que tiene. La probabilidad de infectarse es menor que uno Dumb, pero es igual en el caso en que todos sus vecinos están contagiados.
#### WiseViewer:
Adquiere el comportamiento de un agente Herd, modificando:
1. Añade la posibilidad de curarse, que significa cambiar a la opinión opuesta (response y stance). También puede intentar a curar a otros con probabilidad ```prob_neighbor_cure``` que sean de tipo wise y que tengan una stance distinta a él (no neutral). Esto se modela en el estado ```cured```.
2. Puede curarse a sí mismo del estado infectado, lo que está modelado por la probabilidad ```prob_neighbor_cure```*```vecinos_curados```/```vecinos_infectados```. Fuera de esto, el agente adopta el comportamiento de un agente Herd. Esto se modela en el estado ```infected```.
## Generación de conexiones de la red social
La red de conexiones entre usuarios está generada por un método llamado Barabassi-Albert, que recibe los parámetros ````n```` y ````m````.
1. ````n```` es la cantidad de agentes de red social que tendrá el grafo social.
2. ```m``` es la cantidad de aristas que se intentaran conectar por cada agente, usando como pesos de la probabilidad de conexión los grados de los otros nodos. (Para más información revisar método de Barabassi-Albert).

## Características de una interacción
1. ```id_message```: Es el id único de la interacción.
2. ```state```: Indica el estado actual en el que se produjo la interacción.
3. ```stance```: Indica si el agente está a favor (```agree```) o en contra (```against```) de la noticia. Puede cambiar dentro de la simulación, pero cada agente tiene la configuración que se entrega como input, y que está dada por la simulación del grafo social. En la literatura, este se conoce como 'polarización afectiva.'
4. ```response```: Indica el tipo de comentario que hace el agente. Puede ser ```support```, ```deny```, ```question``` o ```comment```. Las probabilidades dependen de los pesos que se entregan como input, pero dados ciertos stance, puede bloquearse la probabilidad de alguna. En la literatura el response es lo que se conoce como 'stance de veracidad'.
5. ```repost```: Indica si un post es una mención del anterior o es un post 'original'. La probabilidad de repost se entrega en el input. Puede ser 0 o 1. Además no rige para la interacción de backsliding
6. ```method```: Indica el método por el cual se produjo el contagio. Puede ser ```backsliding``` (si recayó en el contagio), ```tv``` (si fue por el nodo raíz) o ```friend``` (si se contagió por un vecino).
7. ```cause```: Indica el causante de un contagio, en el caso en que sea un vecino, puede ser cualquier id dentro de los id's de agentes de red social.
8. ```parent_id```: Indica el id de la interacción de la cual se desprende la interacción.

## Restricciones de interacciones
1. Si el method de una interacción es ```backsliding``` el agente mantendrá su stance y response.
2. Si una interacción es ```repost```, el response será ````support```` y el stance ````agree````.
3. Si el stance es ````against````, la probabilidad de response de ```support``` será 0.
4. Si el stance es ````agree````, la probabilidad de response de ```question``` y ```deny``` serán 0.
5. Si el stance es ````neutral````, la probabilidad de response de ```support``` y ```deny``` serán 0.

## Parámetros a configurar en la simulación
1. Parámetros por defecto de los agentes: Estos son los parámetros que tendrán todos los agentes, a menos que en alguno especifiques un cambio.
2. Configuración de los agentes: Acá se configura cada una de las clases de agentes que se crearán. Cada una tiene pesos, ```weight```, que indican qué tan probable es que aparezcan en la red social respecto al resto. Además, se pueden configurar los parámetros por defecto que se deseen para esa clase de agente en particular. Por último, se debe agregar el tipo adecuado correctamente en ```type```.
3. Configuración del agente de ambiente: Acá se debe configurar cada una de las probabilidades de contagio, los parámetros de la normal de la normal de conexión, los intervalos de tiempo y tanto los parámetros del generados de red social como el método mismo. Nota: Por defecto el simulador siempre hace un step menos que el que se configura
4. Probabilidad de responses: Se debe agregar en un diccionario los pesos de cada response para cada tipo de agente (Notar que no deben sumar 1, son solo pesos).


## Ejecución Simulación :computer:

Se deben ejecutar las celdas del archivo ```run_and_prompts.ipynb```. Las celdas ya están listas, pero lo que se hace básicamente es: 
1. Crear el archivo ```.yml``` que indica los parámetros de la simulación.
2. Ejecutar el comando de soil en la consola, que ejecutará la simulación.

## Crear conversación
1. Se obtienen los datos del output entregado por Soil.
2. Se pivotean los datos, para leerlos de manera más fácil.
3. Se define el título y cuerpo de la noticia.
4. Se crea una instancia de Post, que será el nodo raíz del árbol de interacciones.
5. Se definen los tiempos de inicio y final de la simulación.
6. Se usan los datos de cada una de las interacciones para crear instancias de Post para añadirlas al árbol de interacciones.

## Conexión con modelo LLM
1. Se obtiene el prompt de cada interacción, dándole como parámetro el idioma, la cantidad mínima y máxima de caracteres y la descripción del usuario.
2. Se define un endpoint para enviar el prompt y obtener una respuesta, lo que será el texto correspondiente a la interacción, en otras palabras, lo que el agente de red 'publica' en la red social.
   1. Inglés: Se sugiere usar ```gpt 3.5```, preimplementada en el módulo IA/gpt3_5
   2. Español: Se sugiere usar ```LlaMa 3``` con finetuning
3. Se calcula la correctitud de la respuesta (en término de ratio de palabras que no existen), y se intenta corregir con un nuevo prompt en caso de ser necesario (Este paso es opcional, pero asegura que el mensaje esté bien escrito).

## Visualización del árbol de interacciones
Se visualializa el árbol en un orden DFS. Esta estructura es totalmente modificable a lo que desee el usuario.

## Módulos adicionales creados
1.  ```get_data.py```: Obtiene las funciones que se usan dentro de ```run_and_prompts.ipynb``` para formatear, obtener y limpiar cada uno de los datos que soil entrega como output.
2.  ```ia.py```: Obtiene las funciones que se usan para entregar el prompt y recibir la respuesta del endpoint.
3.  ```post.py```: Crea la clase Post, que hereda de la clase Node de anytree, que maneja todo lo relacionado a una interacción.
4.  ```templates.py```: Almacena los templates de prompts que se envían al endpoint.
5.  ```transform_time.py```: Transforma los steps del simulador a tiempo continuo en minutos con segundos. Nota: El step sólo considera un intervalo de tiempo, posterior a esto, se hace un muestreo aleatorio de una normal(0,1) que permite obtener un tiempo exacto dentro de ese intervalo.
6.  ```spelling_checker.py```: Contiene la función que calcula la correctitud de un texto y la que crea el prompt para corregir un texto anterior.
7.  ```yml_create_functions.py```: Contiene las funciones que transforman los parámetros ingresados en los dict a texto en el formato .yml.

## Clase Post
La clase Post almacena cada uno de los atributos de una interacción, y también implementa los siguientes métodos para manejar esta interacción:
### get_prompt()
Obtiene el prompt de cada interacción.
### create_post()
Genera el prompt en el caso de que sea una respuesta al post raíz.
### create_reply()
Genera el prompt en el caso de que sea una respuesta a otro post distinto del raíz. La respuesta siempre es al primer ancestro que no sea respost.
### search_to_reply()
Entre las interacciones, obtiene el primer ancestro que no es repost.


## Librerías externas

La librerías externas que se utilizaron fueron (Las versiones son las sugeridas):

1. Python (==3.9.x)
2. Anytree (==2.8.0)
3. Soil (==0.20.7)
4. Scipy (==1.8.0)
5. Numpy (==1.24.3)
6. Pyenchant
 
## Ejemplo
Link: En el [siguiente ejemplo](https://github.com/minsoos/network_simulator/blob/master/run_and_prompts.ipynb)