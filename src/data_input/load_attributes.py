from multiprocessing import Pool
from PIL import Image
import pandas as pd
import numpy as np
import itertools
import os

# TODO: better term for 'missing_information' argument

def load_attributes(csv_file, subgroup_information:dict, image_path_column="Path", id_column=None, missing_information='raise', info_format='categorical', rel_path=None, n_processes=None):
  """
  Loads image filepaths and patient attributes from provided csv file.
  
  Parameters
  ----------
  csv_file : :obj:`str`
      Filepath to summary csv.
  subgroup_information : :obj:`dict`
      Subgroup attributes in the format Group:[subgroups] (ex. {"Sex":["Male","Female"]}).
  image_path_column : :obj:`str`, `optional`
      Name of column in csv_file listing image filepaths.
  id_column : :obj:`str` or :obj:`None`, `optional`
      Name of columns in csv_file listing unique patient/sample identifiers.
  missing_information : :obj:`str`, `optional`
      How to handle samples missing information; 'raise': raise an exception, 'remove': remove samples missing information
  info_format : :obj:`str`, `optional`
      Format to return patient information in.
  rel_path : :obj:`str` or :obj:`None`, `optional`
      Declare a relative path for image file paths.
  n_processes : :obj:`int` or :obj:`None`, `optional`
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
        if set(df[k].unique()) != set(v):
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
  
def check_img_paths(img_paths:np.array, n_processes=None): # TODO: n_processes as an argument
  """
  Checks image file paths to ensure (1) file paths exist, (2) program has read access, and (3) file is in an image file format. 
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
  
  