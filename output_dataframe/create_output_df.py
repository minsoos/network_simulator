import pandas as pd

def nodes_message(nodes_list):
    iteration = []
    name_source = []
    message = []
    owner = []
    response = []
    stance = []
    step = []
    repost = []
    for i in range(1,len(nodes_list)): 
        name_source.append(nodes_list[i].parent.name)
        message.append(nodes_list[i].message)
        iteration.append(nodes_list[i].name)        
        owner.append(nodes_list[i].owner) 
        response.append(nodes_list[i].response)
        stance.append(nodes_list[i].stance)
        step.append(nodes_list[i].step)
        repost.append(nodes_list[i].repost)

    df_resume = pd.DataFrame({"step":step,"source_node":name_source,"iteration":iteration,"target_message":message,"interaction":response,"stance":stance,"repost":repost, "target_user":owner})
    return df_resume.sort_values(by="step")

def dict_messages(nodes_list):
    message = [nodes_list[0].message]
    id_node = [0]
    owner = [0]
    for i in range(1,len(nodes_list)): 
        if nodes_list[i].repost==False:
            message.append(nodes_list[i].message)        
            id_node.append(nodes_list[i].name)
            owner.append(nodes_list[i].owner)
    df_resume = pd.DataFrame({"id_node":id_node,"message":message}) 
    return df_resume

def dict_message_repost(nodes_list):
    id_node = []
    owner = [] 
    parent = []
    for i in range(1,len(nodes_list)): 
        if nodes_list[i].repost==True:    
          id_node.append(nodes_list[i].name)
          owner.append(nodes_list[i].owner)
          parent.append(nodes_list[i].parent.name)
    df_resume = pd.DataFrame({"id_node":id_node,"parent":parent }) 
    return df_resume.sort_values(by="parent")

def create_dict_messages(repost_results, message_dictionary):
    for i in sorted(set(repost_results.parent)):
        for j in message_dictionary.id_node:
            if i==j:
                message = repost_results[repost_results["parent"]==i].shape[0]*list(message_dictionary[message_dictionary["id_node"]==i]["message"])
                new = pd.concat((repost_results[repost_results["parent"]==i].reset_index(drop=True),pd.DataFrame({"message":message})),axis=1)[["id_node","message"]]
        message_dictionary = pd.concat((message_dictionary,new),axis=0).reset_index(drop=True)
    return message_dictionary

def owner_origin(nodes_list):
    id_node = []
    owner = [] 
    step = [] 
    for i in range(1,len(nodes_list)):  
          id_node.append(nodes_list[i].name)
          owner.append(nodes_list[i].owner)
          step.append(nodes_list[i].step)
    df_resume = pd.DataFrame({"id_node":id_node,"owner":owner, "step":step}) # , "id_node":id_node "parent":parent
    df_resume["clave"] = df_resume["id_node"].astype(str) +"-"+ df_resume["owner"].astype(str)
    return df_resume.sort_values(by="step")

def get_dataframe(list_nodes):
    message_dictionary_unique = dict_messages(list_nodes)
    result = nodes_message(list_nodes)
    message_dictionary = dict_messages(list_nodes)
    repost_results = dict_message_repost(list_nodes)
    message_dictionary_df = create_dict_messages(repost_results, message_dictionary)
    result_1 = result.merge(message_dictionary_df, left_on="source_node", right_on="id_node", how="left")
    result_1.drop(["id_node"], inplace=True,axis=1)
    result_2 = result_1.merge(message_dictionary_df, left_on="iteration", right_on="id_node", how="left")
    result_2.drop(["id_node"], inplace=True,axis=1)
    owner_list = owner_origin(list_nodes)
    result_3 = result_2.merge(owner_list, left_on="source_node", right_on="id_node", how="left")
    result_3.drop(["id_node"], inplace=True,axis=1)
    result_3.rename(columns={"step_x":"target_step","message_x":"source_message","owner":"source_user","step_y":"source_step"}, inplace=True)
    result_3.fillna(value = {"source_user":0,"source_step":0}, inplace=True)
    result_3["source_user"] = result_3["source_user"].astype("int64")

    df_output = result_3.merge(message_dictionary_unique, left_on="message_y", right_on="message", how="left")
    df_output.drop(["message_y","message","clave"], inplace=True,axis=1)
    df_output.rename(columns={"id_node":"target_node"}, inplace=True)
    return df_output