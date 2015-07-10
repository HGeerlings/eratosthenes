
import os 
import json
import numpy as np
from compound_to_index_er import call
from pymatgen.core.periodic_table import Element, symbol_from_Z


# This script inputs an [n x 3] array of chemical compound encoding 
# and returns the corresponding chemical formula

#####################################################################
# Test with first twenty compounds in alphabetical order just to check
compound_bank = call()
fit_list = compound_bank[0:20,:]
#####################################################################

# Expand 1-52 domain into all possible Z values
def expand():
    all_Z = [3, 4, 5, 11, 12, 13, 14, 19, 20, 21, 22, \
    23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 37, 38, \
    39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, \
    55, 56, 57, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, \
    82, 83]
    idx_to_Z_dict = dict(zip(range(1,53), all_Z))
    
    return idx_to_Z_dict


# loop through and decode each compound vector
def decode(fit_list, idx_to_Z_dict, dir=None): 
    fit_symbols = []

    for i in range(len(fit_list)):
        Za = idx_to_Z_dict[fit_list[i,0]]        
        A = str(symbol_from_Z(Za))

        Zb = idx_to_Z_dict[fit_list[i,2]]
        B = str(symbol_from_Z(Zb))

        if fit_list[i,1] == 0:
            X3 = "O3"
        elif fit_list[i,1] == 1:
            X3 = "O2N"
        elif fit_list[i,1] == 2:
            X3 = "ON2"
        elif fit_list[i,1] == 3:
            X3 = "N3"
        elif fit_list[i,1] == 4:
            X3 = "O2F"
        elif fit_list[i,1] == 5:
            X3 = "OFN"
        elif fit_list[i,1] == 6:
            X3 = "O2S"

        fit_symbols += [A+B+X3]

    return fit_symbols


idx_to_Z_dict = expand()
fit_symbols = decode(fit_list, idx_to_Z_dict)  

print fit_symbols

             



