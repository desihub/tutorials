# Setup to run these tutorials

## Running the tutorials on a local machine

To run these tutorials on a local machine, you will need a Python environment
with a set of 3rd party libraries, plus some DESI code and example data.

1. Install [miniforge](https://conda-forge.org/download/) or
   [anaconda](https://www.anaconda.com/download)

2. Create a DESI environment with the required packages

    ```
    conda create --name desitest 'numpy<2' scipy 'astropy<7' ipython jupyter \
            matplotlib numba pytest fitsio h5py healpy requests
    conda activate desitest
    ```

3. Install the DESI-specific packages

    ```
    pip install git+https://github.com/desihub/desiutil.git@main
    pip install git+https://github.com/desihub/desitarget.git@main
    pip install git+https://github.com/desihub/desispec.git@main
    pip install git+https://github.com/desihub/desimodel.git@main
    install_desimodel_data
    ```
    **TODO**: update those to a new set of tags.

4. Download example DESI data

    **TODO**: instructions for using `desi_download_dr1_subset` to download data without needing a NERSC account.

    In the meantime,
    ```
    scp -r dtn01.nersc.gov:/global/cfs/cdirs/desi/users/forero/tiny_dr1 .
    scp -r dtn01.nersc.gov:/global/cfs/cdirs/desi/spectro/redux/iron/tiles-iron.csv tiny_dr1/spectro/redux/iron/
    scp -r dtn01.nersc.gov:/global/cfs/cdirs/desi/spectro/redux/iron/exposures-iron.csv tiny_dr1/spectro/redux/iron/
    ```

6. Set `$DESI_ROOT` to the path where you just downloaded the data

    * bash: `export DESI_ROOT=$PWD/tiny_dr1`
    * tcsh: `setenv DESI_ROOT $PWD/tiny_dr1`

7. Get the tutorials and start Jupyter

    ```
    git clone https://github.com/desihub/tutorials
    cd tutorials
    git checkout dr1   # TODO: not needed after DR1 becomes public
    jupyter lab .
    ```

    **Safari Users**: JupyterLab 4.3.5 and Safari 16.4 have a bug rendering newly added cells.
    This can be fixed under Settings -> Settings Editor -> Notebook -> Windowing mode
    (near bottom) -> set to "defer"

8. Proceed with the `01_getting_tarted/01_QuickStart.ipynb` tutorial in the left panel.


## Running the tutorials at NERSC

If you have access to [NERSC](https://nersc.gov), e.g. through DESI, DES, LSST-DESC, CMB-S4, etc.,
you can run the tutorials at https://juypter.nersc.gov and have access to the full public DESI data.
To do this, you will need to install a "Jupyter kernel" that tells it where to find the pre-installed
DESI code.

1. Log into perlmutter.nersc.gov and install Jupyter kernel with DESI packages configured for DR1:

    ```
    ssh perlmutter.nersc.gov
    /global/common/software/desi/install_jupyter_kernel --software-version 24.11 --data-release dr1
    
    ```

2. Get a copy of these tutorials
    ```
    git clone https://github.com/desihub/tutorials
    cd tutorials
    git checkout dr1
    ```
    **TODO**: those last two lines will not be necessary once DR1 is public

3. Login to https://jupyter.nersc.gov and navigate to the location where you cloned the tutorials.
   Start with `01_getting_started/DR1/01_QuickStart.ipynb`.

