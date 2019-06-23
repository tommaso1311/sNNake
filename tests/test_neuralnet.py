import numpy as np
from fixtures import fixture_shape, fixture_neural_network

def test_init_neural_network(fixture_shape, fixture_neural_network):
	"""
	Tests correct neural network initialization
	"""

	for i in range(len(fixture_shape)-1):

		assert fixture_neural_network.weights[i].shape == (fixture_shape[i+1], fixture_shape[i])
		assert -1 <= fixture_neural_network.weights[i].all() <= 1

def test_get_output(fixture_neural_network):
	"""
	Tests correct output computation
	"""

	outputs = fixture_neural_network.weights.copy()
	inputs = np.random.rand(fixture_neural_network.weights[0].shape[1])
	outputs.insert(0, inputs)

	for i in range(len(outputs)-1):
		outputs[i+1] = np.tanh(outputs[i+1]@outputs[i])

	assert (outputs[-1] == fixture_neural_network.get_output(inputs)).all()