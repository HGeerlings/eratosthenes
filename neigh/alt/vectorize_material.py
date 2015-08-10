import numpy as np
import random

def vectorize_random(n):
    def with_length_of(lst):
        return np.array(
            [np.array([random.gauss(0, 1) for _ in xrange(n)])
             for _ in xrange(len(lst))])
    return with_length_of
