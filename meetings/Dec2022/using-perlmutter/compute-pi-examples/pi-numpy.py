#/usr/bin/env python3
import argparse
import time
import numpy as np

def estimate_pi(n):
    x = np.random.random((n, 2))
    r = np.linalg.norm(x, axis=1)
    c = np.sum(r < 1)
    return 4.0 * c / n

def main():
    parser = argparse.ArgumentParser(description="Monte Carlo Pi Estimatator (NumPy)")
    parser.add_argument("-n", type=int, default=20_000_000, help="number of samples")
    args = parser.parse_args()

    n = args.n

    start = time.time()
    result = estimate_pi(n)
    end = time.time()

    print(f"Elapsed time: {end - start}")

if __name__ == "__main__":
    main()
