import numpy as np
import time,sys

# This script emullates a job that takes around 30 seconds to run.
print("Hello! Welcome to the tutorial.")
print("I'm currently working :)")
for i in range(5):
    print(f"Iteration {i} of 5"),
    sys.stdout.flush()
    time.sleep(6)
print("Thanks for your patience!")
print("done")