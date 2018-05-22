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

First, get a NERSC account following the instructions on the [DESI wiki](https://desi.lbl.gov/trac/wiki/Computing/AccessNersc).

Install the DESI jupyter kernel from cori.nersc.gov (you only need to do this once):
```
source /project/projectdirs/desi/software/desi_environment.sh 18.3
$DESIMODULES/install_jupyter_kernel.sh 18.3
```

Get a copy of the tutorials on cori.nersc.gov:
```
cd $HOME/desi/git
git clone https://github.com/desihub/tutorials
```

Login at https://jupyter-dev.nersc.gov and browse to wherever you cloned the tutorials repository
(`$HOME/desi/git/tutorials` in the above commands).  Click on a tutorial to try it out.


# Menu of tutorials

Tutorials in this repository include
* [survey-simulations.ipynb](survey-simulations.ipynb): how to use "survey simulation" outputs
* [Intro_to_DESI_spectra.ipynb](Intro_to_DESI_spectra.ipynb): how to find and read DESI spectra
* [simulating-desi-spectra.ipynb](simulating-desi-spectra.ipynb): how to simulate your own spectra
* [dc17a-truth.ipynb](dc17a-truth.ipynb): connecting dc17a spectra and redshift catalog entries
    back to their input truth.
* [RedrockOutputs.ipynb](redrock/RedrockOutputs.ipynb): Understanding redrock outputs and
    connecting the coefficients to template spectra.
* [RedrockPlotSpec.md](redrock/RedrockPlotSpec.md): How to plot redrock outputs
    (spectra, template fits, chi2 vs. z)

These links allow you to browse the results of these tutorials from GitHub; to run them yourself follow the instructions in the "Getting started" section above.

# Other tutorials

Tutorials hosted in other packages include (but haven't been recently vetted):
* [How to run survey simulations](https://github.com/desihub/surveysim/blob/master/doc/tutorial.rst).
* [How to convert an SED into a simulated DESI spectrum](https://github.com/desihub/specsim/blob/master/docs/nb/SimulationExamples.ipynb)
* [How to run fiber assignment](https://desi.lbl.gov/DocDB/cgi-bin/private/ShowDocument?docid=2742)
* [How to run quicksurvey catalog-level simulations](https://github.com/desihub/quicksurvey_example)

# For authors of tutorials

Include at the beginning of the tutorial what is needed as a prerequisite for running the tutorial,
e.g. specific codes, environment variables, datasets.  It's OK to link elsewhere for detailed
instructions (e.g. for how to install DESI code in general).
