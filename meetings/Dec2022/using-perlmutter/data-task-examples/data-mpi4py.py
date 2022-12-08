#!/usr/bin/env python

import argparse
import time

import numpy as np
from tqdm import tqdm

def process_data(i, a):
    w, v = np.linalg.eigh(a)
    return i, w


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, default=1000)
    parser.add_argument('--ntasks', type=int, default=128)
    args = parser.parse_args()
    n = args.n
    ntasks = args.ntasks

    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank = comm.rank
    size = comm.size

    if rank == 0:
        print(f'mpi4py')
        print(f'{n=} {ntasks=} {size=}')

        # create a random set of data
        data = list()
        for i in range(ntasks):
            np.random.seed(i)
            b = np.random.rand(n, n)
            a = b.dot(b.T)
            data.append(a)
    else:
        data = None

    start = time.time()

    # bcast data from root MPI rank
    data = comm.bcast(data, root=0)

    results = []

    # each mpi rank only processes a subset of the data
    # the range is offset by each process mpi rank
    # and uses a step equal to the size of the communicator
    # For example, with 2 MPI ranks and 5 data tasks
    # each MPI rank will process the following indices
    # rank 0: [0, 2, 4]
    # rank 1: [1, 3]
    for i in range(rank, ntasks, size):
        result = process_data(i, data[i])
        results.append(result)

    # gather results to root MPI rank
    results = comm.gather(results, root=0)

    if rank == 0:
        end = time.time()
        elapsed = end - start
        rate = ntasks / elapsed
        print(f'Processed {ntasks} tasks in {elapsed:.2f}s ({rate:.2f}it/s)')

        # flatten list of lists
        results = [r for sub in results for r in sub]

        # check results
        if {r[0] for r in results} == set(range(ntasks)):
            print(f'completed all tasks!')
        else:
            print('uh oh, something went wrong.')
