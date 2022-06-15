'''
    Pi with a trapzoidal method
    no MPI

    (c) Mehdi Rezaie
'''
from time import time
import numpy as np

def f(x):
    return 4.0/(1.0+x*x)

def trap(local_a,local_b,local_n,h):
    estimate = (f(local_a)+f(local_b))/2.0
    for i in np.arange(1,local_n):
        x = local_a+float(i)*h
        estimate += f(x)
    #
    estimate *= h
    return estimate


start = time()

b = 1.0
a = 0.0
n = 10000000
h = (b-a)/float(n)
total_int = trap(a,b,n,h)
end = time()
print("Pi with %d steps is %f in %f secs" %(n, total_int, end-start))
