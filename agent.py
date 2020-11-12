%%writefile agent.py

import time
import os
import random
import pickle
import gzip
from typing import Any
from humanize import naturalsize, precisedelta, intcomma


def read_gzip_pickle_file(filename: str, verbose=True) -> Any:
    time_start = time.perf_counter()
    try:
        if not os.path.exists(filename): raise FileNotFoundError
        with open(filename, 'rb') as file:
            data = file.read()
            try:    data = gzip.decompress(data)
            except: pass
            data = pickle.loads(data)
            time_taken = time.perf_counter() - time_start 
            filesize   = os.path.getsize(filename)
            if verbose: print(f'read: {filename} = {naturalsize(filesize)} in {precisedelta(time_taken)}')
    except Exception as exception:
        print('read_gzip_pickle_file()', exception)
        data = None
    return data


lookup = base64_file_load('./random_sequence.base64')
print(f'lookup = {type(lookup)} len({intcomma(len(lookup))})')
window = len(next(iter(lookup.keys())))

history = []
stats = {
    "hit":   0,
    "miss":  0,
    "total": 0,
}
def rng_statistics_agent(observation, configuration):
    global stats
    if observation.step > 0:
        history.append( observation.lastOpponentAction )
    sequence = tuple(history[-window:])
    
    if len(sequence) == window: stats['total'] += 1 
    if sequence in lookup:
        if len(sequence) == window: stats['hit'] += 1 
        weights = lookup[sequence]
        print(f"{stats['hit']:3d}/{stats['total']:3d} = {100*stats['hit']/stats['total']:3.0f}% | {sequence} = {weights}")
    else:
        if len(sequence) == window: stats['miss'] += 1 
        weights = [1,1,1]

    expected_action = random.choices( population=[0,1,2], weights=weights, k=1 )[0]
    counter_action  = ( expected_action + 1 ) % configuration.signs    
    return counter_action