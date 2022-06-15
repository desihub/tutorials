'''
 python pi_mpi.py
 (c) Mehdi Rezaie
 mpirun -np 5 python pi_mpi_p2p.py
'''

from time import time
import numpy as np

def f(x):
    return 4.0/(1.0+x*x)

def trap(local_a,local_b,local_n,h):
    estimate = (f(local_a)+f(local_b))/2.0
    for i in np.arange(1,local_n):
        x = local_a+float(i)*h
        estimate += f(x)
    #
    estimate *= h
    return estimate


from mpi4py import MPI
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank ==0:start = time()

b = 1.0
a = 0.0
n = 10000000
h = (b-a)/float(n)

local_n = int(n/size)
local_a = a+rank*float(local_n)*h
local_b = local_a+float(local_n)*h


local_int = trap(local_a,local_b,local_n,h)

if rank != 0:
   comm.send(local_int,dest=0,tag = 0)
else:
   total_int = local_int
   for node in np.arange(1,size):
       local_int = comm.recv(source=node,tag=0)
       total_int += local_int

comm.Barrier()

if rank == 0:
   end = time()
   print("Pi with %d steps is %f in %f secs" %(n, total_int, end-start))
