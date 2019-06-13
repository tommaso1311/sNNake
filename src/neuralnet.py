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
		"""
		Parameters
		----------
		shape : tuple
			shape of the neural network
			shape[0] is the number of inputs
			shape[-1] is the number of outputs
			shape[1:-1] are the number of perceptrons for each layer
		new : bool
			tells if the neural network is new
		weights : list || None
			list of neural weights between each layer
		"""

		assert isinstance(shape, list), "Expected a list, received a " + type(shape).__name__
		for e in shape:
			assert isinstance(e, int), "Expected an int, received a " + type(e).__name__
		assert len(shape) >= 2, "Incorrect shape lenght (must be at least 2)"
		assert isinstance(new, bool), "Expected a bool, received a " + type(new).__name__

		self.shape = shape
		self.weights = []

		if new:
			self.weights = self.weights_creator()
		else:
			assert isinstance(weights, list), "Expected a list, received a " + type(weights).__name__
			assert len(weights) == len(shape)-1, "Incorrect weights length"
			for element in weights:
				assert isinstance(element, np.ndarray), "Expected a np.ndarray, received a " + type(element).__name__
			for i in range(len(shape)-1):
				assert weights[i].shape == (shape[i+1], shape[i]), "Incorrect weights shape"

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

		assert len(inputs.shape) == 1, "Incorrect input shape"
		assert inputs.shape[0] == self.weights[0].shape[1], "Incorrect input or weights shape"

		outputs = self.weights.copy()
		outputs.insert(0, inputs)

		for i in range(len(outputs)-1):

			# matrix multiplication between each element
			outputs[i+1] = np.tanh(outputs[i+1]@outputs[i])

		return outputs[-1]