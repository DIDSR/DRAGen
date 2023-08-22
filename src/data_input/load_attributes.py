from multiprocessing import Pool
from PIL import Image
import pandas as pd
import numpy as np
import itertools
import os
from typing import Optional

# TODO: better term for 'missing_information' argument

def load_attributes(csv_file:str, subgroup_information:dict, image_path_column:str="Path", id_column:Optional[str]=None, missing_information:str='raise', 
                    info_format:str='categorical', rel_path:Optional[str]=None, n_processes:Optional[int]=None)->pd.DataFrame:
  """
  Loads image filepaths and patient attributes from provided csv file.
  
  Parameters
  ----------
  csv_file
      Filepath to summary csv.
  subgroup_information
      Subgroup attributes in the format Group:[subgroups] (ex. ``{"Sex":["Male","Female"]}``).
  image_path_column
      Name of column in csv_file listing image filepaths.
  id_column
      Name of columns in csv_file listing unique patient/sample identifiers.
  missing_information
      How to handle samples missing information; 'raise': raise an exception, 'remove': remove samples missing information
  info_format
      Format to return patient information in.
  rel_path
      Declare a relative path for image file paths.
  n_processes
      Number of processes to use while checking image file paths, if :obj:`None`, uses number of available cores.
  
  Returns
  -------
  pandas.DataFrame
      DataFrame of ids, image filepaths, and subgroup information.
  """
  df = pd.read_csv(csv_file)
  if id_column is not None and id_column not in df.columns:
    raise Exception(f"id column '{id_column}' not found in {csv_file}")
  if image_path_column not in df.columns:
    raise Exception(f"image file path column '{image_path_column}' not found in {csv_file}")
  if rel_path is not None:
    df[image_path_column] = df[image_path_column].apply(lambda x: os.path.join(rel_path, x))
  good_img_paths = check_img_paths(df[image_path_column].values, n_processes)
  df = df[df[image_path_column].isin(good_img_paths)]
  if subgroup_information:# Check how the subgroup information is reported in the csv file
    if set(subgroup_information.keys()).issubset(df.columns): # categorical subgroup information
      for k, v in subgroup_information.items():
        if not set(df[k].unique()).issubset(set(v)):
          if missing_information == 'raise':
            raise Exception(f"Found value(s) {set(df[k].unique())} for attribute {k}, only expected value(s) {set(v)}")
          elif missing_information == 'remove':
            df = df[df[k].isin(v)].copy()
    elif set([x for y in subgroup_information.values() for x in y]).issubset(df.columns): # binary subgroup information
      for k, v in subgroup_information.items():
        df[k] = df[v].idxmax(axis=1)
  if id_column is not None:
    df = df[[id_column, image_path_column] + list(subgroup_information.keys())].copy()
  else:
    df = df[[image_path_column] + list(subgroup_information.keys())].copy()
  if info_format == 'binary':
    df = pd.get_dummies(df, columns=list(subgroup_information.keys()))
  # rename image path (and ID) columns to standard format
  df = df.rename(columns={image_path_column:'Path'})
  if id_column is not None:
    df = df.rename(columns={id_column:"ID"})
  return df
  
def check_img_paths(img_paths:np.array, n_processes:Optional[int]=None): # TODO: n_processes as an argument
  """
  Checks image file paths to ensure that file paths exist, the program has read access, and the files are in an image file format. 

  Arguments
  =========
  img_paths
    File paths of the sample images.
  n_processes
    Number of processes to be used for `multiprocessing.Pool`, if None, uses all available.

  Returns
  =======
  numpy.array
    Array of usable file paths.

  Raises
  ======
  Exception
    Raises an exception if not all of the provided file paths are valid.

  """
  pool = Pool(n_processes)
  # (1) + (2) # os.access returns False if file does not exist
  exists = np.array(pool.starmap(os.access, zip(img_paths,itertools.repeat(os.R_OK))))
  existing_paths = img_paths[exists]
  if len(existing_paths) < len(img_paths):
    raise Exception(f"Invalid image path given for {len(img_paths)-len(existing_paths)}/{len(img_paths)} image(s). Check input_csv and img_rel_path.")
  # (3) check that file format is supported by PIL.Image
  supported_exts = Image.registered_extensions()
  extension_check = np.array(pool.starmap(check_img_extension, zip(existing_paths, itertools.repeat(supported_exts))))
  good_extensions = existing_paths[extension_check]
  return good_extensions
  
def check_img_extension(img_path, supported_extensions):
  __, file_extension = os.path.splitext(img_path)
  return file_extension in supported_extensions
  
  