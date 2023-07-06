from argparse import ArgumentParser

#classes = {"COVID_positive":['Yes','No']}
#subgroup_attributes = {"sex":['F','M']}
#tasks = {"COVID_positive":{1:'Yes',0:'No'}}

class CustomParser():
  def __init__(self, mode:str):
    """
    A custom argument parser.
    
    Parameters
    ----------
    mode : str
        The purpose for which the parser is being created; must be 'Analyze', 'Complete', or 'Generate'.
    
    
    """
    modes = {'Analyze','Complete', 'Generate'}
    if mode not in modes:
      raise ValueError(f"mode must be one of {modes}")
    self.parser = ArgumentParser()
    # # Arguments that are always used
    self.parser.add_argument('--save_loc', '--save-loc', type=str, required=True)
    self.parser.add_argument('--save_name', '--save-name', type=str, default='decision_regions')
    self.parser.add_argument('--classes', nargs="+", required=True)
    self.parser.add_argument('--class_order', default='0,1', choices=['0,1','1,0'])
    self.parser.add_argument('--subgroup_attributes', nargs="+", required=True)
    
    if mode == 'Generate' or mode == 'Complete':
      ## Arguments used to generate and evaluate vicinal distributions ------------------------------------------
      self.parser.add_argument('--model_file', type=str, required=True)
      self.parser.add_argument('--data_csv', type=str, required=True)
      self.parser.add_argument('--batch_size', type=int, default=5)
      self.parser.add_argument('--overwrite', action='store_true', default=False) # NOTE: will delete all data in hdf5 file at beginning of running
      self.parser.add_argument('--steps', type=int, default=5, 
        help="Number of 'steps' to take between images in generating the vicinal distribution")
      self.parser.add_argument('--n_triplets', type=int, default=5)
      self.parser.add_argument('--img_rel_path', type=str, default=None)
    if mode == 'Analyze' or mode == 'Complete':
      ## Arguments used to perform decision region analysis -----------------------------------------------------
      self.parser.add_argument('--out_function', type=str, default=None)
      self.parser.add_argument('--aggregate', '--agg', default=None, choices=['group', 'class', 'all'])
      ### Plotting arguments
      self.parser.add_argument('--plot', default=None, choices=['composition', 'performance'])
      self.parser.add_argument('--show', default=False, action='store_true')
      self.parser.add_argument('--display-only', dest='display_only', default=False, action='store_true') # Don't save plots (+ other outputs?)
      self.parser.add_argument('--hide-percent', dest='show_percent', default=True, action='store_false')
      self.parser.add_argument('--hide-errorbar', dest='show_errorbar', default=True, action='store_false')
  
  def parse_args(self):
    args = self.parser.parse_args()
    if not args.save_name.endswith("hdf5"):
      args.save_name = args.save_name + ".hdf5"
    args.classes = {c.split(":")[0]:c.split(":")[-1].split(",") for c in args.classes}
    args.subgroup_attributes = {s.split(":")[0]:s.split(":")[-1].split(",") for s in args.subgroup_attributes}
    args.class_order = args.class_order.split(",")
    args.tasks = {}
    for c in args.classes:
      args.tasks[c] = {float(args.class_order[i]):args.classes[c][i] for i in range(len(args.classes[c]))}
    return args
  