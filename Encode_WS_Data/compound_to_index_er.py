
import os 
import json
import numpy as np
from pymatgen.core.periodic_table import Element

# Code adapted from A. Jain, LBL 2012

# This script must be run within a directory that also contains 
# the 'ivano_perovskite_data' folder

# compress Z numbers into 1-52 domain
def compress():
    all_Z = [3, 4, 5, 11, 12, 13, 14, 19, 20, 21, 22, \
    23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 37, 38, \
    39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, \
    55, 56, 57, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, \
    82, 83]
    Z_to_idx_dict = dict(zip(all_Z, range(1,53)))
    
    return Z_to_idx_dict


# read through all 18928 json files and encode compounds into [A X3 B] parameterization:
def encode(Z_to_idx_dict, dir=None):   
    compound_bank = np.zeros((18928,3))
    counter = 0
    if not dir:
        data_dirs = [dir for dir in os.listdir('.') if dir.endswith('_data')]
        if len(data_dirs) == 1:
            dir = data_dirs[0]
        else:
            raise ValueError("Multiple '_data' directories. Specify path.")
    for fname in os.listdir(dir):
        if fname.endswith('.json'):
            with open(os.path.join(dir,fname)) as f:
                data = json.loads(f.read())
                compound_vector = [Z_to_idx_dict[Element(data['A']).Z], data['anion_idx'], Z_to_idx_dict[Element(data['B']).Z]]
                compound_bank[counter,:] = compound_vector
                counter += 1

    return compound_bank
              
def call():                
    Z_to_idx_dict = compress()
    compound_bank = encode(Z_to_idx_dict)  
         
    return compound_bank
    



