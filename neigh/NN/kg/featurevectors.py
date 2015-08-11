
### FEATURE VECTORS ###

"""
From Wei's paper, we know natural log of volume (lnV), energy per atom (Ec), 
elemental weighted average of atomic number (AlnZ), and elemental weighted 
std deviation of electronegativity (SX) correlate relatively strongly to
bulk modulus (K).

Feature vectors that utilize these correlations will aid in predicting 
bulk moduli of materials.

We eventually want to reduce these vectors to 2D. We will try every 
combination of features in vectors from 1-4 dimensions.

Hypothesis: 4D vector with all correlations will perform the best
"""

import os
import numpy as np
from pymatgen.core.periodic_table import Element
from pymatgen import MPRester
from math import log

def element_lister(material):
	element_list = []
	for element in material['reduced_cell_formula']:
		for i in range(int(material['reduced_cell_formula'][element])):
			element_list += [element]
	return element_list

def get_ln_volume(material, elem_list):
	return log(material['volume']/material['nsites'])

def get_c_energy_per_atom(material, elem_list):
	energy_per_atom = material['formation_energy_per_atom']
	total_energy = energy_per_atom*len(elem_list)
	return total_energy

def get_avg_Z_num(material, elem_list):
	Z_list = []
	for element in elem_list:
		Z_list += [log(Element(element).Z)]
	return np.average(Z_list)

def get_sd_X(material, elem_list):
	X_list = []
	for element in elem_list:
		X_list += [log(Element(element).X)]
	return np.std(X_list)

key = os.environ['MAPI_KEY']
m = MPRester(key)	

materials_list = m.query(criteria={"elasticity": {"$exists": True}}, properties=['pretty_formula', 'reduced_cell_formula', "elasticity.K_VRH", "elasticity.G_VRH", 'volume', 'density', 'formation_energy_per_atom', 'formation_energy_per_atom', 'nsites'])


def vectorize_and_catalog(materials):
	vector_list = []
	catalog = {}
	for material in materials:
		element_list = element_lister(material)
		vector = [get_ln_volume(material, element_list), get_c_energy_per_atom(material, element_list), get_avg_Z_num(material, element_list), get_sd_X(material, element_list)]
		vector_list += [vector]
		catalog[tuple(vector)] = material
	return vector_list, catalog

def vector_to_material(vector):
	return catalog[tuple(vector)]


def normalize_vectors(vector_list):
	vector_array = np.array(vector_list)
	mean_each_column = np.mean(vector_array, axis=0)
	std_each_column = np.std(vector_array, axis=0)
	for i in range(len(vector_array)):
		difference_from_mean = np.subtract(vector_array[i], mean_each_column)
		vector_array[i] = np.divide(difference_from_mean, std_each_column)
	return vector_array








