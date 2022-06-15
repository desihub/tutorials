#!/bin/bash -l
module load python
source activate myenv
# You can add whatever you want in here module loads, definitions, etc. works as the other example of shell file.

# This last line is important and should always be the last one!
exec python -m ipykernel_launcher "$@"


