import pandas as pd
import numpy as np
import h5py

def determine_composition(decision_region, tasks, output_function=None, thresholds=[0.5]):
    """ Determine the composition of an individual decision region """
    if type(tasks) == list:
        raise NotImplementedError("Not yet implemented for list of tasks")
    if type(thresholds) != list: # support float/int thresholds
        thresholds = [thresholds] # TODO: single threshold for multiple tasks?
    DR = decision_region[:]
    if output_function is not None:
        DR = output_function(DR)
    if len(tasks) == 1:
        DR = DR.reshape(DR.size, 1) # TODO: check that dimension order is consistent with multiple task outputs
    df = pd.DataFrame(DR,columns=tasks.keys())
    percent_compositions = {}
    for i, task  in enumerate(tasks):
        df[task] = np.where(DR[:, i] > thresholds[i], tasks[task][1], tasks[task][0])
        # get percent assigned to each task option
        gb = df.groupby(task).size()
        for opt in tasks[task].values():
            if opt not in gb: # this class is not in the decision region
                percent_compositions[f"{task}:{opt}"] = 0
            else:
                percent_compositions[f"{task}:{opt}"] = (gb[opt]/len(df))*100
    # TODO: percent each combination of classes for multiclass classification
    return percent_compositions

def get_compositions(filepath, tasks, output_function=None, thresholds=[0.5], aggregate=None):
    """ Agets the compositions of all decision regions in a decision region file"""
    file = h5py.File(filepath, 'r')
    percent_compositions = []
    for group in file.keys():
        for region in file[group].keys():
            pc = determine_composition(file[group][region], tasks=tasks, output_function=output_function, thresholds=thresholds)
            pc['group'] = group
            pc['region'] = region
            percent_compositions.append(pc)
    df = pd.DataFrame.from_records(percent_compositions)
    if not aggregate: 
        return df
    elif aggregate == 'group':
        return df.groupby('group').agg(['mean','std'])
    elif aggregate == 'all':
        return df.drop(['group','region'], axis=1).agg(['mean','std'])
    elif aggregate == 'class':
        df_list = []
        for task in tasks:
            df[task] = None
            for group in file.keys():
                group_idxs = df[df.group == group].index
                df.loc[group_idxs, task] = file[group].attrs[task]
            df_list.append(df.drop(['group','region'], axis=1).groupby(task).agg(['mean', 'std']))
        if len(df_list) == 1:
            return df_list[0]
        else:
            return df_list

    



        
    