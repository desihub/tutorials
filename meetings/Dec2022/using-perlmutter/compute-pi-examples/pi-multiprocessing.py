#!/usr/bin/env python3
import argparse
import time
import multiprocessing as mp

from library import estimate_pi


def main():
    parser = argparse.ArgumentParser(
        description="Monte Carlo Pi Estimatator (threading)"
    )
    parser.add_argument("-n", type=int, default=20_000_000, help="number of samples")
    parser.add_argument("-p", type=int, default=4, help="number of parallel processes")
    args = parser.parse_args()

    n = args.n
    p = args.p

    if n % p != 0:
        print(f"Warning: {n=} is not evenly divisble by {p=}")

    mp.set_start_method("spawn")
    start = time.time()
    with mp.Pool(processes=p) as pool:
        results = pool.map(estimate_pi, [n//p] * p)
    end = time.time()

    print(f"Elapsed time: {end - start}")

if __name__ == "__main__":
    main()


