import matplotlib.pyplot as plt
import os

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
        step = int(dato[keys["t_step"]])

        if step != last_step and step != -1 and last_step != -1:
            # If step != -1 (well initial conf) and we pass from one step to another
            agg = len(responses_progress)-1
            # print(f"Step is {step} and last_step is {last_step}... agg={agg}")
            # print(type(step), "or", type(last_step))
            if step-last_step-1 > 0 and agg >= 0:
                # if exist steps in the interim (Exist steps where have no changes in the interim)
                for i in range(step-last_step-1):
                    # print(f"Length is {len(responses_progress)} and it adds {agg+i}, we are in")
                    responses_progress.append(responses_progress[agg].copy())
            if agg == -1:
                # agg == -1 when doesn't exist changes before this step
                # So we have to add zeros
                for i in range(step-1):
                    # print(f"Add 0 for {i}-th time")
                    responses_progress.append({"question": 0, "deny": 0, "comment": 0, "support": 0}.copy())

            # print(f"Add {step}")
            responses_progress.append(n_responses.copy())
        last_step = step

        if not count_repost:
            if bool(int(dato[keys["repost"]])):
                continue

        if dato[keys["state"]] == "cured":
            n_responses[ dato[keys["response"]] ] +=1
            if dato[keys["response"]] == "deny":
                n_responses["support"] -= 1
            elif dato[keys["response"]] == "support":
                n_responses["deny"] -= 1
            elif dato[keys["response"]] == "question":
                n_responses["comment"] -= 1
            elif dato[keys["response"]] == "comment":
                n_responses["question"] -= 1
            else:
                print("ERROR IN cured_state plot_functions.py")
        elif dato[keys["state"]] == "died":
            pass
        elif dato[keys["state"]] in ["backsliding", "infected"]:
            response_i = dato[keys["response"]]
            if response_i == None:
                print(dato)
            n_responses[response_i] += 1
        else:
            print("ERROR IN plot_functions.py")
    # print(step)
    # print(n_responses)
    # print("real:", len(responses_progress))
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

def plot_curve(curve, show=True, name_running=''):
    fig, ax = plt.subplots(1, 1)
    fig.suptitle(name_running, fontsize=16)
   
    ax.plot(curve)
    plt.tight_layout()

    if show:
        plt.show()
    else:
        path_save = os.path.join('', f'plot {name_running}.png')
        plt.savefig(path_save)
        plt.close()