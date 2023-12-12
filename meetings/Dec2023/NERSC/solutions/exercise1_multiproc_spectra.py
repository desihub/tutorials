#!/usr/bin/env python

"""
Subtract the continuum using a median-filter from spectra in files.

Do each file serially, and multiprocess parallelize over spectra within
each file.
"""

import os, sys, time
import multiprocessing
import numpy as np
from scipy.signal import medfilt
from astropy.io import fits

# wrapper function to call with multiprocessing.Pool.map
# subtracts median-filter continuum from 1D spectrum
def _sub1d(flux1d):
    return flux1d - medfilt(flux1d, 15)

def subtract_continuum(filename):
    """
    Subtract a median-filter continuum from each spectrum in flux

    Args:
        flux[nspec,nwave]: 2D input flux for nspec spectra x nwave wavelengths

    Returns:
        continuum-subtracted newflux[nspec,nwave]
    """
    t0 = time.time()

    # Read R-band flux from filename
    flux = fits.getdata(filename, 'R_FLUX')

    # subtract median-filter continuum
    # Note: medfilt could do this as a single 2D operation much faster,
    # but we'll loop to mimic some work per spectrum
    with multiprocessing.Pool() as pool:
        newflux = pool.map(_sub1d, flux)

    newflux = np.vstack(newflux)  # list of 1D arrays -> 2D array

    # print timing just to show we're doing something
    dt = time.time() - t0
    basename = os.path.basename(filename)
    print(f'{basename} {dt:.1f} sec')

    return newflux

def main():
    start_time = time.time()
    for filename in sys.argv[1:]:
        subtract_continuum(filename)

    total_time = time.time() - start_time
    print(f'Total time {total_time:.1f} sec')

if __name__ == '__main__':
    main()
