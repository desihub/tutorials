#!/usr/bin/env python

import argparse
import itertools
import multiprocessing
import os

import numpy as np
from tqdm import tqdm


def process_data(i, a):
    w, v = np.linalg.eigh(a)
    return i, w

def _process_data_unpack(args):
    # helper function for unpacking args
    return process_data(*args)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, default=1000)
    parser.add_argument('--ntasks', type=int, default=128)
    parser.add_argument('--nproc', type=int, default=None)
    args = parser.parse_args()
    n = args.n
    ntasks = args.ntasks
    nproc = args.nproc

    # if nproc is not specified, use the number of physical cores
    if nproc is None:
        # sched_getaffinity returns number of logical cores
        # divide by two to get number of physical cores
        cpus = os.sched_getaffinity(0)
        nproc = len(cpus) // 2 

    print('multiprocessing')
    print(f'{n=} {ntasks=} {nproc=}')

    # create a random set of data
    data = list()
    for i in range(ntasks):
        np.random.seed(i)
        b = np.random.rand(n, n)
        a = b.dot(b.T)
        data.append(a)

    results = []
    # We advise using the "spawn" start method at NERSC
    # See the following page for more multiprocessing tips:
    # https://docs.nersc.gov/development/languages/python/parallel-python/#tips-for-using-multiprocessing-at-nersc
    multiprocessing.set_start_method("spawn")
    # create a pool of nproc workers
    with multiprocessing.Pool(processes=nproc) as pool:
        tasks_args = enumerate(data)
        # typically you would then use pool.starmap like so:
        #    results = pool.starmap(process_data, tasks_args)
        # which would be a lot simpler.
        # Here I'm using pool.imap with a helper function to unpack task_args
        # in order to use a progress bar for visualization
        it = pool.imap(_process_data_unpack, tasks_args)
        for result in tqdm(it, total=ntasks, ncols=80):
            results.append(result)

    # check results
    if {r[0] for r in results} == set(range(ntasks)):
        print(f'completed all tasks!')
    else:
        print('uh oh, something went wrong.')

if __name__ == "__main__":
    main()