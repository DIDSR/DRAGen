import sys
sys.path.append("../")
from .triplet_manager import TripletManager
from .vicinal_distribution import plane_dataloader, plane_dataset
# from decision_region_generation import TripletManager, vicinal_distribution
from src.utils import progressbar, sigmoid
import numpy as np
import onnxruntime as ort
import onnx
import h5py
import os

def generate_decision_regions(input_csv_path:str, onnx_model_path:str, output_path:str, batch_size:int, manager_kwargs={}, vicinal_kwargs={}, overwrite=True):
    """ Uses the provided samples to generate vicinal distributions and evaluate """
    # setup ------------------------------------------------------------------------------------------------------------------------
    model = onnx.load_model(onnx_model_path)
    onnx.checker.check_model(model) # check for valid model
    ort_session = ort.InferenceSession(onnx_model_path, providers=ort.get_available_providers())
    # determine the expected numpy dtype for inputs to the model
    for input in model.graph.input:
        if input.type.tensor_type.HasField('elem_type'):
            np_dtype = onnx.mapping.TENSOR_TYPE_MAP[input.type.tensor_type.elem_type].np_dtype
    manager = TripletManager(input_csv=input_csv_path, **manager_kwargs)
    if overwrite:
        out_file = h5py.File(output_path, 'w')
    else:
        out_file = h5py.File(output_path, 'a')
    if len(out_file.keys()) != 0:
        print("Resuming Decision Region Generation")
    for triplet in progressbar(manager): # iterate through triplets, generate vicinal, eval, save -----------------------------------------------
        group_name = f"group_{triplet['group']}"
        decision_region_name = f"decision_region_{triplet['key']}"
        if group_name in list(out_file.keys()): # group for tripletmanager group
            group = out_file[group_name]
        else:
            group = out_file.create_group(group_name)
            for k,v in manager.groups[triplet['group']].items():
                group.attrs.create(name=k, data=v)
        if decision_region_name in group: # continue if dataset already exists
            continue
        vicinal_dist = plane_dataset(*triplet['images'],**vicinal_kwargs)
        vd_outputs = []
        loader = plane_dataloader(vicinal_dist,batch_size=batch_size, output_dtype=np_dtype)
        # TODO: there must be a better way to do this, look into hdf5 datasets more
        for batch, idx in loader:
            logits, emb = ort_session.run(None, {'input':batch})
            vd_outputs += logits.tolist()
        vd_outputs = np.concatenate(vd_outputs)
        dist_group = group.create_dataset(decision_region_name, data=vd_outputs) #specific vicinal distribution
        dist_group.attrs.create('triplet',triplet['triplet']) # save the file paths to the triplet images
        