""" Example4. Scattering

    run with
        $> mpirun -n 2 python <scipt name>
"""

from mpi4py import MPI
 
comm = MPI.COMM_WORLD  

rank = comm.Get_rank()
size = comm.Get_size()

num_int = 4

assert size==num_int, f"({num_int}) != ({size})"

if rank==0:
    data = [i for i in range(num_int)]
else:
    data = None

data = comm.scatter(data, root=0)
print(f'rank: {rank}, data:{data}')
