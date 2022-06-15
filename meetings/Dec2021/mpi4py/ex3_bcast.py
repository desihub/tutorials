""" Example3. Broadcasting

    run with
        $> mpirun -n 2 python <scipt name>
"""

from mpi4py import MPI
 
comm = MPI.COMM_WORLD  

rank = comm.Get_rank()
size = comm.Get_size()

if rank==0:
    data = {'a':[1, 2, 3], 
            'b':2.+3j,
            'c':'this is a sentence!'}
else:
    data = None

print(f'before bcast rank: {rank}, data: {data}')
data = comm.bcast(data, root=0)
print(f'after bcast rank: {rank}, data: {data}')
