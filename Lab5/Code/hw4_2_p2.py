import sys
import numpy as np

ks = np.array(sys.argv[2:], dtype = np.int32) # Get k input
f = open(sys.argv[1], "r") # Open "stream.txt"

for k in ks: # Print each number of 1's in the last k bit
    data = []
    n = 0
    m = 0

    for i in range(k): # Get last k bit
        data.append(f.readline())

    data = np.array(data, dtype = np.int32)

    for i in data: # Get number of 1's (n)
        if i == 1:
            n = n + 1

    if n == 0: # for dealing exception when the number of 1's is 0 
        n = 1

    # Get the number of bit of the number of 1's (m)
    while n > 0:
        n = n - 2**m
        m = m + 1    
    m = m-1

    # Get the estimate (s)
    s = 2**m/2.0
    for i in range(m):
        s = s + 2**i

    print(s) # Print the estimate
    f.seek(0)


f.close()
