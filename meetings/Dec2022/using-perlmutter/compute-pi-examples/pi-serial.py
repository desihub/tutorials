#!/usr/bin/env python3
import argparse
import time

from library import estimate_pi


def main():
    parser = argparse.ArgumentParser(description="Monte Carlo Pi Estimatator (Serial)")
    parser.add_argument("-n", type=int, default=20_000_000, help="number of samples")
    args = parser.parse_args()

    n = args.n

    start = time.time()
    result = estimate_pi(n)
    end = time.time()

    print(f"Elapsed time: {end - start}")


if __name__ == "__main__":
    main()
