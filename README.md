# Network Simulator
Network Simulator is a library that can generate artificial social network data, based in a news as a seed.
## Installation
Network Simulator is in the PyPI repository as 'network-simulator'. To install it, you need to have pip installed. Then, use the following command to install the library
<div style="text-align:center;">
  <strong>pip install network-simulator</strong>
</div>

To complete the installation, it is needed an additional dependence, ``libenchant``. In Windows, it is not necessary to install it manually, but it is in Linux, you should use one of the following commands:
<!---

### macOS
<div style="text-align:center;">
  <strong>brew install enchant</strong>
</div>
-->
### Linux
Depending on the distribution, various libraries could be available, for instance, in ubuntu, you can use:
<div style="text-align:center;">
  <strong>sudo apt install libenchant-2-2</strong>
</div>

## Schema
The following simulation schema is split into environment agents and network agents.
In this particular case, the default schema (in ```schema.py```) in which the simulation is based, is as follows (based on soil schema example):
### Environment agents
The environment agent models the probabilities, that coincide for every agent in the network and time. The time refers to the step at which simulation is. Environment agent also model agent's time connection. The time in what each agent entry to the network is modeled by a normal distribution, whose parameters, ```mean_time_connection``` and ```var_time_connection``` (in discrete units), can be modified from the following file: ```run_and_prompts.ipynb```. An agent begins to be susceptible when it is connected to the network, and this it stays connected until the state changes to ```died```.

### Social Network Agents
The social network agents model autonomous individuals within social network. They have states, functions that run once per step.

At step 0, no agent is able to interact in the social network. This is modeled in the state ```time_0```.

Subsequently, an agent becomes susceptible when the social network time is higher than its time connection. This is modeled in the state ```no_susceptible```.

Thirdly,the agent can be susceptible to become infected by the news, if it has set as true its parameter ```has_tv```, in that case, it becomes infected with a probability ```prob_tv_spread```. Also, it can start out to be infected by infected nodes it is connected to, in other words, its neighbors in the social network. In this case, it becomes contagious with probability ```prob_neighbor_spread```. This is modeled in the state ```neutral```.

Now, when the agent is already infected, it has other behavior. In this case, the agent try to infect to all of his neighbors with probability ```prob_neighbor_spread```. Also, it could reinfect with probability ```prob_backsliding```, this means that the node rejoin to the network. For this instance, it samples an infected node to reply (Being the degree in the social network as a weight), even whether it is not neighbor of the original node. At last, the node can die with probability ```prob_died```. It is important to note that the agent always 'infect' with its last message, i.e., every reply are intended to the last message.

If an agent dies, it leaves social network. This is modeled in the state ```died```

The types of social network agents are as follows:

#### NaiveViewer:
It acquires the base behavior of a regular agent.
#### DubiousViewer:
It acquires the behavior of a Dumb Agent, modifying
1. It weights the probability of getting infected by a neighbor by the number of neighbors. The probability of being infected is lower than a Dumb Agent, unless all of neighbors are infected

#### InformedViewer:
It acquires the behavior of a Herd Agent, modifying:
1. Now, the node can cure, that means a changing to the opposite opinion (response and stance). It also can try to cure other agents with a probability ```prob_neighbor_cure```, only if they are wise type and they have a distinct stance (excluding neutral stance). This is modeled in the state ```cured```
2. It also can cure itself, which is modeled by the probability ```prob_neighbor_cure```*```vecinos_curados```/```vecinos_infectados```. Outside this, the agent adopt the behavior of a Herd Agent. This is modeled in the state ```infected```

## Social network connection generation

The connection network between users is generated by a method called Barabasi-Albert, that receives two parameters, ````n```` and ````m````.
1. ````n```` is the number of social network agents that will have the social graph.
2. ```m``` is the number of edges that each agent is going to connect, using as connection probability weight the nodes degree.
(For more information check Barabasi-Albert Method)

## Interaction features
1. ```id_message```: It is a unique interaction id. It ranges between 1 and number of interactions.
2. ```state```: Indicates the state in which the interaction was produced.
3. ```stance```: Indicates whether the agents is in favor (```agree```) or against (```against```) the news. It could change during the simulation, but each agent has been set by default. In literature, this is known as 'affective polarization'.
4. ```response```: Indicates the kind of comment that the agent do. It can be either ```support```, ```deny```, ```question```, or ```comment```. The probabilities depend on the weights given as inputs, but given certain stances, some responses can be blocked. In literature, the term is referred to as the 'truth stance'.
5. ```repost```: Indicates whether a post is a mention of the one before or it is an 'original' post. The repost probability is given as input. it can be 0 or 1. This probability is not used for backsliding interaction.
6. ```method```: Indicates the infection method. It could be ```backsliding``` (if it relapse into infection), ```tv``` (if the infection was through the root node) or ```friend``` (if the infection was through a neighbor).
7. ```cause```: Indicates the infection cause, if it was through a neighbor. It could be any id in social agent id's. It ranges between 1 and ```n```.
8. ```parent_id```: Indicates the interaction id. It range between 1 and the number of interactions. 

## Interaction contraints
1. If the interaction method is ```backsliding```, the agent will keep its stance and response.
2. If the interaction is ```repost```, the response will be ````support```` and the stance ````agree````.
3. If the stance is ````against````, the response probability of ```support``` will be 0.
4. If the stance is ````agree````, the response probability of ```question``` y ```deny``` will be 0.
5. If the stance is ````neutral````, the response probability of ```support``` y ```deny``` will be 0.

## Parameters to configure in the simulation
1. Agents parameters by defect: These are the parameters that each agent will have, unless some specified change.
2. Network agent configuration: Here, each agent class is going to be created. Each one has weights, ```weight```, that indicate how likely they appear in the social network compared to the rest. Additionally, the specific desired parameters for each one can be set. At last, it must be added the correct type in ```type```.
3. Environment agents configuration: Here, every spread probability is set. Also, are configured the parameters of the connection normal distribution, the time intervals and the social network generation graph and its parameters. Note: By defect, the simulator always simulate 1 step less than the set.

4. Responses probability: It is necessary to add weights for each response and agent in a dictionary (It is not necessary that weights sum to 1).

## Simulation Execution

Cells in the file ```example.ipynb``` must be executed. They are ready to go, basically, they do:

1. Create the file ```.yml``` that indicate the simulation parameters.
2. Execute the soil command in cmd, that will run the simulation.

## Conversation making
1. Soil data output is gotten.
2. Data is pivoted, for easy readability.
3. The title and body news are defined.
4. It is defined a Post instance, that will be the tree interaction root node.
5. It is defined the initial and final time in the simulation.
6. Each interaction data is used for create Post instances and add them to the interaction tree

## LLM model connection
1. It is gotten the prompt of each interaction, giving as a parameter language, minimum and maximum characters and the user description.
2. It is defined an endpoint to send the prompt and get a reply, that will be the text in the interaction, in essence, what the network agent post in the social network.
   1. English: It is suggested to use ```gpt 3.5```, pre-implemented in gpt3_5/gpt3_5 module.
   2. Spanish: It is suggested to use finetuned ```LlaMa 2```
3. The reply correctness is calculated (in terms of the non-existent word ratio). If the correctness is low, the text will try to correct. (This step is optional, but ensure better results)

## Interaction tree visualization
The tree is visualizated in a DFS order. This structure is completely editable.

## Additional modules

1.  ```get_data.py```: It gets the functions that are used in ```example.ipynb``` for formatting, getting and cleaning soil output data.
2.  ```ia.py```: It gets the functions that are used for provide prompt and get the reply from the endpoint.
3.  ```post.py```: It creates Post class, that inherit from anytree class Node. Post class manage everything related to interaction
4.  ```templates.py```: It stores the prompt templates that are sent to the endpoint
5.  ```transform_time.py```: It transforms the simulator steps to continuous time in minutes and seconds. Mark: It consider just a time interval and sample the exact time inside it with a normal distribution.
6.  ```spelling_checker.py```: It contains the function that calculates the correctness of a text and the one that creates the prompt to correct a previous text.
7.  ```yml_create_functions.py```: It contains the function that transform input parameters in the beginning into .yml format.

## Post class
The Post class stores each of the attributes of an interaction and also implements the following methods to handle the interaction:
### get_prompt()
It gets the prompt of each interaction
### create_post()
It generates the prompt if it is a reply to the root post
### create_reply()
It generates the prompt if it is not a reply to the root post. The reply is directed to the first non-repost ancestor
### search_to_reply()

Among the interactions, it gets the first ancestor that is not a repost.

## External libraries


The external libraries that were used are (versions are suggested):

1. Python (>=3.6.x)
2. Anytree (>=2.8.0)
3. Soil (==0.20.7)
4. Scipy (>=1.8.0)
5. Numpy (>=1.24.3)
6. Pyenchant (>=3.2.2)
 
## Example Google Colab
There's an example that it is ready to use in the [following link](https://github.com/minsoos/network_simulator/blob/master/example/example_google_colab.ipynb) in google colab.

## Example from the paper
There is an example that is released to reproduce experiments of our paper "Simulating Online Conversations using Agent-Based Modeling and Large Language Models" in the [following link](https://github.com/minsoos/network_simulator/blob/master/example/example.ipynb) 

Updated: 25 June 2025.
