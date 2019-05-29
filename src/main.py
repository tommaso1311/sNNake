from game import *
import genetic_algorithm as ga


def main():

	number_of_gen = 10
	snakes_per_gen = 10
	shape = (5, 2, 3)

	generation = []
	for i in range(snakes_per_gen):
		generation.append(snake(False, shape))

	for gen in range(number_of_gen):

		for sn in generation:

			G = game([10, 20], 10)
			G.add_snake(sn)
			G.play()

		generation = ga.evaluate_generation(generation)
		print(np.mean([x.fitness for x in generation]))
		generation = ga.create_generation(generation)


if __name__ == "__main__":
	main()