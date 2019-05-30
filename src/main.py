from game import *
import genetic_algorithm as ga


def main():

	number_of_gen = 100
	snakes_per_gen = 100
	shape = (5, 31, 11, 3)

	generation = []
	for i in range(snakes_per_gen):
		generation.append(snake(shape))

	for gen in range(number_of_gen):

		for sn in generation:

			G = game([20, 20], False, 1000)
			G.add_snake(sn)
			G.play()


		generation = ga.evaluate_generation(generation)
		generation = ga.create_generation(generation)
		# if gen % 10 == 0:
		print("generation ", gen, generation[0].fitness)


if __name__ == "__main__":
	main()