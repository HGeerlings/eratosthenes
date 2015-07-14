import json
from pymatgen.core.periodic_table import Element, symbol_from_Z
import numpy as np

def decode(compound): 
    """Decodes a [A, X, B] compound and returns its name as a string"""

    all_Z = [3, 4, 5, 11, 12, 13, 14, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 55, 56, 57, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83]
    idx_to_Z_dict = dict(zip(range(1, 53), all_Z)) # Expand 1-52 domain into all possible Z values

    Za = idx_to_Z_dict[compound[0]]        
    A = str(symbol_from_Z(Za))

    Zb = idx_to_Z_dict[compound[2]]
    B = str(symbol_from_Z(Zb))

    if compound[1] == 0:
        X3 = "O3"
    elif compound[1] == 1:
        X3 = "O2N"
    elif compound[1] == 2:
        X3 = "ON2"
    elif compound[1] == 3:
        X3 = "N3"
    elif compound[1] == 4:
        X3 = "O2F"
    elif compound[1] == 5:
        X3 = "OFN"
    elif compound[1] == 6:
        X3 = "O2S"

    return A+B+X3




