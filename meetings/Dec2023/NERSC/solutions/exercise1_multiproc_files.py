#!/usr/bin/env python

"""
Subtract the continuum using a median-filter from spectra in files

Multiprocess parallelize over files.
"""

import os, sys, time
import multiprocessing
import numpy as np
from scipy.signal import medfilt
from astropy.io import fits

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
    newflux = np.zeros(flux.shape)
    for i in range(flux.shape[0]):
        newflux[i] = flux[i] - medfilt(flux[i], 15)

    # print timing just to show we're doing something
    dt = time.time() - t0
    basename = os.path.basename(filename)
    print(f'{basename} {dt:.1f} sec')

    return newflux

def main():
    start_time = time.time()

    filenames = sys.argv[1:]
    with multiprocessing.Pool() as pool:
        newfluxes = pool.map(subtract_continuum, filenames)

    total_time = time.time() - start_time
    print(f'Total time {total_time:.1f} sec')

if __name__ == '__main__':
    main()
