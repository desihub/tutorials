# Introduction to Year 3 Data and Using NERSC Effectively

Stephen Bailey<br/>
DESI Cancun Meeting December 2024<br/>
ECS Tutorial

*Parts of this tutorial are adapted from the [intro_to_DESI_EDR_files](https://github.com/desihub/tutorials/blob/main/getting_started/intro_to_DESI_EDR_files.ipynb) tutorial originally developed by
Ragadeepika Pucha (U.Arizona), Anthony Kremin (Berkeley Lab), Stéphanie Juneau (NOIRLab), Jaime E. Forero-Romero (Uniandes), and DESI Data Team*

## Goals

This tutorial covers the following topics covering a range of expertise
    
| File | Description |
|:------ |:---------- |
| 01_CoreConcepts.ipynb     | Basic terminology for undersanding how DESI data are organized. |
| 02_DataOrganization.ipynb | Tour of what files are what in a DESI data production. |
| 03_RedshiftCatalogs.ipynb | Using Redshift catalogs |
| 04_Spectra.ipynb          | Using DESI spectra |
| 05_NERSC.md               | Tips for using NERSC effectively |

<br/>

## Code Setup

All of these tutorials can be read at https://github.com/desihub/tutorials/tree/main/meetings/Dec2024/DataIntro .  If you want to interact with them and explore some more, you can run the notebooks using https://jupyter.nersc.gov, but you'll need to setup the DESI kernels first so that your Jupyter notebook can find the DESI code.

Open a terminal (either from Jupyter File -> New -> Terminal or `ssh perlmutter.nersc.gov`) and run the following commands

```
source /global/common/software/desi/desi_environment.sh 24.11
${DESIMODULES}/install_jupyter_kernel.sh 24.11
${DESIMODULES}/install_jupyter_kernel.sh main
```

See https://desi.lbl.gov/trac/wiki/Computing/JupyterAtNERSC for more details and debugging issues.

From the same terminal, get the code
```
mkdir -p /global/cfs/cdirs/desi/users/$USER
cd /global/cfs/cdirs/desi/users/$USER
git clone https://github.com/desihub/tutorials
```

You can put the git clone wherever you want on disk, but we recommend putting it
somewhere under `/global/cfs/cdirs/desi/users/$USER` instead of `$HOME` because then
any plots or files you generate can be shared with your collaborators (they can't
see your `$HOME` directory) and those files/plots can also be downloaded to your
laptop using https://data.desi.lbl.gov/desi/users/ .

## Starting jupyter.nersc.gov

Browse to https://jupyter.nersc.gov and login with your NERSC credentials.

Start a Perlmutter Login Node server (leftmost option).

On the lefthand panel "FILE BROWSER", click the folder icon to go back to the `/` root directory, then browse to `/global/cfs/cdirs/desi/users/(your_user_name)` or wherever you put the code.

**Pro tip**: click the star icon to add this directory to your favorites to make it easier to browse there in the future.

Navigate to `tutorials/meetings/Dec2024/DataIntro` and select notebooks and Markdown (md) files to view.