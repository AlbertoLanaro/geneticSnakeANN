import numpy as np

def sigmoid(x):

	return 1 / (1 + np.exp(-x))

def softmax(x):
	x_exp = np.exp(x)

	return x_exp /np.sum(x_exp)

def relu(x):

	return np.maximum(x, np.zeros_like(x))
