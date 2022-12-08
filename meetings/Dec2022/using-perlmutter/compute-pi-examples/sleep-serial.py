import time

def iotask(n):
    time.sleep(n)

n = 5

start = time.time()
iotask(n)
end = time.time()

print(end - start)


