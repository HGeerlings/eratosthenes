from __future__ import division
import numpy as np  
import matplotlib.pyplot as plt
from pymatgen import MPRester 

# import/truncate raw data (volume, density, energies, etc)
	m = MPRester("ID")
	data = m.query(criteria={"elasticity": {"$exists": True}},
                         	properties=["pretty_formula", "volume", "K_VRH"])

		# for now, import parameters and also bulk modulus (known), in future we will use parameters to select bulk moduli to be calculated

		# subfunction for formatting 


# define desired objectives and bounds/tolerances (GPa)
	tolcost = 1e-5
	kdes = 205


# define tuning/mating parameters 
	theta = 1/2
	w1 = 1


# create objective function
	cost = lambda k: w1*((kdes-k)/kdes)**2 


# randomly sample data and calculate costs


# GA
	while min(costs)>tolcost:
	
		# sort costs and store indices

		# generate offspring (using label parameter)

		# integrate into population 

		# sample some new volumes also

		# recalculate costs


####################################################


# Now do random search method and compare

# cosmetic stuff (plots, charts, etc)
