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
    pip install git+https://github.com/desihub/desimodel.git@install-data
    install_desimodel_data
    ```
    **TODO**: update those to a new set of tags.

4. Download example DESI data

    **TODO**: instructions for downloading Jaime's example `tiny_dr1` and setting `$DESI_ROOT`.

5. Get the tutorials and start Jupyter

    ```
    git clone https://github.com/desihub/tutorials
    cd tutorials/01_getting_started/DR1
    jupyter lab .
    ```

6. Proceed with the `01_QuickStart.ipynb` tutorial in the left panel.


## Running the tutorials at NERSC

If you have access to [NERSC](https://nersc.gov), e.g. through DESI, DES, LSST-DESC, CMB-S4, etc.,
you can run the tutorials at https://juypter.nersc.gov and have access to the full public DESI data.
To do this, you will need to install a "Jupyter kernel" that tells it where to find the pre-installed
DESI code.

1. Log into perlmutter.nersc.gov and set up the DESI code environment. Switch the environment variables to the publicly accessible DR1 location using the following commands:

    ```
    source /global/common/software/desi/desi_environment.sh 23.1
    module switch desitree/dr1
    ```

2. Determine your shell by using the command: echo ${SHELL}.

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

