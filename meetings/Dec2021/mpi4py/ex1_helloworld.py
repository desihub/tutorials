""" Example1. Print Hello World by rank 0, otherwise Hey.

    run with
        $> mpirun -n 2 python <scipt name>
"""

from mpi4py import MPI
 
comm = MPI.COMM_WORLD  

rank = comm.Get_rank()
size = comm.Get_size()

if rank==0:
    print(f"Hello World from {rank}")
else:
    print(f"Hey from {rank}")


