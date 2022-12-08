#!/usr/bin/env python3
import argparse
import time
from library import estimate_pi

def main():
    parser = argparse.ArgumentParser(description="Monte Carlo Pi Estimatator (mpi4py)")
    parser.add_argument("-n", type=int, default=20_000_000, help="number of samples")
    args = parser.parse_args()

    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    
    n = args.n
    p = comm.size

    comm.barrier()
    start = time.time()
    estimate_pi(n // p)
    comm.barrier()
    end = time.time()
    
    if comm.rank == 0:
    print(f"Elapsed time: {end - start}")

if __name__ == "__main__":
    main()

