# DESI tutorials

Welcome to the repository designed for tutorials that guide you through the process of simulating and handling DESI data. A host of detailed tutorials can also be found across various DESI code repositories. However, this particular space serves primarily as a platform for:

* Tutorials that were demonstrated at specific DESI meetings, each segregated under directories marked by the date of the meeting. For example, meetings/Dec2020.
* Tutorials designed around wide-ranging subjects (like onskydata) or specific packages (such as fiberassign, redrock).


# Getting started

The tutorials offered herein utilize a Jupyter server at NERSC. This facility enables users to access all DESI data at NERSC and work with pre-installed DESI code without necessitating any local downloads or installations.

Please note, only the tutorials located under getting_started are designed to be compatible for non-DESI NERSC users. The remainder of the tutorials demand access to DESI's private data.

To commence, you will need to create a NERSC account. Follow the instructions detailed on the [DESI wiki](https://desi.lbl.gov/trac/wiki/Computing/AccessNersc), and subsequently log into perlmutter:

```
ssh perlmutter-p1.nersc.gov
```

Jupyter "kernels" are critical in defining a specific set of code versions for use. To install DESI Jupyter kernels from perlmutter-p1.nersc.gov (this is a one-time requirement):

```
source /global/cfs/cdirs/desi/software/desi_environment.sh 23.1
$DESIMODULES/install_jupyter_kernel.sh 23.1
$DESIMODULES/install_jupyter_kernel.sh main
```

To procure a copy of the tutorials on cori.nersc.gov, execute:

```
mkdir -p $HOME/desi/git
cd $HOME/desi/git
git clone https://github.com/desihub/tutorials
```

Navigate to https://jupyter.nersc.gov and sign in using your credentials and OTP (One Time Password).
Then, select the Perlmutter Shared CPU Node "Start" button.
Using the file browser on the left, navigate to the location where you cloned the tutorials repository. ($HOME/desi/git/tutorials in the above commands). Select a tutorial to begin your journey.

If clicking on a tutorial prompts a "Select Kernel" option from a dropdown list, it indicates that the default tutorial kernel on GitHub is not among the kernels already installed on your system. The system is thus asking you to choose from the kernels you do have installed.
While most tutorials are compatible with the latest release (for instance, 23.1) and the "main" release (updated nightly), some tutorials may require a specific release, which will be indicated at the top of the tutorial. If this is the case, return to perlmutter-p1.nersc.gov, run "$DESIMODULES/install_jupyter_kernel.sh VERSION" for the necessary version, and refresh the Jupyter page.


# Menu of tutorials

This repository hosts a selection of tutorials, including:


* Getting started
  These tutorials are centered around the public data releases:
  * [EDR_AnalyzeZcat.ipynb](getting_started/EDR_AnalyzeZcat.ipynb): This tutorial guides you through the process of flagging a unique set of primary (that is, optimal) spectra for a particular object in the EDR catalog and applying fundamental quality cuts. It showcases how to disaggregate the data in the combined catalog based on target type (BGS, LRG, etc.), survey (SV1, SV2, etc.), and the quantity of spectra per target. Additionally, it demonstrates how to extract and depict various spectra of the same target.
  * [intro_to_DESI_EDR_files.ipynb](getting_started/intro_to_DESI_EDR_files.ipynb): This tutorial offers an exploration into the DESI data file structure in the Early Data Release (EDR). It instructs you on how to access different files in the data release, retrieve all available spectra along with redshift information for a specific object, and eventually plot the "best" spectrum.

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
