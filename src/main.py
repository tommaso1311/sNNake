from game import *
from utils import *


def main():

	parser = argparse.ArgumentParser()

	group = parser.add_mutually_exclusive_group()
	group.add_argument("-p", "--play", action="store_true", help="play a new game")
	group.add_argument("-t", "--train", action="store_true", help="train a new model")
	group.add_argument("-l", "--load", action="store_true", help="load an existing model")

	parser.add_argument("-v", "--view", action="store_true")
	parser.add_argument("-s", "--size", nargs=2, default=[10, 20],
						help="specifies field size", action="store", type=int)
	parser.add_argument("-g", "--generations", default=10,
						help="specifies number of generations in the model", action="store",
						type=int)
	parser.add_argument("-k", "--snakes", default=10,
						help="specifies number of snakes per generation in the model", action="store",
						type=int)
	parser.add_argument("-n", "--nn", nargs="*", default=[],
						help="specifies neural network hidden layers", action="store",
						type=int)
	parser.add_argument("-e", "--end", default=100,
						help="specifies max duration of the game", action="store",
						type=int)
	parser.add_argument("-m", "--name", default="generation_",
						help="specifies name of the file with the model", action="store",
						type=str)

	args = parser.parse_args()

	if args.play:

		G = game(args.size, True, np.inf)
		sn = snake(human=True)
		G.add_snake(sn)

		while G.snake.is_alive:
			G.play()

		print("Your total points are:", G.snake.fitness+1)

	elif args.train:

		generation = []
		best_generation = []
		best_result = -1
		best_index = 0

		for i in range(args.snakes):
			generation.append(snake(args.nn))

		for gen in range(args.generations):
			for sn in generation:

				g = game(args.size, args.view, args.end)
				g.add_snake(sn)

				while g.snake.is_alive:
					g.play()

			result = np.mean([x.fitness for x in generation])
			print("generation", gen+1, "/", args.generations, ":", result)

			if result > best_result:
				best_generation = generation
				best_result = result
				best_index = gen

			generation = create_generation(generation)

		print("Saving generation", best_index+1, "with a result of", best_result, "...")

		best_generation = sort_generation(best_generation)
		details = {"trained": args.generations,
					"game_size": args.size[0],
					"duration": args.end,
					"best:": best_generation[0].fitness}

		save(best_generation, details, args.name+"[fitness="+str(best_result)+"]")
		

	elif args.load:

		generation, details = load(args.name)
		print(details)

	else:

		print("you don't want to play")

	# details = {"trained": 100,
	# 			"game size": [40, 20]}

	# number_of_gen = 2
	# snakes_per_gen = 100
	# shape = (5, 31, 11, 3)

	# generation = []
	# for i in range(snakes_per_gen):
	# 	generation.append(snake(shape))

	# for gen in range(number_of_gen):

	# 	for sn in generation:

	# 		G = game([10, 20], False, 100)
	# 		G.add_snake(sn)

	# 		while G.snake.is_alive:
	# 			G.play()

	# 	result = np.mean([sn.fitness for sn in generation])
	# 	print("generation", gen+1, ":", result)

	# 	generation = ga.create_generation(generation)
		
	# for sn in generation:
	# 	G = game([10, 20], False, 100)
	# 	G.add_snake(sn)

	# while G.snake.is_alive:
	# 	G.play()

	# # generation = sort_generation(generation)
	# save(generation, details)

	# generation, details = load()
	# print(details)
	# generation = sort_generation(generation)

	# G = game()
	# G = game([10, 20], True, 1000)
	# G.add_snake(generation[0])

	# while G.snake.is_alive:
	# 	G.play()


if __name__ == "__main__":
	main()