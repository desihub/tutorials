# Using Perlmutter Tutorial

This tutorial will get you started on your journey to using the Perlmutter system at NERSC.

## Requirements

 * A NERSC account. 

## Connecting to NERSC

The objective of this section is to gain familiarity with connecting to NERSC.

Reference documentation:
 * [DESI Guide to NERSC Access](https://desi.lbl.gov/trac/wiki/Computing/AccessNersc)
 * [Connecting to NERSC](https://docs.nersc.gov/connect/)
 * [NERSC Multi-Factor Authentication](https://docs.nersc.gov/connect/mfa/)
 * [Jupyter at NERSC](https://docs.nersc.gov/services/jupyter/#jupyter)

### Connect via SSH

Log in to a Perlmutter login node using the `ssh` command from a terminal on your local computer.

```bash
> ssh <nersc-username>@perlmutter-p1.nersc.gov
```

#### NERSC sshproxy (optional but highly recommended!)

If you find yourself ssh'ing to NERSC multiple times per day, it may be helpful to setup [`sshproxy`](https://docs.nersc.gov/connect/mfa/#sshproxy). 
`sshproxy` will generate an ssh key with a 24 lifetime so you only have to enter your password + MFA code once per day.

### Connect via JupyterHub

Log in to [NERSC JupyterHub](https://jupyter.nersc.gov). Upon successful login, you will see the "Hub Control Panel".

Start a Jupyter server on a Perlmutter "Shared CPU node" by clicking the "Start" button located in the row labeled "Perlmutter" and column labeled "Shared CPU Node".

Launch a terminal by clicking on the "Terminal" button in the launcher window or by selecting "File -> New -> Terminal" from the menu bar at the top of the page.

At the end of your session, you can stop your Jupyter server from the "Hub Control Panel". To do so, navigate the "Hub Control Panel" in a new browser window or by selecting "File -> Hub Control Panel", then click the red "Stop" button.

### Exercises

 * What is the hostname of the server that you are connected to? 
 * What is the value of the `NERSC_HOST` environment variable?

## Filesystems at NERSC

There are multiple file systems available at NERSC. Each filesystem is configured and intended to be used for a different purpose. The main filesystems you will interact with are Global Home, Perlmutter Scratch, Community, and Global Common.

Reference documentation:
 * [NERSC Filesystems](https://docs.nersc.gov/filesystems/)
 * [DESI File Systems at NERSC](https://desi.lbl.gov/trac/wiki/Computing/NerscFileSystem)

### Global Home File System

Your home directory is useful for storing small files, scripts, notebooks, etc. Your home directory has a storage space quota of 40 GB.

Print the path of your home directory stored in the `$HOME` environment variable.

```bash
> echo $HOME
```

Use the `showquota` command to list the amount of storage space you are currently using on the Global Home File System.

### Perlmutter Scratch File System

Print the file system path of your scratch directory stored in the `$SCRATCH` environment variable.

```bash
> echo $SCRATCH
```

### Community File System (CFS)

List the contents of the DESI project directory on the Community Filesystem:

```bash
> ls /global/cfs/cdirs/desi
```

### Global Common Filesystem

The "Common" filesystem is typically used for installing software at NERSC.

The DESI Data Team provides a software environment that is used for processing DESI data at NERSC. The software is installed at `/global/common/software/desi`.

### Excercise

NERSC provides the `showquota` program for displaying your storage space usage and quota by filesystem. How much storage space are you currently using on the home file system?


## Running Jobs

NERSC uses the [Slurm workload manager](https://slurm.schedmd.com/) to manage access to compute resources. In this tutorial, we will use the `salloc` command to allocate resources for interactive CPU and GPU node jobs. We will also use the `srun` command to run certain parallel jobs.

Reference documentation:
 * [running jobs at NERSC](https://docs.nersc.gov/jobs/)

### Interactive jobs

Request an interactive session on a Perlmutter CPU node using the following command:

```bash
> salloc --constraint cpu --account desi --nodes 1 --qos interactive --time 30
```

To stop or quit your interactive job, run the `exit` command.

Here is the same interactive job request command written using short form options:

```bash
> salloc -C cpu -A desi -N 1 -q interactive -t 30
```

Request an interactive job on a Perlmutter GPU node

```bash
> salloc --constraint gpu --account desi --nodes 1 --gpus-per-node 4 --qos interactive -t 30
```

Again, here is the short form version of that command:

```bash
> salloc -C gpu -A desi -N 1 --gpus-per-node 4 -q interactive -t 30
```

Note that there is no short form equivalent of the `--gpus-per-node` option.

## Parallel Programming in Python at NERSC

This section introduces the basics of how to write parallel Python programs at NERSC.

High performant and parallel applications that are implemented using Python typically must find a way to bypass Python's [Global Interpreter Lock](https://docs.python.org/3/glossary.html#term-global-interpreter-lock) (GIL, pronounced "gill").
In short, the GIL simplifies the implementation of the Python interpreter by limiting what one can do with [threads](https://en.wikipedia.org/wiki/Thread_(computing)) in Python.
The limitations imposed by the GIL are usually bypassed by calling precompiled functions that are implemented in a lower level language such as C (by using something like [`ctypes`](https://docs.python.org/3/library/ctypes.html) or [`pybind11`](https://pybind11.readthedocs.io/en/stable/)) or by using multiple processes insteads of threads (by using something like [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html) or [`mpi4py`](https://mpi4py.readthedocs.io/en/stable/)).

### Pre-requisites

If you are new to Python and using Python to process data, it may be helpful to review the following resources to understand some of the syntax used in the code examples in this section.

 * [Python tutorial](https://docs.python.org/3/tutorial/)
 * [numpy quickstart guide](https://numpy.org/doc/stable/user/quickstart.html)
 * [numpy beginner's guide](https://numpy.org/doc/stable/user/absolute_beginners.html).

### Setup 

If you haven't already done so, download the DESI tutorials repository using `git clone` somewhere at NERSC, for example, into your `$SCRATCH` directory: 

```bash
> cd $SCRATCH
> git clone https://github.com/desihub/tutorials.git
```

Navigate to the `tutorials/meetings/Dec2022/using-perlmutter/data-task-examples` subdirectory:

```bash
> cd tutorials/meetings/Dec2022/using-perlmutter/data-task-examples
```

### Indirect Parallelism in Python

If you have experience using NumPy or SciPy, then you already have experience with parallel Python programming.

Consider the following Python code which computes an eigenvalue decomposition of a random symmetric positive definite matrix:

```python
import numpy as np

# construct a random symmetric positive definite matrix a
n = 1000 # size of 2D matrix
b = np.random.rand(n, n) # generate uniform random 2D matrix b
a = b.dot(b.T) # matrix multiply b with b's transpose

# compute eigenvalue decomposition
w, v = np.linalg.eigh(a)
```

It may not seem like it but that is an example of Python code that is capable of leveraging multi-core systems.
Under the hood, many [linear algebra methods in NumPy](https://numpy.org/install/#numpy-packages--accelerated-linear-algebra-libraries) use a [BLAS backend](https://en.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms) such as OpenBLAS or Intel MKL, which are capabable of using multiple threads.
The multithreading parallelism in the lower level backend used by NumPy is not constrained by Python's GIL.

Let's use Python's `timeit` module to benchmark the eigenvalue decomposition example on a Perlmutter CPU node.
The [`timeit`](https://docs.python.org/3/library/timeit.html) module is helpful for measuring the execution time of small snippets of code while avoiding common benchmarking pitfalls.

To begin, start an interactive job on a CPU node and load the python module.

```bash
> salloc -C cpu -A desi -N 1 -q interactive -t 30
> module load python
```

We'll use `timeit`'s `-s` option to specify the setup statements followed by the statement to benchmark.
`timeit` will execute the setup once and then execute the benchmark statement several times to obtain a measurement. Note the command should be a single line, with two sets statements enclosed by quotation marks. The first set contains the setup statements and the second set contains the statements we want to benchmark.

```bash
> python -m timeit -s "import numpy as np; n = 1000; b = np.random.rand(n, n); a = b.dot(b.T)" "np.linalg.eigh(a)"
```

That should result in output such as the following:

```bash
1 loop, best of 5: 427 msec per loop
```

Exercise: Try adjusting the value of `n` in the previous command. How does the performance vary with respect to the size of the matrix?

<!--- Answer
```bash
> for n in 10 20 50 100 200 500 1000 2000; do echo -n "n=$n | "; python -m timeit -s "import numpy as np; n = $n; b = np.random.rand(n, n); a = b.T @ b" "np.linalg.eigh(a)"; done
n=10 | 20000 loops, best of 5: 11.6 usec per loop
n=20 | 5000 loops, best of 5: 47.1 usec per loop
n=50 | 200 loops, best of 5: 1.01 msec per loop
n=100 | 100 loops, best of 5: 2.18 msec per loop
n=200 | 20 loops, best of 5: 13.3 msec per loop
n=500 | 1 loop, best of 5: 23 msec per loop
n=1000 | 1 loop, best of 5: 573 msec per loop
n=2000 | 1 loop, best of 5: 2.38 sec per loop
```
--->

Let's see what happens when we change the number of threads used by NumPy's BLAS backend.

NumPy's BLAS backends use multithreading parallelism via [OpenMP](https://en.wikipedia.org/wiki/OpenMP).
The number of threads used can be controlled by environment variables such as `OMP_NUM_THREADS`, the generic OpenMP environment variable, or `MKL_NUM_THREADS` and `OPENBLAS_NUM_THREADS`, which are backend specific environment variables respectively corresponding to MKL and OpenBLAS.
<!--- or controlled at runtime using a library such as [`threadpoolctl`](https://github.com/joblib/threadpoolctl). --->
<!--- 
The numpy installed in the default conda environment of the python module at NERSC is configured with Intel MKL as the backend.
Intel MKL uses the number of threads equal to the number of physical cores on the system by default.

```bash
> python -c 'import numpy as np; np.show_config()'
blas_mkl_info:
    libraries = ['mkl_rt', 'pthread']
    library_dirs = ['/global/common/software/nersc/pm-2022q2/sw/python/3.9-anaconda-2021.11/lib']
    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
    include_dirs = ['/global/common/software/nersc/pm-2022q2/sw/python/3.9-anaconda-2021.11/include']
blas_opt_info:
    libraries = ['mkl_rt', 'pthread']
    library_dirs = ['/global/common/software/nersc/pm-2022q2/sw/python/3.9-anaconda-2021.11/lib']
    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
    include_dirs = ['/global/common/software/nersc/pm-2022q2/sw/python/3.9-anaconda-2021.11/include']
lapack_mkl_info:
    libraries = ['mkl_rt', 'pthread']
    library_dirs = ['/global/common/software/nersc/pm-2022q2/sw/python/3.9-anaconda-2021.11/lib']
    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
    include_dirs = ['/global/common/software/nersc/pm-2022q2/sw/python/3.9-anaconda-2021.11/include']
lapack_opt_info:
    libraries = ['mkl_rt', 'pthread']
    library_dirs = ['/global/common/software/nersc/pm-2022q2/sw/python/3.9-anaconda-2021.11/lib']
    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
    include_dirs = ['/global/common/software/nersc/pm-2022q2/sw/python/3.9-anaconda-2021.11/include']
Supported SIMD extensions in this NumPy install:
    baseline = SSE,SSE2,SSE3
    found = SSSE3,SSE41,POPCNT,SSE42,AVX,F16C,FMA3,AVX2
    not found = AVX512F,AVX512CD,AVX512_KNL,AVX512_KNM,AVX512_SKX,AVX512_CNL
```
--->
In the following example, we run the same benchmark that we ran a moment ago but with different values of OMP_NUM_THREADS.
The `scan-num-threads.sh` bash script will run the benchmark, looping over values of OMP_NUM_THREADS.

```bash
> bash scan-num-threads.sh
nthreads=1 | n=1000 | 2 loops, best of 5: 188 msec per loop
nthreads=2 | n=1000 | 2 loops, best of 5: 126 msec per loop
nthreads=4 | n=1000 | 2 loops, best of 5: 117 msec per loop
nthreads=8 | n=1000 | 2 loops, best of 5: 94.9 msec per loop
nthreads=16 | n=1000 | 2 loops, best of 5: 85.4 msec per loop
nthreads=32 | n=1000 | 5 loops, best of 5: 98.3 msec per loop
nthreads=64 | n=1000 | 1 loop, best of 5: 327 msec per loop
nthreads=128 | n=1000 | 1 loop, best of 5: 468 msec per loop
nthreads=256 | n=1000 | 1 loop, best of 5: 446 msec per loop
```

Our earlier measurement of "427 msec" is close to the last step at nthreads=256. This happens to coincide with the number of logical cores on a Perlmutter CPU node. When the OMP_NUM_THREADS variable is not set, typically, the number of logical cores "available" to the process will be used. 

Note that the performance improves as we increase from nthreads=1 to nthreads=16, starts to degrade at nthreads=32, and then degrades significantly beyond that point.

<!---
This is getting ahead of ourselves a bit, but we can run the same application on a GPU (using CuPy) which takes about 18.5 msec.
The speedup factor between CPU/GPU would likely improve at larger matrix sizes.

```bash
> python -c 'import cupy as cp; from cupyx.profiler import benchmark; n = 1000; b = cp.random.rand(n, n); a = b.T @ b; print(benchmark(cp.linalg.eigh, (a,), n_repeat=5))'
eigh                :    CPU:16353.855 us   +/-1780.469 (min:13992.920 / max:17809.189) us     GPU-0:18412.544 us   +/-2086.878 (min:15674.368 / max:20120.577) us
```
--->

It's important to keep this indirect parallelism in mind as we begin to directly program with parallelism in Python.
The composibility of parallel components of a program can be a significant challenge to deal with, especially when those components are layered or nested.

### Data Parallel Problems in Python

A data parallel problem is one in which we want to apply the same computation to multiple independent data.
This is a frequently encountered class of problems encountered by scientists proccessing data from an instrument such as DESI.

Let's consider an example problem where we need to perform the same computation on several input data.
We'll reuse the code from the previous example. 
This time, we'll pretend we have many 2D matrices that we want to perform eigenvalue decomposition on.

The following code will be used to generate our data:

```python
data = list()
for i in range(ntasks):
    np.random.seed(i)
    b = np.random.rand(n, n)
    a = b.dot(b.T)
    data.append(a)
```

We will process individual units of our data with the following function:

```python
def process_data(i, a):
    w, v = np.linalg.eigh(a)
    return i, w
```

Our data processing function takes in an index and and the input matrix. It returns the index of the input data and the array of eigenvalues computed. It can be useful to pass along the index of the input data or some other unique identifier in case the tasks are processed out of order and we want the output data to be in a particular order later on.

We'll also try to ignore indirect parallelism in NumPy by setting `OMP_NUM_THREADS=1` in the examples below.

### Serial `for`-loop

We can process are data serially (in order) using a Python `for`-loop like so: 

```python
results = []
for i in range(ntasks):
    results.append(process_data(i, data[i]))
```

The serial `for`-loop solution to this problem is implemented in `data-serial.py`.

When we run this example, we measure a wall clock time of about 29 seconds (measured by prepending `time` to our command).
The progress bar reports a work rate of 5.21 iterations per second (192 msec per iteration) which roughly corresponds to the performance we measured earlier with nthreads=1.

```bash
> OMP_NUM_THREADS=1
> time python data-serial.py
serial
n=1000 ntasks=128
100%|█████████████████████████████████████████| 128/128 [00:24<00:00,  5.21it/s]
completed all tasks!

real	0m28.969s
user	0m28.464s
sys	0m0.344s
```

The progress bar reports a work rate of 5.21 iterations per second (192 ms per iteration) is pretty close to the 190 ms measurement at nthreads=1 from the previous section.
We changed the method we are using to measure the performance of the data processing task so this is a reassuring check that we have not introduced a bias in to our benchmark.


### Process-based parallelism with Python's multiprocessing

Now let's write the parallelism directly using the [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) library which is part of the Python Standard Libary.
We'll use a `multiprocessing.Pool` object to spawn a group of worker processes and map our set of tasks onto that group of workers.

```python
results = []
# create a pool of nproc workers
with multiprocessing.Pool(processes=nproc) as pool:
    results = pool.starmap(process_data, enumerate(data))
```

By spawning new Python processes, multiprocessing bypasses the GIL limitation that we would encounter using threads within single Python process.

Let's run the implemention in `data-multiprocessing.py`. First, run this using a single process:

```bash
> OMP_NUM_THREADS=1
> time python data-multiprocessing.py --nproc 1
multiprocessing
n=1000 ntasks=128 nproc=1
100%|█████████████████████████████████████████| 128/128 [00:25<00:00,  5.06it/s]
completed all tasks!

real	0m29.663s
user	0m29.274s
sys	0m0.886s
```

The performance is similar to the previous example, perhaps a little slower due to multiprocessing overhead.
Let's run this again increasing the number of processes:

```bash
> OMP_NUM_THREADS=1
> time python 1-multiprocessing.py --nproc 4
multiprocessing
n=1000 ntasks=128 nproc=4
100%|█████████████████████████████████████████| 128/128 [00:06<00:00, 18.29it/s]
completed all tasks!

real	0m11.752s
user	0m31.486s
sys	0m1.492s
```

Using 4 processes results in nearly a 4x speedup for the data processing step (18.29it/s compared to 5.06it/s). Note that if we look at the overall runtime we only observe a ~2.5x speedup (30s compared to 12s).

Exercise: How does the performance change as you continue increasing the number of processes?

<!--- Answer

It improves but starts to taper off.

Possible explanations:
 * communication or startup overhead of multiple processes
 * resource contention

--->


### MPI-based parallelism with mpi4py

In Python, the most common way to use [MPI](https://docs.nersc.gov/development/programming-models/mpi/) is through the [`mpi4py` library](https://mpi4py.readthedocs.io/en/stable/intro.html).

In the multiprocessing example, we launched a single process to run our program which dynamically spawned new processes to execute a single function. Here, we will use MPI to launch a fixed number of processes at the that will each execute the same program.

MPI programs must be launched with a special launcher program which is typically something like `mpirun` or `mpiexec`.
At NERSC, we recommend using the [`srun` SLURM command](https://docs.nersc.gov/jobs/#srun) to launch MPI programs.

The MPI version of our example is implemented in `data-mpi4py.py`. If you're unfamiliar with MPI, it look a bit confusing at first. Each process is executing the same program. MPI functions provide a common set of functions that those process can use to send messages to each other and coordinate work. Often, we use control structures such as `if-else` statements and `for` that behave differently depending on the processes MPI rank. 

In the example implementation here, the "root" MPI rank (rank 0) is responsible for generating all the input data. It "broadcasts" that data out to other ranks and then each rank processes a subset of the data. Finally, the data is "gathered" back to the "root" rank which is responsible for printing out a summary and verifying that the correct number of tasks were performed.

```bash
> export OMP_NUM_THREADS=1
> time srun -n 4 -c 2 --cpu-bind=cores python data-mpi4py.py
mpi4py
n=1000 ntasks=128 size=4
Processed 128 tasks in 7.17s (17.84it/s)
completed all tasks!

real    0m12.639s
user    0m0.043s
sys     0m0.018s
```

Exercise: Find the optimal number of MPI tasks for this example by changing the value specified by `-n`.

<!--- Answer
Performance peaks around 32 MPI tasks.
--->

<!---
(This is the first time we've used srun. Capture start-up time? mpi init? I assume that is why this is slower than the previous implementations)
--->

The MPI implementation seems significantly more complicated than the multiprocessing implementation. Is that complexity worth it?

### Multi-node parallelism with mp4py

One of the main reasons MPI is popular is that is can scale out to multiple nodes. We can reuse the previous example, this time running our application on more than a single node.

Request an interactive job with two CPU nodes (exit from your current interactive allocation first):

```bash
> salloc -C cpu -A nstaff -N 2 -q interactive -t 60
> module load python
```

Launch with two nodes, four MPI tasks per node:

```bash
> export OMP_NUM_THREADS=1
> time srun -N 2 --ntasks-per-node 4 -c 2 --cpu-bind=cores python 2-mpi4py.py
mpi4py
n=1000 ntasks=128 size=8
Processed 128 tasks in 4.37s (29.26it/s)
completed all tasks!

real	0m11.210s
user	0m0.019s
sys	0m0.023s
```

### GPU-based parallelism with CuPy

Let's hop over to a GPU node: 

```bash 
> salloc -C gpu -A desi -N 1 --gpus-per-node 4 -q interactive -t 30
```

Next, create a new environment with [CuPy](https://docs.cupy.dev/en/stable/overview.html), a NumPy/SciPy-compatible library for GPU-accelerated computing with Python.
The following instructions are based on the instruction in the [Perlmutter Python NERSC documentation](https://docs.nersc.gov/development/languages/python/using-python-perlmutter/#guide-to-using-python-on-perlmutter).

```bash
module load python
conda create -n using-perlmutter-gpu python=3.9 pip numpy scipy tqdm
conda activate using-perlmutter-gpu
pip install cupy-cuda11X
MPICC="cc -target-accel=nvidia80 -shared" pip install --force --no-cache-dir --no-binary=mpi4py mpi4py
```

The CuPy implementation in `data-cupy.py` is nearly identical to the serial implementation that we started with. The main difference is that we generate our data in GPU memory using the CuPy API instead of in CPU memory like we did earlier using NumPy. Typically, you would read in some data from a filesystem to CPU memory first and then move it over to GPU memory.

```bash
> time python data-cupy.py
cupy
n=1000 ntasks=128 device_pci_bus_id='0000:C3:00.0'
100%|█████████████████████████████████████████| 128/128 [00:02<00:00, 62.25it/s]
completed all tasks!

real	0m3.471s
user	0m6.155s
sys	0m10.462s
```

This is about 10x faster than the CPU version.

Note that `process_data` function is identical to the serial-version and uses the NumPy API.
The `numpy.linalg.eigh` method in the NumPy API detects that the input data is a CuPy ndarray and calls out to CuPy's `cupy.linalg.eigh` method instead.


### Multi-GPU parallelism with CuPy + mpi4py

This example demonstrates how to combine CuPy with mpi4py to share GPU data directly between GPUs without passing through CPU memory.

Note that CUDA-aware MPI is enabled by default on Perlmutter

```bash
> time srun -n 4 -c 2 --cpu-bind=cores --gpus-per-node=4 python data-cupy-mpi4py.py
rank=0 device_pci_bus_id='0000:03:00.0'
rank=3 device_pci_bus_id='0000:C1:00.0'
rank=1 device_pci_bus_id='0000:41:00.0'
rank=2 device_pci_bus_id='0000:81:00.0'
cupy-mpi4py
n=1000 ntasks=128 size=4
Processed 128 tasks in 1.14s (112.31it/s)
completed all tasks!

real    0m6.320s
user    0m0.034s
sys     0m0.011s
```

