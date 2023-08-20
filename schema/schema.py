from soil.agents import FSM, state, default_state, prob, NetworkAgent
from soil import Environment
import random
import logging

from scipy.stats import norm
import numpy as np


logging.basicConfig(level=logging.WARNING, filename='logs.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.warning('This is a depuration message')


RESPONSES = ["support", "deny", "question", "comment"]

class NewsEnvironmentAgent(Environment):
    def __init__(self, name=None, network_agents=None, environment_agents=None, states=None, default_state=None, interval=1,
                 network_params=None, seed=None, topology=None, schedule=None, initial_time=0, environment_params=None, history=True,
                 dir_path=None, **kwargs):
        super().__init__(name, network_agents, environment_agents, states, default_state, interval, network_params, seed, topology,
                         schedule, initial_time, environment_params, history, dir_path, **kwargs)
        N_AGENTS = len(self.G.nodes())
        time_connections = np.random.normal(self["mean_time_connection"],
                                            self["var_time_connection"], N_AGENTS)
        time_connections = list(map(lambda x: int(x), time_connections))
        for i, agent in enumerate(self.network_agents):
            agent["time_connection"] = time_connections[i]
        self["id_message"] = 1

#  logging.warning(self["time_connection"])


class DumbViewer(FSM):
    '''
    A viewer that gets infected via TV (if it has one) and tries to infect
    its neighbors once it's infected.
    '''
    @default_state
    @state
    def time_0(self):
        '''
        Allows that at step 0, nothing happens
        '''
        self.set_state(self.no_susceptible)
        self.last_infection = 0

    @state
    def no_susceptible(self):
        '''
        Enables a agent to participate in the network only after connecting
        '''
        if self.env.now >= self["time_connection"]:
            self.set_state(self.neutral)

    @state
    def neutral(self):
        '''
        Allows agents to infect themselves
        '''
        if self['has_tv']:
            self.try_infect(infecter=self, first_time=True)

    @state
    def infected(self):
        '''
        The agent begins to infect
        '''
        if self.last_infection == self.now:
            return
        logging.warning(
            f"{self['id']} está en el estado infectar en el step {self.env.now}")
        for neighbor in self.get_neighboring_agents(state_id=self.neutral.id):
            neighbor.try_infect(infecter=self, first_time=True)

        self.try_infect(infecter=self, first_time=False)

        if prob(self.env["prob_dead"]):
            self.set_state(self.died)

    @state
    def died(self):
        '''
        The agent stop participating to the network
        '''
        pass

    def try_infect(self, infecter, first_time):
        '''
        This is not a state. It is a function that other agents can use to try to
        infect this agent. DumbViewer always gets infected, but other agents like
        HerdViewer might not become infected right away
        '''

        if not isinstance(self, DumbViewer):
            raise Exception("Type Error of infecter in infect method")
        # Check successful
        if first_time and infecter == self:
            successful_infect = self.check_tv_infect()
        elif first_time:
            successful_infect = self.check_neighbor_infect()
        elif not first_time:
            successful_infect = self.check_backsliding_infect()

        if not successful_infect:
            return

        # If we are successful:
        self.set_state(self.infected)
        self.last_infection = self.now
        self.assign_id_message()
        self.assign_id_message_parent(infecter)
        #
        repost = prob(self.env["prob_repost"]) if first_time else False
        # and infecter != self ## To block repost for root

        response = self.find_response()
        self.assign_infect_attrs(first_time, repost, response, infecter)

    def assign_infect_attrs(self, first_time, repost, response, infecter):
        if not first_time:
            self['method'] = 'backsliding'
            self['response'] = self['response']
            self['stance'] = self['stance']
            self['repost'] = repost
            return
        if repost:
            self['repost'] = True
            self['response'] = 'support'
            self['stance'] = 'agree'
            return
        self['repost'] = repost
        self['response'] = response
        self["stance"] = self["stance"]

        if self == infecter:
            self['method'] = 'tv'
        else:
            self['method'] = 'friend'
            self["cause"] = infecter.id

    def assign_id_message(self):
        self["id_message"] = self.env["id_message"]
        logging.warning(
            f"{self['id']} ha enviado un mensaje con id {self['id_message']}. Se infectó por el método {self['method']} en el tiempo {self.env.now}")
        self.env["id_message"] += 1

    def assign_id_message_parent(self, infecter):
        if infecter != self:
            self['parent_id'] = infecter['id_message']
        else:
            self['parent_id'] = 0

    def find_response(self):
        type = self["type"]
        prob_response_self = {}
        for response in RESPONSES:
            name_prob = f"prob_{type}_{response}"
            prob = self.env[name_prob]
            prob_response_self[response] = prob

        if self["stance"] == "against":
            prob_response_self["support"] = 0
        elif self["stance"] == "agree":
            prob_response_self["question"] = 0
            prob_response_self["deny"] = 0
        elif self["stance"] == "neutral":
            prob_response_self["agree"] = 0
            prob_response_self["deny"] = 0


        choiced = random.choices(
            list(prob_response_self.keys()), list(prob_response_self.values()))
        if choiced[0] == None:
            raise ValueError("The response cant be Null")

        return choiced[0]

    def check_tv_infect(self):
        return prob(self.env['prob_tv_spread'])

    def check_neighbor_infect(self):
        return prob(self.env['prob_neighbor_spread'])

    def check_backsliding_infect(self):
        return prob(self.env['prob_backsliding'])


class HerdViewer(DumbViewer):
    '''
    A viewer whose probability of infection depends on the state of its neighbors.
    '''

    def check_neighbor_infect(self):
        infected = self.count_neighboring_agents(state_id=self.infected.id)
        total = self.count_neighboring_agents()
        prob_infect = self.env['prob_neighbor_spread'] * infected/total
        # self.debug('prob_infect', prob_infect)
        return prob(prob_infect)


class WiseViewer(HerdViewer):
    '''
    A viewer that can change its mind.
    '''

    @state
    def cured(self):
        prob_cure = self.env['prob_neighbor_cure']
        for neighbor in self.get_neighboring_agents(state_id=self.infected.id):
            if prob(prob_cure):
                try:
                    if self["stance"] != "neutral":
                        neighbor.cure(self)
                except AttributeError:
                    self.debug('Viewer {} cannot be cured'.format(neighbor.id))
        return

    def cure(self, doctor):
        self['repost'] = False

        if self["stance"] == "against":
            self["stance"] = "agree"
        elif self["stance"] == "agree":
            self["stance"] = "against"
        else:
            raise Exception("Unrecognized Stance")

        if self["response"] == "deny":
            self["response"] = "support"
        elif self["response"] == "support":
            self["response"] = "deny"
        elif self["response"] == "question":
            self["response"] = "comment"
        elif self["response"] == "comment":
            self["response"] = "question"
        else:
            raise Exception("Unrecognized response")
        self.assign_cure_attrs(doctor)
        self.assign_id_message()
        self.assign_id_message_parent(doctor)
        self.set_state(self.cured)
        return

    def assign_cure_attrs(self, doctor):
        if self == doctor:
            self["method"] = "self"
        else:
            self["cause"] = doctor.id
            self["method"] = "friend"

    @state
    def infected(self):
        cured = max(self.count_neighboring_agents(self.cured.id),
                    1.0)
        infected = max(self.count_neighboring_agents(self.infected.id),
                       1.0)
        prob_cure = self.env['prob_neighbor_cure'] * (cured/infected)
        if prob(prob_cure):
            self.cure(self)
        super().infected()
        return
