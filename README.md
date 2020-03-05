# DESI tutorials

This repository is for tutorials on simulating and working with DESI data.
There are additional more detailed tutorials within many of the DESI code
repositories; tutorials here are generally for:
* Topics that span individual repositories, e.g. working with data challenge outputs
* Tutorials to be presented at a collaboration meeting where we want to decouple
  updates to the tutorial itself from the desispec, desisim, etc. code versions that
  the tutorial is describing.

# Getting started

These tutorials use a Jupyter server at NERSC, which provides pre-installed DESI code and access to all DESI data at NERSC without having to download or install anything locally.

First, get a NERSC account following the instructions on the [DESI wiki](https://desi.lbl.gov/trac/wiki/Computing/AccessNersc). Then login to cori:
```
ssh cori.nersc.gov
```

Install the DESI jupyter kernel from cori.nersc.gov (you only need to do this once):
```
source /project/projectdirs/desi/software/desi_environment.sh 19.10
$DESIMODULES/install_jupyter_kernel.sh 19.10
```

Get a copy of the tutorials on cori.nersc.gov:
```
mkdir -p $HOME/desi/git
cd $HOME/desi/git
git clone https://github.com/desihub/tutorials
```

Login at https://jupyter.nersc.gov and enter your credentials and OTP.
Then, click on the Cori Shared CPU Node "Start" button.
In the file browser on the left, navigate to wherever you cloned the
tutorials repository.  (`$HOME/desi/git/tutorials` in the above commands).
Click on a tutorial to try it out.


# Menu of tutorials

Tutorials in this repository include
* [Intro_to_DESI_spectra.ipynb](Intro_to_DESI_spectra.ipynb): how to find and read DESI spectra
* [simulating-desi-spectra.ipynb](simulating-desi-spectra.ipynb): how to simulate your own spectra
* [survey-simulations.ipynb](survey-simulations.ipynb): how to use "survey simulation" outputs
* [dc17a-truth.ipynb](dc17a-truth.ipynb): connecting dc17a spectra and redshift catalog entries
    back to their input truth.
* [redshift-database.ipynb](redshift-database.ipynb) : interacting with DESI pipeline and redshift data in
    a database.
* [RedrockOutputs.ipynb](redrock/RedrockOutputs.ipynb): Understanding redrock outputs and
    connecting the coefficients to template spectra.
* [FiberAssign.ipynb](FiberAssign.ipynb): fiber assignment
* [FiberAssignDECaLS.ipynb](FiberAssignDECaLS.ipynb): use observational data from DR8 to prepare it for fiberassign
* [FiberAssignMocks.ipynb](FiberAssignMocks.ipynb): Generate mock files from simulations to feed into fiberassign


These links allow you to browse the results of these tutorials from GitHub; to run them yourself follow the instructions in the "Getting started" section above.

# Other tutorials

Tutorials hosted in other packages include (but haven't been recently vetted):
* [How to run survey simulations](https://github.com/desihub/surveysim/blob/master/doc/tutorial.rst).
* [How to convert an SED into a simulated DESI spectrum](https://github.com/desihub/specsim/blob/master/docs/nb/SimulationExamples.ipynb)
* [How to run fiber assignment](https://desi.lbl.gov/DocDB/cgi-bin/private/ShowDocument?docid=2742)
* [How to run quicksurvey catalog-level simulations](https://github.com/desihub/quicksurvey_example)
* [How to make all-sky plots](https://github.com/desihub/desiutil/blob/master/doc/nb/SkyMapExamples.ipynb)

# For authors of tutorials

Include at the beginning of the tutorial what is needed as a prerequisite for running the tutorial,
e.g. specific codes, environment variables, datasets.  It's OK to link elsewhere for detailed
instructions (e.g. for how to install DESI code in general).
