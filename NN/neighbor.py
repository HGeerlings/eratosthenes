from __future__ import division
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random

from sklearn.neighbors import NearestNeighbors
from tsne import xec

# setup kneighbors data bank for 2D coords
[bank, tsne_to_vect_dict, vect_to_mat_dict] = xec()
bank = bank.tolist()
neigh = NearestNeighbors(n_neighbors=2)

# function for retrieving nearest neighbor of 'coord' on the fly 
def get_neighbor(current_coord, bank):
	neigh.fit(bank)
	neigh_idx = neigh.kneighbors(current_coord)[1][0][1]
	neigh_coord = bank[neigh_idx]
	return neigh_idx, neigh_coord

# calculate objective function of 2D coordinate 'x'
bulk_des = 200
def f(x):
	# this function must also decode the SNE dataset into bulk dataset
	bulk_x = vect_to_mat_dict[tsne_to_vect_dict[tuple(x)]]['elasticity.K_VRH']
	obj = ((bulk_x - bulk_des)/bulk_des)**2
	return obj, bulk_x


#### start actual searching

# allocate arrays 
good_formula = []
good_dict = []
keys = ['Formula', 'Bulk Modulus']
num_good = 10
good_tol = 0.02
iters = 0

# generate random starting point in SNE dataset
current_idx = np.random.randint(len(bank))
current_coord = tuple(bank[current_idx])

while len(good_dict) < num_good:
	
	[neigh_idx, neigh_coord] = get_neighbor(current_coord, bank)

	[f_current, bulk_current] = f(current_coord)
	[f_neighbor, bulk_neighbor] = f(neigh_coord)

	if f_neighbor < f_current:
		[current_coord, f_current, bulk_current] = [neigh_coord, f_neighbor, bulk_neighbor]
		del bank[current_idx]
	else: 
		del bank[neigh_idx]

	if f_current <= good_tol:
		pretty = vect_to_mat_dict[tsne_to_vect_dict[tuple(current_coord)]]['pretty_formula']
		if not any(pretty in x for x in good_formula):
			good_dict.append(dict(zip(keys, [pretty, bulk_current])))
			good_formula.append(pretty)
		else:
			print 'Repeat Detected!'
			current_idx = np.random.randint(len(bank))
			current_coord = tuple(bank[current_idx])
	iters += 1

print good_dict
print iters








