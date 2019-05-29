from game import *
import genetic_algorithm as ga


def main():

	snakes_per_gen = 10
	shape = (5, 2, 3)
	starting_generation = []
	for i in range(snakes_per_gen):
		starting_generation.append(snake(False, shape))

	for sn in starting_generation:

		G = game([10, 20])
		G.add_snake(sn)
		G.play()

	for sn in starting_generation:
		print(sn.fitness)


if __name__ == "__main__":
	main()