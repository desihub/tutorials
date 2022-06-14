'''
	example of gathering
    (c) Mehdi Rezaie

'''


from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()



# create data 
data = [(rank+1)**2, rank**2]

print("before gather, data on rank %d is: "%rank, data)

comm.Barrier()
data = comm.gather(data, root=0)

if rank == 0:
   for i in range(size):
       assert data[i] == [(i+1)**2,i**2]
else:
    assert data is None

print("data on rank: %d is: "%rank, data)
