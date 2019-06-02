from game import *
from utils import *
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

			G = game([10, 20], False, 100)
			G.add_snake(sn)

			while G.snake.is_alive:
				G.play()

		result = np.mean([sn.fitness for sn in generation])
		print("generation", gen+1, ":", result)

		generation = ga.create_generation(generation)
		
	for sn in generation:
		G = game([10, 20], False, 100)
		G.add_snake(sn)

	while G.snake.is_alive:
		G.play()

	# generation = sort_generation(generation)
	save(generation)

	# generation = load()
	# generation = sort_generation(generation)

	# G = game()
	# G = game([10, 20], True, 1000)
	# G.add_snake(generation[0])

	# while G.snake.is_alive:
	# 	G.play()


if __name__ == "__main__":
	main()