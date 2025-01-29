# Exercises for How to Use NERSC Effectively Tutorial

Stephen Bailey<br>
December 2023 Hawaii Collaboration Meeting

See [DESI-8059](https://desi.lbl.gov/DocDB/cgi-bin/private/ShowDocument?docid=8059) for tutorial slides.

Solutions for each exercise are in the solutions/ subdirectory, but
you are highly encouraged to try solving the exercises yourself before
looking at the solutions.

## Getting started

On perlmutter.nersc.gov, setup a python environment that has
numpy, scipy, and astropy, e.g.
```
source /global/cfs/cdirs/desi/desi_environment.sh main

-or-

source /global/common/software/desi/users/adematti/cosmodesi_environment.sh main
```

Get a copy of the DESI tutorials
```
mkdir -p $CFS/desi/users/$USER
cd $CFS/desi/users/$USER
git clone https://github.com/desihub/tutorials
cd meetings/Dec2023/NERSC
```

Get an interactive node
```
salloc -N 1 -C cpu -t 02:00:00 -q interactive
```

## Exercise 1: Adding parallelism

`exercise1.py` is a non-parallelized code to process coadded spectra
files.  It reads the `R_FLUX` HDU, and subtracts a median-filtered
continuum from each spectrum and prints the amount of read time + processing
time.  It doesn't write any output; this is just a toy example.  e.g.
```
python exercise1.py /dvs_ro/cfs/cdirs/desi/spectro/redux/fuji/tiles/cumulative/338/20210414/coadd-8-338-thru20210414.fits

coadd-8-338-thru20210414.fits 0.5 + 0.6 sec
Total time 1.1 sec
```

The file `coaddfiles.txt` has a list of 128 coadd files;
processing these serially would take 1-2 minutes.
```
python exercise1.py $(cat coaddfiles.txt)
```
Note: The `$(cat coaddfiles.txt)` syntax just converts the contents of
coaddfiles.txt into command line arguments.

### Exercise 1a: GNU parallel

Use GNU parallel to run example1.py on all input files in coaddfiles.txt.

Hint: See tutorial slide 8.

This should run in 10-15 seconds for all files.

### Exercise 1b: multiprocessing

Make a copy of exercise1.py and update it to use multiprocessing.
This can process all files in 2-5 seconds.

Hint: See tutorial slides 9-11.

Bonus: did you try parallelizing over files or over spectra within a file?
Try implementing the other form of parallelism.  Which was faster?

### Exercise 1c: MPI

Make a copy of exercise1.py and update it to use MPI.  This would be run with an
`srun` prefix like:
```
srun -n 128 -c 2 python exercise1_mpi.py $(cat coaddfiles.txt)
```
This can process all files in 2-5 seconds.

Hint: See tutorial slides 14-15.

### Exercise 1 Discussion

Which parallelism method ran fastest?  Which did you find easiest to implement?

## Exercise 2: Tuning parallelism

In this exercise we'll study the tradeoffs on different levels of parallelism,
using MPI + multiprocessing.

`exercise2.py` is similar to `exercise1.py`, but it uses MPI to parallelize
over input files, and multiprocessing to parallelize over spectra within a file.
It includes command line options to load the list of input files and how many
multiprocessing processes to use.  Run it like
```
srun -n 32 -c 8 python exercise2.py --filelist coaddfiles.txt --nproc 4
```
That will use 32 MPI ranks to process 32 files in parallel, and for each
file it will use 4 multiprocessing processes to work on 4 spectra in parallel
(out of 500 per file).  We chose 32x4=128 to match the number of physical cores.

Note 1: in this case multiprocessing over spectra has enough overhead that it
would be faster to not parallelize that at all, but this is a toy example
to study parallelism tradeoffs.

Note 2: srun+starting python can have an overhead of up to a minute depending
upon the load at NERSC, which gets in the way of timing toy examples like this.
For this study, just use the "Total time" reported by the script itself,
not the actual wallclock time.

Try running this with different levels of MPI vs. multiprocessing parallelism
while keeping the total number of cores constant, and -c twice as large as
--nproc, e.g.
```
srun -n   8 -c 32 python exercise2.py --filelist coaddfiles.txt --nproc 16
srun -n  16 -c 16 python exercise2.py --filelist coaddfiles.txt --nproc 8 
srun -n  32 -c  8 python exercise2.py --filelist coaddfiles.txt --nproc 4
srun -n  64 -c  4 python exercise2.py --filelist coaddfiles.txt --nproc 2
srun -n 128 -c  2 python exercise2.py --filelist coaddfiles.txt --nproc 1
```

Record the time for each run and compare.  What combination was most effective?

### Exercise 2 Discussion 

You probably got something like
```
MPI x nproc  Runtime
-----------  -------
  8 x 16     550
 16 x  8     256
 32 x  4     124
 64 x  2     65
128 x  1     28
```

This case was constructed to be especially "unfair" to multiprocessing,
but it shows a >10x performance difference just by changing the balance
of how the cores are used, without changing the code itself at all!

### Exercise 2 Bonus 1 - hyperthreading

The Perlmutter CPUs have 2x hyperthreading, which allows you to run 2x more
processes than there are physical cores (128).
Try running `exercise2.py --nproc 1` which turns off multiprocessing, and
compare performance when using 128 MPI ranks (the number of physical CPU cores)
vs. 256 (with 2x hyperthreading).  Did using hyperthreading help?

```
srun -n 128 -c 2 python exercise2.py --filelist coaddfiles.txt --nproc 1
srun -n 256 -c 1 python exercise2.py --filelist coaddfiles.txt --nproc 1
```

### Exercise 2 Bonus 2 - multiple nodes

Log out of your current interactive session and get a new one with 2 nodes.
We'll check whether using 2 nodes runs faster, and whether it runs enough
faster to be worth being charged for 2 nodes instead of 1.

```
# get a new interactive session with 2 nodes
salloc -N 2 -C cpu -t 01:00:00 -q interactive

# run on 1 node
srun -N 1 -n 128 -c 2 python exercise2.py --filelist coaddfiles.txt --nproc 1

# run twice as many ranks, spread across 2 nodes
srun -N 2 -n 256 -c 2 python exercise2.py --filelist coaddfiles.txt --nproc 1
```

*Discussion*: running on 2 nodes was probably faster, but probably not 2x faster
to fully compensate for being charged for 2x more nodes.  If it is close to
the same number of node-hours charged, the faster wall-clock time my be worth
your human time.  But for larger runs, optimizing how many nodes should be
used per job can save thousands of node-hours being charged.

## Exercise 3

Apply these methods to your own code, either to add parallelism, or to study
what parallelism parameters are optimal for your code before you do your
next big run.

If you add parallelism and it still doesn't run faster, something is wrong.
Reach out for help and keep working on it before proceeding with big runs.

If you are already parallelized and changing parallelism parameters doesn't
have a big effect, that's ok. This is worth a few hours of testing with
various parameters, but if you don't see big differences then it's ok to
proceed with your big runs.  Or maybe your will find a big speedup!



