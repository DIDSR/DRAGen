import sys
sys.path.append('../')
from src import args
from src.utils import output_functions
from src.composition_analysis import plot_figures, get_compositions, save_compositions

def run_analysis(args):
    """ Calculates decision region compositions and plots results """
    decision_region_file = f"{args.save_loc}/{args.save_name}"
    decision_region_compositions = get_compositions(decision_region_file, tasks=args.tasks, output_function=output_functions[args.out_function], aggregate=args.aggregate)
    save_compositions(compositions=decision_region_compositions, save_loc=args.save_loc, overwrite=args.overwrite, aggregate=args.aggregate)
    if args.plot:
        plot_figures(df=decision_region_compositions, plot=args.plot, save_loc=args.save_loc, tasks=args.tasks, palette=args.plot_palette,
            aggregate=args.aggregate, show_percent=args.show_percent, errorbar=args.show_errorbar, show=args.show,save=args.save_plot,
            save_dpi=args.save_dpi, filepath=decision_region_file, n_per_group=args.n_per_group, threshold=args.plot_threshold, output_formats=args.plot_output_format)
        

if __name__ == "__main__":
    parser = args.CustomParser(mode='Analyze')
    run_analysis(parser.parse_args())
    print("DONE")