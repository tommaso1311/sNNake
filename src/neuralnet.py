import numpy as np

class neuralnet:
	"""
	Class used to create the neural network controlling snakes
	"""

	def __init__(self, shape, new=True):

		assert type(shape) is tuple, "Incorrect shape type (must be a tuple)"
		assert len(shape) >= 2, "Incorrect shape lenght (must be at least 2)"

		self.shape = shape
		self.weights = []

		if new:
			self.weights = self.weights_creator()


	def weights_creator(self):

		weights = []

		for i in range(len(self.shape)-1):

			matrix = np.random.uniform(-1, 1, size=(self.shape[i+1], self.shape[i]))
			weights.append(matrix)

		return weights


	def get_output(self, inputs):

		outputs = self.weights.copy()
		outputs.insert(0, inputs)

		for i in range(len(outputs)-1):

			outputs[i+1] = np.tanh(outputs[i+1].dot(outputs[i]))

		return outputs[-1]