#!/Users/albertolanaro/venv3/bin/python3
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lfilter

filename = './max_fitness.txt'

STEP = 100

n = 500
b = 1/n * np.ones(n)

plt.figure(1)
plt.title("Max fitness")
while True:
	data = np.loadtxt(filename, delimiter='\n')
	plt.plot(lfilter(b, 1, data)[n::STEP], 'b')
	plt.pause(1)
	plt.clf()


