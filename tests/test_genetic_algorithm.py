import numpy as np
import genetic_algorithm as ga
import snake
from fixtures import fixture_shape, fixture_neural_network, fixture_neural_network2

def test_neuralnet_crossover(fixture_neural_network, fixture_neural_network2):
	"""
	Tests the correct crossover between two neural networks (with no mutation)
	by checking the indices
	"""

	a = fixture_neural_network
	b = fixture_neural_network2

	c = ga.neural_network_crossover(a, b, crossover_prob=1, mutation_prob=0)

	for i in range(len(c.shape)-1):
		
		assert a.weights[i].shape == c.weights[i].shape

		indices_a = np.where(c.weights[i].flatten() == a.weights[i].flatten())[0]
		indices_b = np.where(c.weights[i].flatten() == b.weights[i].flatten())[0]

		assert (np.diff(indices_a) == 1).all()
		assert (np.diff(indices_b) == 1).all()
		assert len(indices_a) + len(indices_b) == c.weights[i].shape[0]*c.weights[i].shape[1]

def test_sort_generation():

	test_gen = []

	for i in range(10):
		test_gen.append(snake.snake())
		test_gen[-1].fitness = np.random.randint(0, 10)

	test_gen = ga.sort_generation(test_gen)

	assert all(test_gen[i].fitness >= test_gen[i+1].fitness for i in range(len(test_gen)-1))

def test_create_generation(fixture_neural_network):

	test_gen = []

	for i in range(10):
		test_gen.append(snake.snake((fixture_neural_network)))
		test_gen[-1].fitness = np.random.randint(0, 10)

	new_gen = ga.create_generation(test_gen)

	for sn in new_gen:
		assert isinstance(sn, snake.snake)
		assert len(test_gen) == len(new_gen)
		assert sn.neural_network.shape == fixture_neural_network.shape