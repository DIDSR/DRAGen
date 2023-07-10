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
    """ 
    Generates, evaluates and saves decision regions.

    Parameters
    ==========
    input_csv_path
        File path to the input csv; passed to :func:`load_attributes <src.data_input.load_attributes.load_attributes>`.
    onnx_model_path
        Onnx model file path.
    output_path
        Name and path for output file.
    batch_size
        Batch size for :class:`plane_loader <src.decision_region_generation.vicinial_distribution.plane_loader>`.
    manager_kwargs : dict
        Keyword arguments to be passed to :class:`TripletManager <src.decision_region_generation.triplet_manager.TripletManager>`.
    vicinal_kwargs : dict
        Keyword arguments to be passed to :class:`plane_dataset <src.decision_region_generation.vicinial_distribution.plane_dataset>`.
    overwrite : bool
        If True, will overwrite existing file at output_path.
    """
    # setup ------------------------------------------------------------------------------------------------------------------------
    print("Loading model...",end='')
    model = onnx.load_model(onnx_model_path)
    onnx.checker.check_model(model) # check for valid model
    print("Complete")
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
        print("Resuming decision region generation")
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
        vd_coords = []
        loader = plane_dataloader(vicinal_dist,batch_size=batch_size, output_dtype=np_dtype)
        for batch, idx, coords in loader:
            logits, emb = ort_session.run(None, {'input':batch})
            vd_outputs += logits.tolist()
            vd_coords += [coords]
        vd_outputs = np.concatenate(vd_outputs)
        vd_coords = np.array(np.concatenate(vd_coords))
        dist_group = group.create_dataset(decision_region_name, data=vd_outputs) #specific vicinal distribution
        dist_group.attrs.create('triplet',triplet['triplet']) # save the file paths to the triplet images
        dist_coord_group = group.create_dataset(decision_region_name + "__coordinates", data=vd_coords)
    print(f"Decision region generation complete; output file: {output_path}")
        