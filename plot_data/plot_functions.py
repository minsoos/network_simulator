import matplotlib.pyplot as plt

def responses_progress(data, count_repost):
    keys = {"id_node": 0, "t_step": 1, "id_msj": 2, "parent_id": 3,
            "state": 4, "cause": 5, "method": 6, "response": 7,
            "stance": 8, "repost": 9}

    responses_progress = []
    last_step = 1
    n_responses = {
        "question": 0,
        "deny": 0,
        "comment": 0,
        "support": 0
    }

    for dato in data:
        step = dato[keys["t_step"]]
        if step != last_step:
            responses_progress.append(n_responses.copy())
        last_step = step

        if not count_repost:
            if bool(int(dato[keys["repost"]])):
                continue

        if dato[keys["state"]] == "cured":
            if dato[keys["response"]] == "deny":
                n_responses["support"] -= 1
            elif dato[keys["response"]] == "support":
                n_responses["deny"] -= 1
            elif dato[keys["response"]] == "question":
                n_responses["comment"] -= 1
            elif dato[keys["response"]] == "comment":
                n_responses["question"] -= 1
        elif dato[keys["state"]] == "died":
            pass
        else:
            response_i = dato[keys["response"]]
            if response_i == None:
                print(dato)
            n_responses[response_i] += 1

    print(n_responses)
    return responses_progress

def plot_responses(responses_progress, show=True, name_running=''):
    fig, axs = plt.subplots(2, 2)
    fig.suptitle(f"Responses's curves of {name_running}", fontsize=16)

    position_responses = [["question", "deny"], ["comment", "support"]]

    for y_id, y in enumerate(position_responses):
        for x_id, x in enumerate(position_responses[y_id]):
            current_response = position_responses[y_id][x_id]
            axs[y_id][x_id].plot(range(len(responses_progress)), [
                                 response[current_response] for response in responses_progress])
            axs[y_id][x_id].set_xlabel("Step")
            axs[y_id][x_id].set_ylabel(current_response)
            axs[y_id][x_id].set_title(f"{current_response} vs Tiempo")
    plt.tight_layout()

    if show:
        plt.show()
    else:
        path_save = os.path.join('', f'plot {name_running}.png')
        plt.savefig(path_save)
        plt.close()