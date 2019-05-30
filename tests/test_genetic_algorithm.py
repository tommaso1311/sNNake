from fixtures.fixture_neural_network import *
from fixtures.fixture_shape import *
import genetic_algorithm as ga

def test_neuralnet_crossover(fixture_neural_network, fixture_neural_network2):

	a = fixture_neural_network
	b = fixture_neural_network2

	c = ga.neural_network_crossover(a, b)

	for i in range(len(c.shape)-1):
		
		assert a.weights[i].shape == c.weights[i].shape

		indices_a = np.where(c.weights[i].flatten() == a.weights[i].flatten())[0]
		indices_b = np.where(c.weights[i].flatten() == b.weights[i].flatten())[0]

		assert (np.diff(indices_a) == 1).all()
		assert (np.diff(indices_b) == 1).all()
		assert len(indices_a) + len(indices_b) == c.weights[i].shape[0]*c.weights[i].shape[1]