"""
Preliminary checks:
(1) You have a folder ending in '_data' in the same folder as this file with all the water-splitting data
(2) Edit your bash profile to support the moe and ga_optimization_ternary modules by writing:
    # for GA
    export PYTHONPATH="[insert pwd to ga_optimization_ternary directory]:$PYTHONPATH"

    # for MOE
    export PYTHONPATH="[insert pwd to MOE directory]:$PYTHONPATH"

    (without the brackets)

"""

import math
import random
import json
import numpy as np
import os

from moe.easy_interface.experiment import Experiment
from moe.easy_interface.simple_endpoint import gp_next_points
from moe.optimal_learning.python.data_containers import SamplePoint
from ga_optimization_ternary.fitness_evaluators import eval_fitness_simple, eval_fitness_complex_product
from tools import decode
from pymatgen.core.periodic_table import Element, symbol_from_Z


#results from water-splitting paper
results_bank = ["LiVO3", "NaSbO3", "MgTaO2N", "CaGeO3", "CaSnO3", "CaTaO2N", "SrGeO3", "SrSnO3", "SrTaO2N", "YTaON2", "AgNbO3", "SnTiO3", "CsNbO3", "BaGaO2F", "BaInO2F", "BaSnO3", "BaTaO2N", "LaTiO2N", "LaTaON2", "PbGaO2F"]

bank = np.zeros((1000,4))
sorted_bank = np.zeros((1000,4))
symbol_bank  = []


def run_example(num_points_to_sample=1000, verbose=True, **kwargs):
    """Run the example, asking MOE for ``num_points_to_sample`` optimal points to sample."""

    exp = Experiment([[1, 52], [0, 6], [1, 52]])  # 2D experiment, we build a tensor product domain
    # Bootstrap with some known or already sampled point(s)
    exp.historical_data.append_sample_points([
        SamplePoint([26, 2, 46], get_fitness([26, 2, 35]), 0.5),  # Iterables of the form [point, f_val, f_var] are also allowed
        ])
    # Sample num_points_to_sample points
    for i in range(num_points_to_sample):
        # Use MOE to determine what is the point with highest Expected Improvement to use next
        next_point_to_sample = map(round, gp_next_points(exp, **kwargs)[0])  # in [A, X, B] form, rounded integers
        value_of_next_point = get_fitness(next_point_to_sample)

        if verbose:
            if in_results(next_point_to_sample):
                print '***', "Sampled f({0:s}) = {1:.18E}".format(str(next_point_to_sample), value_of_next_point), '***'
            else:
                print "Sampled f({0:s}) = {1:.18E}".format(str(next_point_to_sample), value_of_next_point)

        bank[i,0:3] = next_point_to_sample
        bank[i,3]  = value_of_next_point
        # Add the information about the point to the experiment historical data to inform the GP
        exp.historical_data.append_sample_points([SamplePoint(next_point_to_sample, value_of_next_point, 0.01)])  # We can add some noise


def json_get(name, key):
    """Gets the json file with the name inputted into this function by looking in all directories ending in '_data'. """
    cmpd_file = name + '.json'
    data_dirs = [dir for dir in os.listdir('.') if dir.endswith('_data')]
    dir = data_dirs[0]
    for fname in os.listdir(dir):
        if fname.endswith(name + '.json'):
            with open(os.path.join(dir,fname)) as f:
                data = json.load(f)
                return data[key]

def get_fitness(compound):
    """Computes the fitness of a compound, and returns the negative of it (for function-minimizing)."""
    #get inputs to fitness function:
    cmpd_name = decode(compound) #finds the name of the compound corresponding to next_point_to_sample
    #then query for JSON file with same name
    return 0 - eval_fitness_complex_product(json_get(cmpd_name, 'gllbsc_dir-gap'), json_get(cmpd_name, 'gllbsc_ind-gap'), json_get(cmpd_name, 'heat_of_formation_all'), json_get(cmpd_name, 'VB_dir'), json_get(cmpd_name, 'CB_dir'), json_get(cmpd_name, 'VB_ind'), json_get(cmpd_name, 'CB_ind'))

def in_results(compound):
    """Returns a boolean based on whether a compound is in the results_bank."""
    name = decode(compound)
    return (name in results_bank)

def bank_sorter(bank):
    """Sorts bank of tested compounds by fitness and returns all tested compounds and the matches to results_bank."""
    keys = np.argsort(bank[:,-1])
    for j in range(len(bank)):
        # sort the paramterized vectors
        sorted_bank[j,:] = bank[keys[j],:]

        # call decoder and get symbol
        symbol_bank.append(decode(sorted_bank[j,0:3]))
        final_bank = [name for name in symbol_bank if (name in results_bank)]
    symbol_bank_select = symbol_bank[0:50]
    return "all tested = " + str(symbol_bank_select), "matches = " + str(final_bank)

if __name__ == '__main__':
    run_example()
    print bank_sorter(bank)

