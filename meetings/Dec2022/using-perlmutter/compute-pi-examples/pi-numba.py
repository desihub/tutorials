#!/usr/bin/env python3
import argparse
import time

import numba

from library import estimate_pi

# Apply numba JIT wrapper to estimate_pi function from our library
# estimate_pi will be compiled to machine code when first called
# Note not all python functions can be JIT wrapped
estimate_pi = numba.jit(estimate_pi)

def main():
    parser = argparse.ArgumentParser(description="Monte Carlo Pi Estimatator (Numba)")
    parser.add_argument("-n", type=int, default=20_000_000, help="number of samples")
    args = parser.parse_args()

    n = args.n

    estimate_pi(100)

    start = time.time()
    result = estimate_pi(n)
    end = time.time()

    print(f"Elapsed time: {end - start}")


if __name__ == "__main__":
    main()
