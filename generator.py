%%writefile generator.py

from typing import Any, List, Union
import sys
import os
import time
import random
import pickle
import gzip
import numpy as np
import tensorflow as tf
from humanize import naturalsize, precisedelta, intcomma


# https://github.com/JamesMcGuigan/kaggle-digit-recognizer/blob/master/src/random/random_seed_search.py
def get_randoms(length, seed, method='random') -> Union[List[int],np.ndarray]:
    if method == 'random':
        random.seed(seed)        
        return [ random.randint(0,2) for n in range(length) ]
    if method == 'np':
        np.random.seed(seed)
        return np.random.randint(0,2, length)
    if method == 'tf':
        tf.random.set_seed(seed)
        return tf.random.uniform((length,), minval=0, maxval=3, dtype=tf.dtypes.int32).numpy()
    
    
# NOTE: state space = filesize = 3**window
def generate_random_sequence_table(timeout=8.8*60*60, window=10, numbers_per_seed=1000, method='random', lookup=None):
    time_start = time.perf_counter()
    lookup     = lookup or {}  # pickle breaks if given defaultdict()
    count      = 0
    for seed in range(sys.maxsize):
        if time.perf_counter() - time_start > timeout: break
        numbers = get_randoms(numbers_per_seed, seed=seed, method=method)
        for n in range(len(numbers)-window-1):
            sequence    = tuple(numbers[n:n+window])
            next_number = int(numbers[n+window])                
            if sequence not in lookup: lookup[sequence] = [0,0,0]  
            lookup[sequence][next_number] += 1
            count                         += 1

    time_taken = time.perf_counter() - time_start
    print(f'{intcomma(count)} samples / {intcomma(len(lookup))} sequences' + 
          f' = {count/len(lookup):.1f} samples/sequences' + 
          f' = {100*len(lookup)/(3**window):.0f}% ' +
          f'in {precisedelta(time_taken)}')
    
    return lookup


if __name__ == '__main__':
    timeout = 1*60*60 if os.environ.get('KAGGLE_KERNEL_RUN_TYPE','') != 'Interactive' else 12

    # lookup = base64_file_load('../input/rock-paper-scissors-rng-statistics/random_sequence.base64')
    lookup = generate_random_sequence_table(timeout=timeout)
    base64_file_save(lookup, './random_sequence.base64')        