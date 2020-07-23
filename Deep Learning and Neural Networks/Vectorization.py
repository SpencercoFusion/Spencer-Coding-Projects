import numpy as np  
import time

def demonstrateVectorization():
    msperdimensionVec = 0
    msperdimensionFor = 0
    for t  in range(100):
        x = (t + 1) * 10000
        a = np.random.rand(x)
        b = np.random.rand(x)

        tic = time.time()
        c = np.dot(a, b)
        toc = time.time()
        msperdimensionVec += (1000* (toc - tic)) / x
        #print("vectorized: " + str(1000* (toc - tic)))
        #print("c: " + str(c))

        z = 0
        tic = time.time()
        for i in range(x):
            z += a[i] * b[i]
        toc = time.time()

        msperdimensionFor += (1000* (toc - tic)) / x
        #print("z: " + str(z))
        #print("for loop: " + str(1000*(toc - tic)))

    msperdimensionFor /= t
    msperdimensionVec /= t

    print("msperdimensionVec: " + str(msperdimensionVec))
    print("msperdimensionFor: " + str(msperdimensionFor))

