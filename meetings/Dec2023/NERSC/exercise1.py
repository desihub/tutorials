#!/usr/bin/env python

"""
Subtract the continuum using a median-filter from spectra in files
"""

import os, sys, time
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
    t1 = time.time()

    # subtract median-filter continuum
    # Note: medfilt could do this as a single 2D operation much faster,
    # but we'll loop to mimic some work per spectrum
    newflux = np.zeros(flux.shape)
    for i in range(flux.shape[0]):
        newflux[i] = flux[i] - medfilt(flux[i], 15)

    # print timing just to show we're doing something
    t2 = time.time()

    basename = os.path.basename(filename)
    print(f'{basename} {t1-t0:.1f} + {t2-t1:.1f} sec')

    return newflux

def main():
    start_time = time.time()
    for filename in sys.argv[1:]:
        subtract_continuum(filename)

    total_time = time.time() - start_time
    print(f'Total time {total_time:.1f} sec')

if __name__ == '__main__':
    main()
