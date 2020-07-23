
import numpy as np 

def sigmoid(v):
    return(1/(1+np.exp(-v)))
Y = np.array([[0, 1]])
X = np.array([1.0, 2.0, 3.4, 4.5, 2.0, 2.1, 4.6, 4.0]).reshape((4, 2), order='F')
print(X)
w = np.array([.3, 0.4, -0.5, 0.4]).reshape((4, 1))
print(w)
A = sigmoid(np.dot(w.T, X))
print(Y)
print(A)
print(A-Y)
print(np.dot(X, (A-Y).T))
print(np.array(0).shape)

