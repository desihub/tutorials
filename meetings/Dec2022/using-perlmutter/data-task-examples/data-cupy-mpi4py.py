#!/usr/bin/env python

import argparse
import time

import cupy as cp
import numpy as np
from tqdm import tqdm


def process_data(i, a):
    w, v = np.linalg.eigh(a)
    return i, w

def main():
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

    # have each rank select a different device
    num_devices = cp.cuda.runtime.getDeviceCount()
    cp.cuda.runtime.setDevice(rank % num_devices)

    device_pci_bus_id = cp.cuda.Device().pci_bus_id
    print(f'{rank=} {device_pci_bus_id=}', flush=True)

    comm.barrier()

    data = cp.empty((ntasks, n, n), dtype=float)

    if rank == 0:
        print('cupy-mpi4py')
        print(f'{n=} {ntasks=} {size=}')

        # create a random set of data
        for i in range(ntasks):
            cp.random.seed(i)
            b = cp.random.rand(n, n)
            a = b.dot(b.T)
            data[i] = a

    # bcast data from root MPI rank
    comm.Bcast([data, MPI.DOUBLE], root=0)

    start = time.time()

    results = []
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

if __name__ == "__main__":
    main()
