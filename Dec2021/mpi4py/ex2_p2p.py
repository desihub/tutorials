""" Example2. Point to Point Communication

    run with
        $> mpirun -n 2 python <scipt name>
"""

from mpi4py import MPI
 
comm = MPI.COMM_WORLD  

rank = comm.Get_rank()
size = comm.Get_size()

assert size>3, "this example requires at least 3 processes"

if rank==0:
    data = {'survey':'desi', 'year':2021}
    comm.send(data, dest=1)

    data = {'survey':'jwst', 'year':2025}
    comm.send(data, dest=2)

if rank in [1, 2]:
    data = comm.recv(source=0)
    print(f"rank:{rank}, data:{data}")

