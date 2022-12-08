from threading import Thread
import time

def iotask(n):
    time.sleep(n)

n = 5
p = 4

t = [
    Thread(target=iotask, args=(n/p,)) 
    for i in range(p)
]

start = time.time()
[t[i].start() for i in range(p)]
[t[i].join() for i in range(p)]
end = time.time()

print(end - start)


