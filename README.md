# DESI tutorials

This repository is for tutorials on simulating and working with DESI data.
There are additional more detailed tutorials within many of the DESI code
repositories; tutorials here are generally for:

* Tutorials presented at a specific DESI meeting, grouped under a dated directory. e.g. meetings/Dec2020.
* Tutorials on broad topics (onskydata) or packages (fiberassign, redrock). 

# Getting started

These tutorials use a Jupyter server at NERSC, which provides pre-installed DESI code and access to all DESI data at NERSC without having to download or install anything locally.

First, get a NERSC account following the instructions on the [DESI wiki](https://desi.lbl.gov/trac/wiki/Computing/AccessNersc). Then login to cori:
```
ssh cori.nersc.gov
```

Jupyter "kernels" define a specific set of code versions to use.  To install
DESI jupyter kernels from cori.nersc.gov (you only need to do this once):
```
source /project/projectdirs/desi/software/desi_environment.sh 22.2
$DESIMODULES/install_jupyter_kernel.sh 22.2
$DESIMODULES/install_jupyter_kernel.sh master
```

Get a copy of the tutorials on cori.nersc.gov:
```
mkdir -p $HOME/desi/git
cd $HOME/desi/git
git clone https://github.com/desihub/tutorials
```

Login at https://jupyter.nersc.gov and enter your credentials and OTP (One Time Password).
Then, click on the Cori Shared CPU Node "Start" button.
In the file browser on the left, navigate to wherever you cloned the
tutorials repository.  (`$HOME/desi/git/tutorials` in the above commands).
Click on a tutorial to try it out.

If you click on a tutorial and it prompts you to "Select Kernel" from a drop down list, it
means that the default tutorial kernel in GitHub isn't one of the ones that you have already
installed and it is asking you to select from one of the kernels that you do have installed.
In most cases the tutorials will work with the latest release (e.g. 22.2) and
the "master" release (updated nightly, name to switch to "main" in 2021).  Otherwise the
text at the top of the tutorial will tell you which release is needed.  Go back to
cori.nersc.gov, run "$DESIMODULES/install_jupyter_kernel.sh VERSION" for the required version,
and reload the Jupyter page.

# Menu of tutorials

Tutorials in this repository include

* DESI meetings
    * DESI Meeting Dec 2020
      * Dec2020/LSS.ipynb
      * Dec2020/ML_TensorFlow/ML_TensorFlow.ipynb
      * Dec2020/galaxies/fitting_redshifts.ipynb
      * Dec2020/galaxies/fitting_sps.ipynb
      * Dec2020/quickquasars/quickquasars.ipynb

    * DESI Meeting June 2021
      * June2021/Intro_to_a_DESI_Release.ipynb
      * June2021/git-intro.ipynb
      * June2021/nersc_computing/computing_at_nersc.ipynb

    * DESI Meeting Dec 2021
      * Dec2021/Everest_Tutorial_Dec2021.ipynb
      * Dec2021/SpectroperfectionismExample.ipynb

* Fiber assignment
  * [FiberAssign.ipynb](fiberassign/FiberAssign.ipynb): fiber assignment basics
  * [FiberAssignDECaLS.ipynb](fiberassign/FiberAssignDECaLS.ipynb): use observational data from DR8 to prepare it for fiberassign
  * [FiberAssignMocks.ipynb](fiberassign/FiberAssignMocks.ipynb): Generate mock files from simulations to feed into fiberassign
  * [FiberAssignAlgorithms_Part1.ipynb](fiberassign/FiberAssignAlgorithms_Part1.ipynb): a detailed look at fiberassign algorithms
  * [FiberAssignAlgorithms_Part2.ipynb](fiberassign/FiberAssignAlgorithms_Part2.ipynb): fiberassign with multiple survey passes
  * fiberassign/restrict_reach.ipynb
 
* Redrock
  * [RedrockBOSSDemo.ipynb](redrock/RedrockBOSSDemo.ipynb)
  * [RedrockNthBestFit.ipynb](redrock/RedrockNthBestFit.ipynb): How to look up the Nth best redrock fit coefficients. 
  * [RedrockOutputs.ipynb](redrock/RedrockOutputs.ipynb): Understanding redrock outputs and
    connecting the coefficients to template spectra.
  * [redshift-database.ipynb](redrock/redshift-database.ipynb) : interacting with DESI pipeline and redshift data in
    a database (work in progress).
  
  
* On sky data:
    * [spectro_completeness.ipynb](onskydata/spectro_completeness.ipynb): computing spectroscopic completeness on DESI data. 
    * [spectro_nz.ipynb](onskydata/spectro_nz.ipynb): making an n(z) histogram from the spectro production zbest files.
    * [Intro_to_DESI_SV_spectra.ipynb](onskydata/Intro_to_DESI_SV_spectra.ipynb): working with real DESI data from minisv2
    * [EDR_Tutorial.ipynb](onskydata/EDR_Tutorial.ipynb): tutorial notebook to work with EDR data.
    * [Spectroscopic Production Database tutorial](database/spectroscopic-production-database.ipynb): working with EDR data in a database.

* archive
  * [archive/GFA_targets.ipynb](archive/GFA_targets.ipynb)
  * [archive/Intro_to_DESI_spectra.ipynb](archive/Intro_to_DESI_spectra.ipynb)
  * [archive/dc17a-truth.ipynb](archive/dc17a-truth.ipynb)
  * [archive/quickgen.ipynb](archive/quickgen.ipynb)
  * [archive/simulating-desi-spectra.ipynb](archive/simulating-desi-spectra.ipynb): how to simulate your own spectra
  * [archive/survey-simulations.ipynb](archive/survey-simulations.ipynb): how to use "survey simulation" outputs



These links allow you to browse the results of these tutorials from GitHub; to run them yourself follow the instructions in the "Getting started" section above.

# Other tutorials

Tutorials hosted in other packages include (but haven't been recently vetted):
* [How to run survey simulations](https://github.com/desihub/surveysim/blob/master/doc/tutorial.rst).
* [How to convert an SED into a simulated DESI spectrum](https://github.com/desihub/specsim/blob/master/docs/nb/SimulationExamples.ipynb)
* [How to run fiber assignment](https://desi.lbl.gov/DocDB/cgi-bin/private/ShowDocument?docid=2742)
* [How to run quicksurvey catalog-level simulations](https://github.com/desihub/quicksurvey_example)
* [How to make all-sky plots](https://github.com/desihub/desiutil/blob/master/doc/nb/SkyMapExamples.ipynb)
* [Working with DESI target bits (Main, CMX, SV)](https://github.com/desihub/desitarget/blob/master/doc/nb/target-selection-bits-and-bitmasks.ipynb)

# For authors of tutorials

Include at the beginning of the tutorial what is needed as a prerequisite for running the tutorial,
e.g. specific codes, environment variables, datasets.  It's OK to link elsewhere for detailed
instructions (e.g. for how to install DESI code in general).
