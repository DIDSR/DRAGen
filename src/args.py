from argparse import ArgumentParser

def get_arguments():
  parser = ArgumentParser()
  # Define Arguments ==========================================================================================
  ## Required inputs ------------------------------------------------------------------------------------------
  parser.add_argument('--model_file', type=str, required=True)
  parser.add_argument('--data_csv', type=str, required=True)
  parser.add_argument('--save_loc', type=str, required=True)
  ## General settings -----------------------------------------------------------------------------------------
  parser.add_argument('--save_name', type=str, default='decision_regions')
  parser.add_argument('--batch_size', type=int, default=5)
  parser.add_argument('--out_function', type=str, default=None)
  parser.add_argument('--overwrite', action='store_true', default=False) # NOTE: will delete all data in hdf5 file at beginning of running
  ## Vicinal distribution settings ----------------------------------------------------------------------------
  parser.add_argument('--steps', type=int, default=5, 
    help="Number of 'steps' to take between images in generating the vicinal distribution")
  ## Triplet manager settings ---------------------------------------------------------------------------------
  parser.add_argument('--n_triplets', type=int, default=5)
  parser.add_argument('--img_rel_path', type=str, default=None)
  ## Analysis settings ----------------------------------------------------------------------------------------
  parser.add_argument('--aggregate', '--agg', default=None, choices=['group', 'class', 'all'])
  # Process Arguments =========================================================================================
  args = parser.parse_args()
  if not args.save_name.endswith("hdf5"):
    args.save_name = args.save_name + ".hdf5"
  return args
  