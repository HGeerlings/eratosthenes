"""Interface to SigOpt for Perovskite data set and fitness evaluation.

SigOpt Experiment Detail (via sigopt_expt.fetch()):

{u'metric': {u'name': u'smooth product of E_g, H_f, and band edges'},
 u'name': u'Water-splitting perovskites',
 u'parameters': [{u'bounds': {u'max': 52.0, u'min': 1.0},
   u'name': u'A',
   u'tunable': True,
   u'type': u'int'},
  {u'bounds': {u'max': 52.0, u'min': 1.0},
   u'name': u'B',
   u'tunable': True,
   u'type': u'int'},
  {u'categorical_values': [{u'enum_index': 1, u'name': u'O3'},
    {u'enum_index': 2, u'name': u'O2N'},
    {u'enum_index': 3, u'name': u'ON2'},
    {u'enum_index': 4, u'name': u'N3'},
    {u'enum_index': 5, u'name': u'O2F'},
    {u'enum_index': 6, u'name': u'O2S'},
    {u'enum_index': 7, u'name': u'OFN'}],
   u'name': u'X3',
   u'tunable': True,
   u'type': u'categorical'}],
 u'type': u'offline'}

Example interactive usage:
>>> from perov_sigopt.observe import *
>>> assignments = get_assignments()
>>> e = Evaluator()
>>> value = e.evaluate(assignments)
>>> send_report(assignments, value)
"""

import logging
import os

from pymatgen.core import periodic_table
from pymongo import MongoClient
import sigopt.interface

from ga_optimization_ternary import fitness_evaluators

exptnum = os.environ['SIGOPT_EXPT']
logging.basicConfig(filename='sigopt-expt-{}.log'.format(exptnum),
                    level=logging.INFO)
_log = logging.getLogger("erato." + __name__)

sigopt_conn = sigopt.interface.Connection(
    client_token=os.environ['SIGOPT_CLIENTTOKEN'],
    user_token=os.environ['SIGOPT_USERTOKEN'])
sigopt_expt = sigopt_conn.experiments(int(exptnum))

class Evaluator:
    def __init__(self, evaluator='eval_fitness_complex_product',
                 db_name='unc', coll_name='data_raw'):
        self._db_coll = get_db_collection(db_name, coll_name)
        self._fn = getattr(fitness_evaluators, evaluator)

    def evaluate(self, assignments):
        """Return larger values for better assignments."""
        value = self._fn(*get_data(assignments, self._db_coll))
        _log.info('Got value {} for {}'.format(value, assignments))
        return value

    def fetch_and_report(self):
        assignments = get_assignments()
        value = self.evaluate(assignments)
        send_report(assignments, value)

def get_assignments():
    """Fetches parameters that *maximize* a metric.
    """
    response = sigopt_expt.suggest()
    assignments = response.suggestion.assignments
    _log.info('Got assignents {} from SigOpt'.format(assignments))
    return assignments

def send_report(assignments, value):
    """Send the result of Evaluator.evaluate() to SigOpt."""
    sigopt_expt.report(data={'assignments': assignments, 'value': value})
    _log.info('Sent value {} for {} to SigOpt'.format(value, assignments))

def get_db_collection(db_name, coll_name):
    port = int(os.environ.get('LOCAL_MONGO_PORT', 27017))
    client = MongoClient('localhost', port)
    db = getattr(client, db_name)
    return getattr(db, coll_name)

def get_data(assignments, db_coll):
    params = assignments
    spec = params_to_db_spec(params)
    result = db_coll.find_one(spec)
    _log.info("Fetched {}->{} from db".format(params, spec))
    props = ['gllbsc_dir-gap', 'gllbsc_ind-gap', 'heat_of_formation_all',
             'VB_dir', 'CB_dir', 'VB_ind', 'CB_ind']
    return [result[p] for p in props]

idx_range = range(1,53)
used_Zs = [ 3,  4,  5, 11, 12, 13, 14, 19, 20, 21,
           22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
           32, 33, 37, 38, 39, 40, 41, 42, 44, 45,
           46, 47, 48, 49, 50, 51, 52, 55, 56, 57,
           72, 73, 74, 75, 76, 77, 78, 79, 80, 81,
           82, 83]
symbol_for = list(periodic_table.all_symbols())
symbol_for.insert(0, None) # One-based indexing for Z
eltidx_sym = dict(zip(idx_range, [symbol_for[Z] for Z in used_Zs]))
anion_idx = {"O3": 0, "O2N": 1, "ON2": 2, "N3": 3, "O2F": 4, "OFN": 5, "O2S": 6}

def params_to_db_spec(params):
    """Map sigopt param space to a db query spec."""
    return {'A': eltidx_sym[params['A']],
            'B': eltidx_sym[params['B']],
            'anion_idx': anion_idx[params['X3']]}

if __name__ == "__main__":
    import sys
    import time

    e = Evaluator()
    while True:
        e.fetch_and_report()
        time.sleep(5) # Simulate expensive function evaluation
