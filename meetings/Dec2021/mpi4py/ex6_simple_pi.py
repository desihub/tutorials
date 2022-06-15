""" Example6. Calculate Pi (3.1415..) with a simple 
    code based on trapzoidal method.

    run with
        $> python <scipt name>
"""
import numpy as np
from time import time

def f(x):
    return 4.0/(1.0+x*x)

def trap(local_a,local_b,local_n,h):
    # trapzoidal method
    estimate = (f(local_a)+f(local_b))/2.0
    for i in np.arange(1,local_n):
        x = local_a+float(i)*h
        estimate += f(x)
    return estimate*h

b = 1.0
a = 0.0
n = 1000000
h = (b-a)/float(n)

start = time()
pi = trap(a, b, n, h)
end = time()

print(f'Pi=%.6f (true)'%np.pi)
print("Pi=%.6f (%d steps in %.3f secs)" %(pi, n, end-start))
