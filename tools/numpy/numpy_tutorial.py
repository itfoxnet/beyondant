#!/usr/bin/env python
import numpy
from numpy import *
from numpy.linalg import *
import pylab
import matplotlib.pyplot as plt
def array_basics() :
  print "ary = arange(15).reshape(3, 5)"
  ary = arange(15).reshape(3, 5)
  print "ary=", ary
  print "ary.shape=", ary.shape
  print "ary.dim=", ary.ndim
  print "ary.size=", ary.size
  print "type(ary)=", type(ary)
  print "ary.dtype.name=", ary.dtype.name

def array_creation() :
  print "ary = array([1, 3, 8])"
  ary = array([1, 3, 8])
  print ary

  print "ary = array([(1, 3, 8), (2, 8, 9)])"
  ary = array([(1, 3, 8), (2, 8, 9)])
  print ary

  print "ary = zeros((5, 7, 8), dtype=int16)"
  ary = zeros((5, 7, 8), dtype=int16)
  print ary 

  print "ary = ones((5, 7, 8), dtype=int16)"
  ary = ones((5, 7, 8), dtype=int16)
  print ary 

  print "ary = empty((5, 7, 8), dtype=int16)"
  ary = empty((5, 7, 8), dtype=int16)
  print ary 

def array_operation() :
  print "a = array([20, 30, 40, 50])"
  a = array([20, 30, 40, 50])
  print "b = arange(4)"
  b = arange(4)
  print "b=", b
  c = a - b
  print "a-b=", c
  print "b**2=", b**2
  print "sin(a)=", sin(a)
  print "a*10=", a*10
  print "a>35:", a>35

  a = ones((2, 2))
  b = ones((2, 2))
  print "a=", a
  print "b=", b
  print "a*b=", a * b
  print "dot(a,b)=", dot(a, b)

def linear_algebra() :
  print "a = array([[1.0, 2.0], [3.0, 4.0]])"
  a = array([[1.0, 2.0], [3.0, 4.0]])
  print "a.transpose()=", a.transpose()
  print "inv(a)=", inv(a)
  print "eye(2)=", eye(2)
  print "j = array([[0.0, -1.0], [1.0, 0.0]])"
  j = array([[0.0, -1.0], [1.0, 0.0]])
  print "dot(j,j)=", dot(j, j)

def matrix() :
  print "A = mat([[1.0,2.0],[3.0,4.0]])"
  A = mat([[1.0,2.0],[3.0,4.0]])
  print "type(A)=", type(A)
  print "A.T=", A.T
  print "A.I=", A.I
  print "X = mat([5.0, 7.0])"
  X = mat([5.0, 7.0])
  print "Y=X.T"
  Y = X.T
  print "Y=", Y
  print "A*Y=", A*Y
  print "solve(A,Y)=", solve(A,Y)

def histograms():
  # Build a vector of 10000 normal deviates with variance 0.5^2 and mean 2
  mu, sigma = 2, 0.5
  v = numpy.random.normal(mu,sigma,10000)
  # Plot a normalized histogram with 50 bins
  pylab.hist(v, bins=50, normed=1)       # matplotlib version (plot)
  pylab.show()

  # Compute the histogram with numpy and then plot it
  (n, bins) = numpy.histogram(v, bins=50, normed=True)  # NumPy version (no plot)
  pylab.plot(.5*(bins[1:]+bins[:-1]), n)
  pylab.show()

  plt.plot(bins, 1/(sigma*numpy.sqrt(2*numpy.pi))*
                 numpy.exp(-(bins-mu)**2 / (2*sigma**2)),
                 linewidth=2, color='r')
  plt.show()

if __name__ == '__main__' :
  array_basics()
  array_creation()
  array_operation()
  linear_algebra()
  histograms()
  matrix()
