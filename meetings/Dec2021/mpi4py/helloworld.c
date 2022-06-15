/*
    Example of Hello World using C

    Author: Mehdi Rezaie
    medirz90@icloud.com

*/

#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {

    MPI_Init(NULL, NULL);

    int size;
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    char processor_name[MPI_MAX_PROCESSOR_NAME];

    int name_len;
    MPI_Get_processor_name(processor_name, &name_len);

    if (rank == 0)
    {
         printf("Hello world from processor %s, rank %d out of %d processors\n",
                  processor_name, rank, size);
     }
     else{
         printf("Goodbye world from processor %s, rank %d out of %d processors\n",
                  processor_name, rank, size);
     }
    MPI_Finalize();
}
