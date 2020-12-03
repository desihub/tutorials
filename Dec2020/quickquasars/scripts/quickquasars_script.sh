#!/bin/bash -l
## Originally taken from https://github.com/desihub/desisim/blob/master/etc/quickquasar_slurm_script.sh

#SBATCH -C haswell
#SBATCH --partition=debug
#SBATCH --account=desi
#SBATCH --nodes=40
#SBATCH --time=00:30:00
#SBATCH --job-name=lyasim
#SBATCH --output=lyasim.log

# HOWTO:
# 1) copy this script
# 2) choose your options to quickquasars (z range, downsampling, target selection, DESI footprint) in the command below
# 3) change idir/outdir, output, nodes, nthreads, time
# 4) verify nodes=XX below is same as --nodes=XX above
# 5) sbatch yourjob.sh
#
# example:
# for the Dec 20 tutorial set downsampling=0.1 to get ~270K quasars. 
# To get a  QSO density (z>2.1) ~ 50/deg2, using London mocks, set downsampling=0.4,

source /project/projectdirs/desi/software/desi_environment.sh master


seed=123
downsampling=0.1
idir=/global/cfs/projectdirs/desi/mocks/lya_forest/london/v9.0/v9.0.0
outdir=$SCRATCH/mocks/quickquasar/tutorial-0.3-4/
nodes=40 # CHECK MATCHING #SBATCH --nodes ABOVE !!!!
nthreads=4 # TO BE TUNED ; CAN HIT NODE MEMORY LIMIT ; 4 is max on edison for nside=16 and ~50 QSOs/deg2

if [ ! -d $outdir ] ; then
    mkdir -p $outdir
fi
if [ ! -d $outdir/logs ] ; then
    mkdir -p $outdir/logs
fi
if [ ! -d $outdir/spectra-16 ] ; then
    mkdir -p $outdir/spectra-16
fi

echo "get list of skewers to run ..."

files=`\ls -1 $idir/*/*/transmission*`
nfiles=`echo $files | wc -w`
nfilespernode=$((nfiles/nodes+1))

echo "n files =" $nfiles
echo "n files per node =" $nfilespernode

first=1
last=$nfilespernode
for node in `seq $nodes` ; do
    echo "starting node $node"

    # list of files to run
    if (( $node == $nodes )) ; then
        last=""
    fi

    echo ${first}-${last}
    tfiles=`echo $files | cut -d " " -f ${first}-${last}`
    first=$(( first + nfilespernode ))
    last=$(( last + nfilespernode ))
    command="srun -N 1 -n 1 -c $nthreads  quickquasars --exptime 4000. -i $tfiles --zmin 1.8 --nproc $nthreads --outdir $outdir/spectra-16 --downsampling $downsampling --zbest --bbflux --desi-footprint --metals-from-file --balprob 0.16 --dla file --add-LYB --seed $seed"
    echo $command
    echo "log in $outdir/logs/node-$node.log"

    $command >& $outdir/logs/node-$node.log &

done

wait
echo "END"
