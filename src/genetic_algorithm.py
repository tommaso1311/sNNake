import numpy as np
from snake import *


def neuralnet_crossover(neural_network_a, neural_network_b, crossover_prob=0.95, mutation_prob=0.01):

	assert isinstance(neural_network_a, neuralnet)
	assert isinstance(neural_network_b, neuralnet)
	assert neural_network_a.shape == neural_network_b.shape
	assert 1 >= crossover_prob >= 0
	assert 1 >= mutation_prob >= 0

	weights = []

	for i in range(len(neural_network_a.shape)-1):

		neural_network_a_genes = neural_network_a.weights[i].flatten()
		neural_network_b_genes = neural_network_b.weights[i].flatten()

		if np.random.rand() < crossover_prob:

			crossover = np.random.randint(0, len(neural_network_a_genes))
			temp = neural_network_a_genes[crossover:len(neural_network_a_genes)+1].copy()

			neural_network_a_genes[crossover:len(neural_network_a_genes)+1] = neural_network_b_genes[crossover:len(neural_network_b_genes)+1]
			neural_network_b_genes[crossover:len(neural_network_b_genes)+1] = temp

		if np.random.rand() < mutation_prob:

			m = np.random.randint(0, len(neural_network_a_genes))
			mutation = np.random.uniform(-1, 1)

			neural_network_a_genes[m] = mutation
			neural_network_b_genes[m] = mutation

		if np.random.choice([-1, 1]) > 0:
			weights.append(neural_network_a_genes.reshape(neural_network_a.weights[i].shape))
		else:
			weights.append(neural_network_b_genes.reshape(neural_network_b.weights[i].shape))
 
	neuralnet_final = neuralnet(neural_network_a.shape, False, weights)

	return neuralnet_final


def evaluate_generation(generation):

	assert isinstance(generation, list)
	for element in generation: assert isinstance(element, snake)

	generation.sort(key=lambda snake: snake.fitness, reverse=True)

	return generation


def create_generation(generation, q=0.05):

	# TODO add possibility to modify crossover parameters!

	assert 1 >= q >= 0
	assert isinstance(generation, list)
	for element in generation: assert isinstance(element, snake)

	p = np.fromfunction(lambda r: q*(1-q)**r, shape=(n,))
	p = p/p.sum()

	new_generation = []

	for i in len(generation):

		neural_network_a = np.random.choice(generation, p=p).neural_network
		neural_network_b = np.random.choice(generation, p=p).neural_network

		neural_network_final = neuralnet_crossover(neural_network_b, neural_network_b)

		snake_final = snake(False, neural_network_final)

		new_generation.append(snake_final)

	return new_generation