import pandas as pd
import numpy as np
import h5py
import os

def determine_composition(decision_region:h5py.Dataset, tasks:dict, output_function:str=None, thresholds:list=[0.5])->pd.DataFrame:
    """ Determine the composition of an individual decision region.
    
    Arguments
    =========
    decision_region
        Decision region for a single triplet.
    tasks
        Model classification tasks.
    output_function
        Function to be applied to model output scores.
    thresholds
        Thresholds for each task.

    Returns
    =======
    pandas.DataFrame
        Decision region composition.
    
    """   
    DR = decision_region[:]
    if output_function is not None:
        DR = output_function(DR)
    if len(tasks) == 1:
        DR = DR.reshape(DR.size, 1)
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
    return percent_compositions

def get_compositions(filepath:str, tasks:dict, output_function:str=None, thresholds:list=[0.5], aggregate:str=None)->pd.DataFrame:
    """ Gets the compositions of all decision regions in a decision region file.
    
    Arguments
    =========
    filepath
        File path of decision region hdf5 file.
    tasks
        Model classification tasks.
    output_function
        Function to be applied to model output scores.
    thresholds
        Thresholds for each task.
    aggregate
        How to aggregate the compositions.

    Returns
    =======
    pandas.DataFrame
        Dataframe of decision region compositions.
    
    """
    file = h5py.File(filepath, 'r')
    percent_compositions = []
    att_cols = set()
    for group in file.keys():
        for region in file[group].keys():
            if region.endswith("__coordinates"):
                continue
            pc = determine_composition(file[group][region], tasks=tasks, output_function=output_function, thresholds=thresholds)
            pc['group'] = group
            pc['region'] = region
            for att in file[group].attrs:
                pc[att] = file[group].attrs[att]
                att_cols.add(att)
            percent_compositions.append(pc)
    df = pd.DataFrame.from_records(percent_compositions)
    numeric_cols = list(df.select_dtypes(include=np.number).columns)
    if not aggregate: 
        return df
    elif aggregate == 'group':
        return df.groupby(['group'] + list(att_cols))[numeric_cols].agg(['mean','std'])
    elif aggregate == 'all':
        return df[numeric_cols].agg(['mean','std'])
    elif aggregate == 'class':
        df_list = [df.groupby(task)[numeric_cols].agg(['mean','std']) for task in tasks]
        if len(df_list) == 1:
            return df_list[0]
        else:
            return df_list

def save_compositions(compositions:pd.DataFrame, save_loc:str, overwrite:bool=False, aggregate:str=None):
    """ Saves the compositions analysis in a csv file
    
    Arguments
    =========
    compositions
        Decision region compositions, as output by :func:`get_compositions`.
    save_loc
        Save location
    overwrite
        Whether or not to overwriting existing files.
    aggregate
        The aggregation method; used as part of naming convention.
    """
    if aggregate is None:
        save_name = f"{save_loc}/decision_region_compositions.csv"
    else:
        save_name = f"{save_loc}/decision_region_compositions_{aggregate}.csv"
    if os.path.exists(save_name) and not overwrite:
        i = 1
        save_name = save_name.replace(".csv",f"_({i}).csv")
        while os.path.exists(save_name):
            save_name = save_name.replace(f"_({i}).csv",f"_({i+1}).csv")
            i += 1
    print(f"Saving decision region compositions to file: {save_name}")
    compositions.to_csv(save_name) 



        
    