# Getting Started

Welcome to the **DESI Getting Started Tutorials**! 

This resource is designed to guide you through the fundamentals of working with DESI data, providing references and tutorials to help you navigate and make the most of the DESI ecosystem.

The current set of tutorials is based upon DESI Data Release 1 (DR1) data.
Previous tutorials for the Early Data Release (EDR) are archived under the
[EDR/](./EDR) directory.

Start with [00_Setup.md](./00_Setup.md) for initial software setup and how to access example data, then proceed with the other tutorials.

## Tutorial Overview

- [00_Setup.md](./00_Setup.md): Set-up instructions to run the file-based tutorials either locally or at NERSC.
- [01_QuickStart.ipynb](./01_QuickStart.ipynb): Rapid overview of DESI DR1 file access from redshift catalogs through spectra.
- [02_CoreConcepts.md](./02_CoreConcepts.md): Explanation of key concepts to better understand DESI data and tutorials (e.g., survey, program, healpix, tile, specprod).
- [03_DataOrganization.ipynb](./03_DataOrganization.ipynb): Navigation of the DESI data file structure under a spectroscopic production run ("specprod")
- [04_RedshiftCatalogs.ipynb](./04_RedshiftCatalogs.ipynb): In-depth usage of the DESI redshift catalog files such as object/target selection, data quality cuts, choosing the best of multiple spectra, and spectral classification
- [05_Spectra.ipynb](./05_Spectra.ipynb): Broad usage of DESI spectra files including reading, slicing, combining, and writing spectra data
- [06_PublicDatabaseAccess.ipynb](./06_PublicDatabaseAccess.ipynb): Usage of searchable databases of DESI catalogs and spectra accessible publicly covering sample selection, classification per target class or spectral type, retrieval and visualization of spectra with SPARCL. 

## Additional Resources

### 1. DESI Data Documentation

The [DESI Data Documentation website](https://data.desi.lbl.gov/doc/) offers detailed information about:
- [Data access and formats](https://data.desi.lbl.gov/doc/access/)
- [Data releases](https://data.desi.lbl.gov/doc/releases/)
- [Technical papers and key cosmology results](https://data.desi.lbl.gov/doc/papers/)
- [Data license and acknowledgments](https://data.desi.lbl.gov/doc/acknowledgments/)

### 2. DESI Helpdesk

Have questions or need assistance?  
Visit the [DESI User Forum](https://help.desi.lbl.gov) to ask questions and find solutions provided by the DESI community and support team.

### 3. Tutorials and Data at NOIRLab

Looking for additional tutorials and data outside NERSC?  
[NOIRLab's Astro Data Lab](https://datalab.noirlab.edu/desi/index.php) provides both public (anonymous) and authenticated services to access DESI data including a database containing the main pipeline catalogs (e.g., redshift, target, photometry catalogs). The full-depth ("healpix coadds") spectra are available via [SPectra Analysis and Retrievable Catalog Lab (SPARCL)](https://astrosparcl.datalab.noirlab.edu/) for fast search and retrieval. Other types of spectra (per exposure, per night, per tile) are only available at NERSC using files ([05_Spectra.ipynb](./05_Spectra.ipynb)).

In addition to the [06_PublicDatabaseAccess.ipynb](./06_PublicDatabaseAccess.ipynb) tutorial provided here, additional [tutorials](https://github.com/astro-datalab/notebooks-latest/tree/master/03_ScienceExamples/DESI) are available to help you explore and analyze DESI data effectively. 

### 4. Public TAP handle for, e.g., TOPCAT or Astroquery

The Astro Data Lab created a Table Access Protocol (TAP) handle that provides a convenient access layer for the 
DESI catalog database tables. TAP-aware clients (such as TOPCAT) can point to `https://datalab.noirlab.edu/tap`, 
select the `desi_dr1` database, and see the database tables and descriptions. 

Descriptions of the associated tables can also be found in the Astro Data Lab [table browser](https://datalab.noirlab.edu/query.php?name=desi_dr1.zpix) 
and on the DESI Data Documentation [Database page](https://data.desi.lbl.gov/doc/access/database/). 

Below is an example code snippet featuring [Astroquery](https://astroquery.readthedocs.io/en/latest/), a coordinated package of astropy:
```
from astroquery.utils.tap.core import Tap

## Point TAP service to Astro Data Lab URL
datalab_tap_url = "https://datalab.noirlab.edu/tap"

## Create TAP service object
tap_service = Tap(url=datalab_tap_url)

## Example query in ADQL (similar to SQL but Astronomy tailored)
query = """
SELECT TOP 10 targetid, survey, program, z, zwarn, spectype
FROM desi_dr1.zpix
WHERE mean_fiber_ra BETWEEN 150 AND 151
AND mean_fiber_dec BETWEEN 2 AND 3
"""

## Run query
job = tap_service.launch_job(query)

## Save output into result
result = job.get_results()
```

For additional tips and example usage, consult: https://astroquery.readthedocs.io/en/latest/utils/tap.html