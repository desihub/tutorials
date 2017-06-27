# DESI tutorials

This repository is for tutorials on simulating and working with DESI data.
There are additional more detailed tutorials within many of the DESI code
repositories.  Tutorials in this repository are generally for:
* Topics that span individual repositories, e.g. working with data challenge outputs
* Tutorials to be presented at a collaboration meeting where we want to decouple
  updates to the tutorial itself from the desispec, desisim, etc. code versions that
  the tutorial is describing.
  
# Menu of tutorials

Tutorials in this repository include
* [Intro_to_DESI_spectra.ipynb](Intro_to_DESI_spectra.ipynb): how to find and read DESI spectra
* [simulating-desi-spectra.ipynb](simulating-desi-spectra.ipynb): how to simulate your own spectra
* [dc17a-truth.ipynb](dc17a-truth.ipynb) : connecting dc17a spectra and redshift catalog entries
    back to their input truth.
* [RedrockOutputs.ipynb](redrock/RedrockOutputs.ipynb) : Understanding redrock outputs and
    connecting the coefficients to template spectra.
* [RedrockPlotSpec.md](redrock/RedrockPlotSpec.md) : How to plot redrock outputs
    (spectra, template fits, chi2 vs. z)

# Other tutorials

Tutorials hosted in other packages include:
* [https://github.com/desihub/surveysim/blob/master/doc/tutorial.md](How to run survey simulations).
* [https://github.com/desihub/specsim/blob/master/docs/nb/SimulationExamples.ipynb](How to convert an SED into a simulated DESI spectrum)
* [https://desi.lbl.gov/DocDB/cgi-bin/private/ShowDocument?docid=2742](How to run fiber assignment)
* [https://github.com/desihub/quicksurvey_example](How to run quicksurvey catalog-level simulations)

# For authors of tutorials

Include at the beginning of the tutorial what is needed as a prerequisite for running the tutorial,
e.g. specific codes, environment variables, datasets.  It's OK to link elsewhere for detailed
instructions (e.g. for how to install DESI code in general).
