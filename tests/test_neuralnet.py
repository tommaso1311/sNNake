from fixtures.fixture_shape import *
from fixtures.fixture_neural_network import *

def test_init_neural_network(fixture_shape, fixture_neural_network):
	"""
	Tests correct neural network initialization
	"""

	for i in range(len(fixture_shape)-1):

		assert fixture_neural_network.weights[i].shape == (fixture_shape[i+1], fixture_shape[i])
