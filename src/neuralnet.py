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
	decide(direction, status, directions)
		decides the new direction
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

		if not isinstance(shape, list):
			raise TypeError("Expected a list, received a " + type(shape).__name__)

		for e in shape:
			if not isinstance(e, int):
				raise TypeError("Expected an int, received a " + type(e).__name__)
		if not len(shape) >= 2:
			raise ValueError("Incorrect shape lenght (must be at least 2)")
		if not isinstance(new, bool):
			raise TypeError("Expected a bool, received a " + type(new).__name__)

		self.shape = shape
		self.weights = []

		if new:
			self.weights = self.weights_creator()
		else:
			if not isinstance(weights, list):
				raise TypeError("Expected a list, received a " + type(weights).__name__)
			if not len(weights) == len(shape)-1:
				raise TypeError("Incorrect weights length")
			for element in weights:
				if not isinstance(element, np.ndarray):
					raise TypeError("Expected a np.ndarray, received a " + type(element).__name__)
			for i in range(len(shape)-1):
				if not weights[i].shape == (shape[i+1], shape[i]):
					raise ValueError("Incorrect weights shape")
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

		if not len(inputs.shape) == 1:
			raise ValueError("Incorrect input shape")
		if not inputs.shape[0] == self.weights[0].shape[1]:
			raise ValueError("Incorrect input or weights shape")

		outputs = self.weights.copy()
		outputs.insert(0, inputs)

		for i in range(len(outputs)-1):

			# matrix multiplication between each element
			outputs[i+1] = np.tanh(outputs[i+1]@outputs[i])

		return outputs[-1]


	def decide(self, direction, status, directions=['L', 'U', 'R', 'D']):
		"""
		Parameters
		----------
		direction : str
			current direction
		status : array
			input vector
		directions : list of str
			available directions
		"""

		out = self.get_output(status)
		max_index = out.argmax(axis=0)
		direction_index = directions.index(direction)

		# changing direction based on the neural network result
		if max_index == 0:
			direction = directions[(direction_index-1) % 4]
		elif max_index == 2:
			direction = directions[(direction_index+1) % 4]

		return direction