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
	print('in fucntion', len(bank), neigh_idx)
	return neigh_idx, neigh_coord

# calculate objective function of 2D coordinate 'x'
kg_des = 5
def f(x):
	# this function must also decode the SNE dataset into bulk dataset
	kg_x = vect_to_mat_dict[tsne_to_vect_dict[tuple(x)]]['elasticity.K_VRH']/vect_to_mat_dict[tsne_to_vect_dict[tuple(x)]]['elasticity.G_VRH']

	if kg_x >= 5:
		obj = 1
	else:
		obj = 0
	return obj, kg_x


#### start actual searching

# allocate arrays 
good_formula = []
good_dict = []
keys = ['Formula', 'K/G Ratio']
num_good =5
iters = 0

# generate random starting point in SNE dataset
current_idx = np.random.randint(len(bank))
current_coord = tuple(bank[current_idx])

while len(good_dict) < num_good:
	
	[neigh_idx, neigh_coord] = get_neighbor(current_coord, bank)
	print('neighbor', current_idx, neigh_idx)

	[f_current, kg_current] = f(current_coord)
	[f_neighbor, kg_neighbor] = f(neigh_coord)

	if f_neighbor == 1:
		[current_coord, f_current, kg_current] = [neigh_coord, f_neighbor, kg_neighbor]
		print('bank', len(bank), current_idx)
		del bank[current_idx]

		# check if deleting current coord will create void in indexing list  when jumping to neighbor, if neighbor index is smaller, void will be irrelevant
		if neigh_idx > current_idx:
			current_idx = neigh_idx - 1
		else:
			current_idx = neigh_idx

	elif f_neighbor == 0: 
		# as you idle at a current point and bad neighbors are being deleted, this adjusts the current coord index to keep up with changing size of data bank
		if neigh_idx < current_idx:
			current_idx = current_idx - 1
		del bank[neigh_idx]

	if f_current == 1:
		pretty = vect_to_mat_dict[tsne_to_vect_dict[tuple(current_coord)]]['pretty_formula']
		if not any(pretty in x for x in good_formula):
			good_dict.append(dict(zip(keys, [pretty, kg_current])))
			good_formula.append(pretty)
		else:
			print 'Repeat Detected!'
			current_idx = np.random.randint(len(bank))
			current_coord = tuple(bank[current_idx])
	iters += 1

print good_dict
print iters








