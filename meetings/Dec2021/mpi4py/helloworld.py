'''
    Example of MPI Hello
    (c) Mehdi Rezaie

'''

from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
name = MPI.Get_processor_name()


print("Hi from rank {}".format(rank))

comm.Barrier()  # keep all processes

if rank ==0:
    print("Hello from rank {} from size {} on {}".format(rank, size, name))


