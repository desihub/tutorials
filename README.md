# DESI tutorials

Welcome to the repository of tutorials to guide you through the process of analyzing DESI data.
We recommend starting with the tutorials under [01_getting_started/](01_getting_started/)
and then explore additional topics under [02_digging_deeper/](02_digging_deeper/).

Other directories in this repository cover detailed topics and tutorials presented at DESI collaboration meetings; these are not actively maintained and may not work with the latest data and software releases.  Some tutorials require substantial amounts of data or are specific to the
[NERSC](https://nersc.gov) computing center used by the DESI collaboration, but may still be useful to read even without NERSC access.

See [01_getting_started/00_Setup.md](01_getting_started/00_Setup.md) for instructions on installing the necessary Python libraries and downloading example data.

# Other tutorials and resources

## Tutorials in other DESI code repositories

Tutorials hosted in other packages include (but haven't been recently vetted):
* [How to run survey simulations](https://github.com/desihub/surveysim/blob/master/doc/tutorial.rst).
* [How to convert an SED into a simulated DESI spectrum](https://github.com/desihub/specsim/blob/master/docs/nb/SimulationExamples.ipynb)
* [How to run fiber assignment](https://desi.lbl.gov/DocDB/cgi-bin/private/ShowDocument?docid=2742)
* [How to run quicksurvey catalog-level simulations](https://github.com/desihub/quicksurvey_example)
* [How to make all-sky plots](https://github.com/desihub/desiutil/blob/master/doc/nb/SkyMapExamples.ipynb)
* [Working with DESI target bits (Main, CMX, SV)](https://github.com/desihub/desitarget/blob/master/doc/nb/target-selection-bits-and-bitmasks.ipynb)

## Astro Data Lab

The NOIRLab Astro Data Lab serves a copy of the DESI DR1 and EDR databases as `desi_dr1` and `desi_edr`.
These are accessible to users without a NERSC account. 
Various modes of data access are described [here](https://datalab.noirlab.edu/desi/access.php). 
For public access, there is a Table Access Protocol (TAP) handle that provides a convenient access layer for the 
DESI catalog database tables. TAP-aware clients (such as TOPCAT) can point to `https://datalab.noirlab.edu/tap`, 
select the `desi_dr1` database, and see the database tables and descriptions. 

Descriptions of the associated tables can also be found in the Data Lab [table browser](https://datalab.noirlab.edu/query.php?name=desi_dr1.zpix) 
and on the DESI Data Documentation [Database page](https://data.desi.lbl.gov/doc/access/database/). 

## SPARCL

The [SPectra Analysis & Retrievable Catalog Lab (SPARCL)](https://astrosparcl.datalab.noirlab.edu) contains 
DESI DR1 and EDR spectra that were coadded per healpix and coadded across cameras. It is a searchable database that can be used via the Astro Data Lab 
JupyterLab Notebook. Alternatively, the Python client can be installed locally using:
```
pip install sparclclient
```
The client can be loaded within a Python session or program via:
```
>>> from sparcl.client import SparclClient 
>>> client = SparclClient()
```

There are instructions and useful examples in the [How-to-use-SPARCL tutorial notebook](https://github.com/astro-datalab/notebooks-latest/blob/master/04_HowTos/SPARCL/How_to_use_SPARCL.ipynb).

# Acknowledgments

Any use of DESI data whether via NERSC or external databases requires [DESI Data Acknowledgments](https://data.desi.lbl.gov/doc/acknowledgments/).

# For authors of tutorials

Include at the beginning of the tutorial what is needed as a prerequisite for running the tutorial,
e.g. specific codes, environment variables, datasets.  It's OK to link elsewhere for detailed
instructions (e.g. for how to install DESI code in general).

# Bug reporting

If you find a bug in the tutorials, please file a ticket at https://github.com/desihub/tutorials or ask for help on the DESI user forum at https://help.desi.lbl.gov .
