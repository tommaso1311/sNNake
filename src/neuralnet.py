import numpy as np

class neuralnet:
	"""
	Class used to create the neural network controlling snakes

	Attributes
	----------
	shape : tuple
		shape of the neural network
		shape[0] is the number of inputs
		shape[-1] is the number of outputs
		shape[1:-1] are the number of perceptrons for each layer
	weights : list
		list of neural weights between each layer

	Methods
	-------
	weights_creator()
		creates a new list with random weights between -1 and 1
	get_output(inputs)
		computes weights matrices product to get neural network output
	"""

	def __init__(self, shape, new=True, weights=None):

		assert type(shape) is list, "Incorrect shape type (must be a list)"
		for e in shape:
			assert isinstance(e, int)
		assert len(shape) >= 2, "Incorrect shape lenght (must be at least 2)"
		assert isinstance(new, bool), "Incorrect value for new parameter"

		self.shape = shape
		self.weights = []

		if new:
			self.weights = self.weights_creator()
		else:
			assert isinstance(weights, list)
			assert len(weights) == len(shape)-1
			for element in weights:
				assert isinstance(element, np.ndarray)
			for i in range(len(shape)-1):
				assert weights[i].shape == (shape[i+1], shape[i])

			self.weights = weights


	def weights_creator(self):

		weights = []

		for i in range(len(self.shape)-1):

			matrix = np.random.uniform(-1, 1, size=(self.shape[i+1], self.shape[i]))
			weights.append(matrix)

		return weights


	def get_output(self, inputs):
		"""
		Parameters
		----------
		inputs : array
			array of input to feed to the neural network
		"""

		assert len(inputs.shape) == 1
		assert inputs.shape[0] == self.weights[0].shape[1]

		outputs = self.weights.copy()
		outputs.insert(0, inputs)

		for i in range(len(outputs)-1):

			outputs[i+1] = np.tanh(outputs[i+1]@outputs[i])

		return outputs[-1]