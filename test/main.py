import sys
sys.path.append('../')
from src import args
from run_analysis import run_analysis
from run_generation import run_generation

def main(args):
    """ Runs generation and analysis steps back-to-back. """
    run_generation(args)
    run_analysis(args)

if __name__ == "__main__":
    parser = args.CustomParser(mode='Complete')
    main(parser.parse_args())