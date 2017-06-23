# Redrock plotspec

This page documents how to run the `redrock.PlotSpec` viewer to get plots like:

![redrock.PlotSpec screenshot](rrplotspec.png)

## Installation

Install the redrock + desispec code into an isolated conda environment:
```
conda create -n rrdesi python=3 numpy scipy astropy numba ipython h5py matplotlib pyyaml
pip install speclite
source activate rrdesi

git clone https://github.com/desihub/redrock-templates
git clone https://github.com/desihub/redrock
git clone https://github.com/desihub/desiutil
git clone https://github.com/desihub/desispec

for repo in desiutil desispec redrock; do
    cd $repo
    python setup.py install
    cd ..
done

export RR_TEMPLATE_DIR=$(pwd)/redrock-templates
```

## Getting example data

Available from NERSC at
```
/project/projectdirs/desi/datachallenge/dc17a-twopct/dc17a-lite.tar.gz
```

## Running plotspec

Go to the top level directory where you have those files then start
an ipython session with `ipython --pylab`:
```
#- import required packages
import numpy as np
import redrock.io
from redrock.external import desi
from astropy.table import Table, join

#- read redshift results and truth table
specfile = 'spectro/redux/dc17a2/spectra-64/172/17242/spectra-64-17242.fits'
rrfile = 'spectro/redux/dc17a2/spectra-64/172/17242/rr-64-17242.h5'
zbestfile = 'spectro/redux/dc17a2/spectra-64/172/17242/zbest-64-17242.fits'
truthfile = 'targets/truth-lite.fits'
templates = redrock.io.read_templates()
targets, targetids = desi.read_spectra(specfile)
zscan, zfit = redrock.io.read_zscan(rrfile)
zbest = Table.read(zbestfile)
truth = Table.read(truthfile)

#- Plot spectra and redshift fits
p = redrock.PlotSpec(targets, templates, zscan, zfit)

#- Include truth info in plots; first fix some datamodel inconsistencies
truth['targetid'] = truth['TARGETID']
truth['ztrue'] = truth['TRUEZ']
p = redrock.PlotSpec(targets, templates, zscan, zfit, truth=truth)

#- Filter on bad QSO targets
ztruth = join(truth, zbest, keys='TARGETID')
ztruth['TEMPLATETYPE'][:] = np.char.strip(ztruth['TEMPLATETYPE'])
dv = 3e5*(ztruth['Z'] - ztruth['TRUEZ']) / (1+ztruth['TRUEZ'])
isqso = ztruth['TEMPLATETYPE'] == 'QSO'
bad = (np.abs(dv)>1000) & (ztruth['ZWARN'] == 0) & (isqso)

bad_targetids = ztruth['TARGETID'][bad]
bad_targets = list()
for t in targets:
    if t.id in bad_targetids:
        bad_targets.append(t)

p = redrock.PlotSpec(bad_targets, templates, zscan, zfit, truth=truth)
```