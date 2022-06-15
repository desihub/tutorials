""" Example5. Gathering

    run with
        $> mpirun -n 2 python <scipt name>
"""

from mpi4py import MPI
 
comm = MPI.COMM_WORLD  

rank = comm.Get_rank()
size = comm.Get_size()

data = [rank, rank*rank]
print(f"before gather, rank: {rank}, data: {data}")

comm.Barrier()
data = comm.gather(data, root=0)

if rank==0:
    for i in range(size):
        assert data[i] = [i, i*i]
else:
    assert data is None

print(f"after gather, rank: {rank}, data: {data}")

