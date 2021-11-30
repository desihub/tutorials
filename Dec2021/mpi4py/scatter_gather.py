'''
    Scatter Gather

    (c) Mehdi Rezaie
'''
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
   data = [(i+1)**2 for i in range(10)]
   print('generated data set is: ',data)
   data = [data[:5],data[5:]]
else:
   data = None

data = comm.scatter(data, root=0)


print("data on rank %d is: "%comm.rank, data)
if rank != 0:
   data = [2*d for d in data]

comm.Barrier()
data = comm.gather(data, root=0) 

if rank == 0:
    data = [d for di in data for d in di]
    for i in range(5, 10):
        assert data[i] == 2*(i+1)**2          
else:
    assert data is None

print("data on rank: %d is: "%rank, data)
