#!/usr/bin/env python

"""
Subtract the continuum using a median-filter from spectra in files.

MPI-parallelize over files, multiprocess parallelize over spectra
within a file.
"""

import os, sys, time
import multiprocessing
import argparse
import numpy as np
from scipy.signal import medfilt
from astropy.io import fits

# wrapper function to call with multiprocessing.Pool.map
# subtracts median-filter continuum from 1D spectrum
def _sub1d(flux1d):
    return flux1d - medfilt(flux1d, 31)

def subtract_continuum(filename, nproc):
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
    if nproc > 1:
        with multiprocessing.Pool(nproc) as pool:
            newflux = pool.map(_sub1d, flux)

        newflux = np.vstack(newflux)  # list of 1D arrays -> 2D array
    else:
        newflux = np.zeros(flux.shape)
        for i in range(flux.shape[0]):
            newflux[i] = _sub1d(flux[i])

    # print timing just to show we're doing something
    t2 = time.time()
    basename = os.path.basename(filename)
    print(f'{basename} {t1-t0:.1f} + {t2-t1:.1f} sec using {nproc} processes')

    return newflux

def main():
    # IMPORTANT: when used with multiprocessing, mpi4py imports must be
    # inside a function, not at top level module (!?!)
    from mpi4py import MPI
    from mpi4py.futures import MPICommExecutor

    start_time = time.time()

    # argparse to get --nproc number of multiprocesses to use
    parser = argparse.ArgumentParser()
    parser.add_argument('--nproc', type=int,
        default=multiprocessing.cpu_count(),
        help='Number of multiprocessing processes to use')
    parser.add_argument('--filelist', type=str, required=True,
        help='Text file with list of input coadd files to process')

    args = parser.parse_args()

    # connect to MPI communicator to find out which rank this is
    comm = MPI.COMM_WORLD
    rank = comm.rank
    size = comm.size

    # required for MPI + multiprocessing to play nicely together
    multiprocessing.set_start_method('spawn')

    # Rank 0 create arglist of (filename, nproc)
    if rank == 0:
        arglist = list()
        for filename in open(args.filelist).readlines():
            filename = filename.strip()  # remove trailing newline
            arglist.append( (filename, args.nproc) )
    else:
        arglist = None

    # MPI parallelize over files; only rank 0 needs arglist
    with MPICommExecutor(comm, root=0) as pool:
        newflux = pool.starmap(subtract_continuum, arglist)

    # with MPICommExecutor, only rank 0 gets the results
    if rank == 0:
        newflux = np.vstack(list(newflux))  # list of 1D arrays -> 2D array

    comm.barrier()  # wait for all ranks to finish
    total_time = time.time() - start_time
    if rank == 0:
        print(f'Total time {total_time:.1f} sec')

if __name__ == '__main__':
    main()
