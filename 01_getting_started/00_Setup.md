# Setup to run these tutorials

## Running the tutorials on a local machine

To run these tutorials on a local machine, you will need a Python environment
with a set of 3rd party libraries, plus some DESI code and example data.

1. Install [miniforge](https://conda-forge.org/download/) or
   [anaconda](https://www.anaconda.com/download)

2. Create a DESI environment with the required packages

    ```
    conda create --name desi 'numpy<2' scipy 'astropy<7' ipython jupyter \
            matplotlib numba pytest fitsio h5py healpy requests
    conda activate desi
    ```

3. Install the DESI-specific packages

    ```
    pip install git+https://github.com/desihub/desiutil@3.5.0
    pip install git+https://github.com/desihub/desitarget@2.9.0
    pip install git+https://github.com/desihub/desispec@0.69.0
    pip install git+https://github.com/desihub/desimodel@0.19.3
    install_desimodel_data
    pip install git+https://github.com/desihub/redrock@0.20.4
    install_redrock_templates
    ```

    **NOTE**: To get the absolute latest versions, you can replace those tag X.Y.Z numbers
    with "main".  If you previously installed main and want to update it again,
    use `pip install --force-reinstall ...`.

4. Download example DESI data

    ```
    curl https://raw.githubusercontent.com/desihub/desida/refs/tags/1.0.0/bin/desi_get_dr_subset > desi_get_dr_subset
    python desi_get_dr_subset
    ```

    **NOTE**: if you don't have curl installed, you can also use wget or download `desi_get_dr_subset` using a web browser.

    **NOTE**: even a "tiny" subset of DR1 is ~40 GB and can take an hour or more to download
    even with a fast internet connection.  Once you have gotten past the
    "Downloading files for healpix 23040..." step you can proceed with the tutorials
    while the remaining tile-based data finish downloading
    (needed for [03_DataOrganization.ipynb](03_DataOrganization.ipynb) and [05_Spectra.ipynb](05_Spectra.ipynb)
    but not the others)

    **NOTE**: Most of these tutorials require downloading example files.
    The [06_PublicDatabaseAccess.ipynb](06_PublicDatabaseAccess.ipynb) tutorial demonstrates
    an alternative method of accessing the data through public database queries and
    downloading spectra on-the-fly using
    [SPARCL](https://astrosparcl.datalab.noirlab.edu), without needing any local data.

5. Set `$DESI_ROOT` to the path where you just downloaded the data

    * bash: `export DESI_ROOT=$PWD/tiny_dr1`
    * tcsh: `setenv DESI_ROOT $PWD/tiny_dr1`

6. Get the tutorials and start Jupyter

    ```
    git clone https://github.com/desihub/tutorials
    cd tutorials
    jupyter lab .
    ```

    **Safari Users**: JupyterLab 4.3.5 and Safari 16.4 have a bug rendering newly added cells.
    This can be fixed under Settings -> Settings Editor -> Notebook -> Windowing mode
    (near bottom) -> set to "defer"

7. Proceed with the [01_getting_started/01_QuickStart.ipynb](01_QuickStart.ipynb) tutorial in the left panel.


## Running the tutorials at NERSC

If you have access to [NERSC](https://nersc.gov), e.g. through DESI, DES, LSST-DESC, CMB-S4, etc.,
you can run the tutorials at https://juypter.nersc.gov and have access to the full public DESI data
without having to copy or download anything.
To do this, you will need to install a "Jupyter kernel" that tells it where to find the pre-installed
DESI code and data.

1. Log into perlmutter.nersc.gov and install Jupyter kernel with DESI packages configured for DR1:

    ```
    ssh perlmutter.nersc.gov
    /global/common/software/desi/install_jupyter_kernel --software-version 25.3 --data-release dr1
    ```

2. Get a copy of these tutorials
    ```
    git clone https://github.com/desihub/tutorials
    ```

3. Login to https://jupyter.nersc.gov, start a "Perlmutter Login Node" server,
   and navigate to the location where you cloned the tutorials.

4. Start with [01_getting_started/01_QuickStart.ipynb](01_QuickStart.ipynb).
   For each tutorial, Kernel -> Change Kernel... (or click on the kernel name
   in the upper right) and change the kernel to the "DESI 25.3 DR1" kernel
   that you installed in step 1.

**NOTE**: If you get an `ModuleNotFoundError` or `ImportError` when running these
tutorials, you probably forgot to switch to a DESI kernel first.
In that case, switch kernels and restart the notebook from the beginning.

**NOTE**: at NERSC you do *not* need to get a copy of the data since that is already there.
The Jupyter kernel will set `$DESI_ROOT` to the DR1 location, and the tutorials will find
it from there.


