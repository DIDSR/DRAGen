import sys
import numpy as np


def sigmoid(l):
    return 1/(1+np.exp((-l)))

output_functions = {
    'sigmoid':sigmoid,
    None:None
}

def progressbar(iterable, prefix="", out=sys.stdout, sym='#', length=60):
    num = len(iterable)
    sym = sym*int(length/num)
    alt_sym = '.'*int(length/num)
    for i, item in enumerate(iterable):
        yield item
        print(f"[{prefix}{sym*i}{alt_sym*(num-i)}] {i}/{num}", end='\r',file=out,flush=True)
    print(f"[{prefix}{sym*num}] {num}/{num}", end='\r',file=out,flush=True)
    print("", file=out,flush=True)

def verify_type_or_none(argument, arg_type, arg_name:str):
    none_options = {None, 'None', 'none'}
    if argument in none_options:
        return None
    try:
        return arg_type(argument)
    except:
        raise ValueError(f"Unrecognized value {argument} for {arg_name}; must be type {arg_type} or None.")
        