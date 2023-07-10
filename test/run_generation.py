import sys
sys.path.append('../')
from src import args
from src.decision_region_generation import generate_decision_regions

def run_generation(args):
    """ Generates decision region hdf5 file from inputs. """
    decision_region_file = f"{args.save_loc}/{args.save_name}"
    manager_args = {
        'classes':args.classes,
        'subgroup_attributes':args.subgroup_attributes,
        'triplets_per_group':args.n_triplets,
        'image_rel_path':args.img_rel_path
    }
    generate_decision_regions(input_csv_path=args.data_csv, onnx_model_path=args.model_file, output_path=decision_region_file,
        overwrite=args.overwrite, manager_kwargs=manager_args, batch_size=args.batch_size)

if __name__ == '__main__':
    parser = args.CustomParser(mode='Generate')
    run_generation(parser.parse_args()) 