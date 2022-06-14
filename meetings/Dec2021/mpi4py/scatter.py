'''
    Scatter

    (c) Mehdi Rezaie
'''

from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
   data = [(i+1)**2 for i in range(size)]
   print('generated data set is: ',data)
else:
   data = None

data = comm.scatter(data, root=0)
assert data == (rank+1)**2

print("data on rank %d is: "%comm.rank, data)
