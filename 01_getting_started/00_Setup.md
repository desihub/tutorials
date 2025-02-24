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
    cd tutorials/01_getting_started
    jupyter lab .
    ```

    **Safari Users**: JupyterLab 4.3.5 and Safari 16.4 have a bug rendering newly added cells.
    This can be fixed under Settings -> Settings Editor -> Notebook -> Windowing mode
    (near bottom) -> set to "defer"

8. Proceed with the `01_QuickStart.ipynb` tutorial in the left panel.


## Running the tutorials at NERSC

**DESI Collaborators**: install the DESI "main" kernel described at https://desi.lbl.gov/trac/wiki/Computing/JupyterAtNERSC.

**TODO**: the remaining instructions for non-DESI NERSC accounts don't work yet.

If you have access to [NERSC](https://nersc.gov), e.g. through DESI, DES, LSST-DESC, CMB-S4, etc.,
you can run the tutorials at https://juypter.nersc.gov and have access to the full public DESI data.
To do this, you will need to install a "Jupyter kernel" that tells it where to find the pre-installed
DESI code.

* **TODO**: make a newer set of tags to use with DR1 data
* **TODO**: These instructions for non-DESI collaborator usage at NERSC don't work yet due to missing kernels, lack of desitree/dr1 module, and possibly other issues.

1. Log into perlmutter.nersc.gov and set up the DESI code environment pointing to the publicly accessible DR1 location using the following commands:

    ```
    source /global/common/software/desi/desi_environment.sh main
    module switch desitree/dr1
    ```
    **TODO**: Make new software release with latest tags

2. Determine your shell by using the command: `echo ${SHELL}`.

3. Depending on your shell, select the appropriate kernel version:
    * For /bin/bash, /bin/sh, or /bin/zsh, use the "bash" kernels. For example, `desi-dr1-23.1-bash`.
    * For /bin/tcsh or /bin/csh, use the "tcsh" kernels. For example, `desi-dr1-23.1-tcsh`.

4. Copy the chosen kernel to your home directory using the following command:
    ```
    mkdir -p ~/.local/share/jupyter/kernels
    cp -R /global/common/software/desi/kernels/desi-dr1-23.1-bash ~/.local/share/jupyter/kernels
    ```
    This step will install the DESI DR1 23.1 kernel. Other available kernels are `desi-22.5`, `desi-23.1` and `desi-main`,

5. Get a copy of these tutorials
    ```
    git clone https://github.com/desihub/tutorials
    ```

6. Login to https://jupyter.nersc.gov and navigate to the location where you cloned the tutorials.
   Start with `01_getting_started/DR1/01_QuickStart.ipynb`.

