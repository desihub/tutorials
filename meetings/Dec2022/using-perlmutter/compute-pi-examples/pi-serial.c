// Example usage: 
//    > gcc -o pi-serial-c pi-serial.c
//    > ./pi-serial-c
//
// Example output:
//    Result: 3.141237
//    Elapsed time: 0.294798
//
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double drandom() {
    // Generate a uniform random number [0, 1).
    return (double) rand() / RAND_MAX;
}

double estimate_pi(unsigned long n) {
    unsigned long m = 0;
    double x, y;
    for(int i = 0; i < n; ++i) {
        x = drandom();
        y = drandom();
        if (sqrt(x*x + y*y) < 1.0) m++;
    }
    return (double) m * 4.0 / (double) n;
}

int main() {
    unsigned long n = 20 * 1000 * 1000;

    clock_t start = clock();
    double result = estimate_pi(n);
    clock_t end = clock();
    double elapsed_time = (double) (end - start) / CLOCKS_PER_SEC;
    printf("Result: %f\n", result);
    printf("Elapsed time: %f\n", elapsed_time);
    return 0;
}
