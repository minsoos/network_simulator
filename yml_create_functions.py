def make_yml(dict_parameters, indentation=0):
    space = "  "
    data = ""
    dict_par = dict_parameters
    for element in dict_par:
        data += space*indentation

        if type(dict_par[element]) not in [dict, list]:
            data += element + ": " + str(dict_par[element]) + "\n"

        elif type(dict_par[element]) == dict:
            data += element + ":\n"
            data += make_yml(dict_par[element], indentation=indentation+1)
        else:
            raise Exception("Unknown element in dict_parameters from make_yml")
    return data


def make_network_agents_yml(network_agents):
    data = "network_agents:\n"

    for element in network_agents:
        if element == "default":
            continue

        for instance in network_agents[element]:
            data += "- agent_type: " + element + "\n"

            agent_states = network_agents["default"].copy()

            for data_change in instance:
                if data_change == "weight":
                    continue
                agent_states[data_change] = instance[data_change]
            dict_instance = {
                "state": agent_states,
                "weight": instance["weight"]
            }

            data += make_yml(dict_instance, indentation=1)

    return data
