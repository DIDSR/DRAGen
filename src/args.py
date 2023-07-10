from argparse import ArgumentParser
from src.utils import verify_type_or_none

#classes = {"COVID_positive":['Yes','No']}
#subgroup_attributes = {"sex":['F','M']}
#tasks = {"COVID_positive":{1:'Yes',0:'No'}}

class CustomParser():
  """
  A custom argument parser.
  
  Parameters
  ----------
  mode
      The purpose for which the parser is being created; must be 'Analyze', 'Complete', or 'Generate'.
  
  Raises
  ======
  ValueError
    mode value is not 'Analyze', 'Complete', or 'Generate'.
  """
  def __init__(self, mode:str):
    modes = {'Analyze','Complete', 'Generate'}
    if mode not in modes:
      raise ValueError(f"mode must be one of {modes}")
    self.mode = mode
    self.parser = ArgumentParser()
    # # Arguments that are always used
    self.parser.add_argument('--save_loc', '--save-loc', type=str, required=True)
    self.parser.add_argument('--save_name', '--save-name', type=str, default='decision_regions')
    self.parser.add_argument('--classes', nargs="+", required=True)
    self.parser.add_argument('--class_order', default='0,1', choices=['0,1','1,0'])
    self.parser.add_argument('--subgroup_attributes', nargs="+", required=True)
    self.parser.add_argument('--overwrite', action='store_true', default=False) # NOTE: will delete all data in hdf5 file at beginning of running if generating
    if mode == 'Generate' or mode == 'Complete':
      ## Arguments used to generate and evaluate vicinal distributions ------------------------------------------
      self.parser.add_argument('--model_file', type=str, required=True)
      self.parser.add_argument('--data_csv', type=str, required=True)
      self.parser.add_argument('--batch_size', type=int, default=5)
      self.parser.add_argument('--steps', type=int, default=5, 
        help="Number of 'steps' to take between images in generating the vicinal distribution")
      self.parser.add_argument('--n_triplets', type=int, default=5)
      self.parser.add_argument('--img_rel_path', type=str, default=None)
    if mode == 'Analyze' or mode == 'Complete':
      ## Arguments used to perform decision region analysis -----------------------------------------------------
      self.parser.add_argument('--out_function', type=str, default=None)
      self.parser.add_argument('--aggregate', '--agg', default=None, choices=['group', 'class', 'all'])
      ### Plotting arguments
      self.parser.add_argument('--plot', default=None, choices=['composition', 'performance', 'region'])
      self.parser.add_argument('--show', default=False, action='store_true')
      self.parser.add_argument('--display-only', dest='save_plot', default=True, action='store_false') # Don't save plots (+ other outputs?)
      self.parser.add_argument('--hide-percent', dest='show_percent', default=True, action='store_false')
      self.parser.add_argument('--hide-errorbar', dest='show_errorbar', default=True, action='store_false')
      self.parser.add_argument("--save_dpi", "--save-dpi", default=800, type=int, help="dpi used when saving summary plots.")
      self.parser.add_argument("--plot_output_format","--plot-output-format", default=[], nargs='+',
        help="Output formats in which the plots should be saved.")
      self.parser.add_argument("--plot_palette",'--plot-palette', type=str, default="Set2",
        help="Color palette to be used during plotting, can be either a matplotlib colorpalette or a custom palette.")
      #### Only used with plot == 'region
      self.parser.add_argument("--plot_threshold", "--plot-threshold", default=None,
        help="Threshold applied to ouput scores in 'region' plots; if None, no threshold is applied.")
      self.parser.add_argument("--n_per_group", '--n-per-group', default=None,
        help="Number of decision regions to plot per group if plot = 'region'; if None, all decision regions are plotted.")
  
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
    if self.mode != 'Generate':
      args.plot_threshold = verify_type_or_none(args.plot_threshold, float, arg_name="--plot-threshold/--plot_threshold")
      args.n_per_group = verify_type_or_none(args.n_per_group, int, "--n-per-group/--n_per_group")
      args.plot_output_format = list(set(args.plot_output_format))
      if len(args.plot_output_format) == 0:
        args.plot_output_format = ['png']
      if ":" in args.plot_palette:
        args.plot_palette = {c.split(":")[0]:c.split(":")[-1] for c in args.plot_palette.split(",")}
      elif ',' in args.plot_palette:
        args.plot_palette = args.plot_palette.split(",")
    return args
  