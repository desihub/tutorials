'''
    Example of brodcasting
    (c) Mehdi Rezaie

'''

import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    # create a data
    data = {
            'key1' : [10, 10.1, 10+11j],
            'key2' : ('Mehdi' , 'Rezaie'),
            'key3' : np.array([1, 2, 3]),
            'key4' : True
            }
else:
    data = None

data = comm.bcast(data, root=0)  # broadcast

if rank == 0:print("bcast finished")

print("data on rank {} is : {}".format(comm.rank, data))
