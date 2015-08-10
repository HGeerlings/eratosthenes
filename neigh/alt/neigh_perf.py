"""Playing around with a more performant implementation of t-SNE."""


import logging
import pickle

from pymatgen import MPRester
from tsne import bh_sne

from plot_tsne import plot_tsne
from vectorize_material import vectorize_random

# Set up streaming log to console with formatting
_log = logging.getLogger('neigh_perf')
_log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
_log.addHandler(ch)

def get_materials_list():
    """Fetch data (from local cache if available)."""
    try:
        _log.info('Trying data cache for materials')
        with open('materials_list.pickle') as f:
            return pickle.load(f)

    except IOError:
        _log.info('Fetching remote data')
        m = MPRester()
        materials_list = m.query(
            criteria={"elasticity": {"$exists": True}},
            properties=['pretty_formula', 'reduced_cell_formula', 'task_id',
                        "elasticity.K_VRH", "elasticity.K_VRH", 'volume',
                        'density', 'formation_energy_per_atom', 'nsites'])
        # Save for later
        with open('materials_list.pickle', 'w') as f:
            pickle.dump(materials_list, f)
        _log.info('Data loaded')
        return materials_list

def get_tsne_mapping(materials_list=None):
    if materials_list is None:
        # Doesn't call get_materials_list() when module is loaded
        materials_list = get_materials_list()
    try:
        _log.info('Trying data cache for t-SNE mapping')
        with open('tsne_points.pickle') as f:
            _log.info('Using pickled t-SNE points')
            return pickle.load(f)
    except IOError:
        X = vectorize_random(4)(materials_list)
        X_2d = bh_sne(X)
        _log.info('t-SNE plot at {}'.format(plot_tsne(X_2d)))
        point_map = [{'pt': pt, 'material': m} for pt, m in
                     zip(X_2d, materials_list)]
        with open('tsne_points.pickle', 'w') as f:
            pickle.dump(point_map, f)
        return point_map

if __name__ == "__main__":
    get_tsne_mapping()
