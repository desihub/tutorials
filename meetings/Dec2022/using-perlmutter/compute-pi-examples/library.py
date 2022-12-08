import random
import math

def estimate_pi(n):
    c = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        if math.sqrt(x*x + y*y) < 1:
            c += 1
    return c * 4.0 / n
