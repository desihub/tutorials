#!/usr/bin/env python3
import argparse
from threading import Thread
import time

from library import estimate_pi


def main():
    parser = argparse.ArgumentParser(
        description="Monte Carlo Pi Estimatator (threading)"
    )
    parser.add_argument("-n", type=int, default=20_000_000, help="number of samples")
    parser.add_argument("-p", type=int, default=4, help="number of parallel threads")
    args = parser.parse_args()

    n = args.n
    p = args.p

    if n % p != 0:
        print(f"Warning: {n=} is not evenly divisble by {p=}")

    import threading

    # Define a wrapper function that appends results from individual threads
    # to a shared (nonlocal) list in the main thread
    results = []
    def estimate_pi_wrapper(n):
        nonlocal results
        start = time.time()
        results.append(estimate_pi(n))
        end = time.time()
        print(f"{threading.current_thread().getName()} Elapsed time: {end - start}")

    # Create threads that will perform portion of calculation
    t = [Thread(target=estimate_pi_wrapper, args=(n // p,)) for i in range(p)]

    start = time.time()
    # Start threads
    [t[i].start() for i in range(p)]
    # Wait for threads to complete
    [t[i].join() for i in range(p)]
    end = time.time()

    print(f"Elapsed time: {end - start}")


if __name__ == "__main__":
    main()
