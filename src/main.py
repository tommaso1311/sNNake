from game import *
from utils import *


def main():

	# adding parser
	parser = argparse.ArgumentParser()

	group = parser.add_mutually_exclusive_group()
	group.add_argument("-p", "--play", action="store_true", help="play a new game")
	group.add_argument("-t", "--train", action="store_true", help="train a new model")
	group.add_argument("-l", "--load", action="store_true", help="load an existing model")

	parser.add_argument("-v", "--view", action="store_true", help="activate representation")

	parser.add_argument("-s", "--size", default=10,
						help="specifies game size", action="store", type=int)

	parser.add_argument("-g", "--generations", default=10,
						help="specifies number of generations in the trained model",
						action="store", type=int)

	parser.add_argument("-k", "--snakes", default=10,
						help="specifies number of snakes per generation in the trained model",
						action="store",	type=int)

	parser.add_argument("-n", "--nn", nargs="*", default=[],
						help="specifies neural network hidden layers in the trained model",
						action="store", type=int)

	parser.add_argument("-e", "--end", default=100,
						help="specifies max duration of the game in the trained model",
						action="store", type=int)

	parser.add_argument("-m", "--name", default="generation",
						help="specifies name of the file in which store the model",
						action="store", type=str)

	args = parser.parse_args()

	# parser option for a simple game
	if args.play:

		G = game(args.size, True, np.inf)
		sn = snake(human=True)
		G.add_snake(sn)

		while G.snake.is_alive:
			G.play()
			esc_exit()

		print("Your total points are:", G.snake.fitness+1)

	# parser option to train a model
	elif args.train:

		best_generation, details = train(snakes=args.snakes, shape=args.nn,
										generations=args.generations, size=args.size,
										view=args.view, end=args.end)

		save(best_generation, details, args.name)
		
	# parser option to load an existing model
	elif args.load:

		generation, details = load(args.name)
		print()
		print(args.name, "correctly loaded! Model details are:")
		print(details)

		print()
		train_answer = get_yes_no("Do you want to continue to train the model?")

		if train_answer:

			print()
			generations = input("Insert number of generations to train: ")
			assert generations.isdigit()
			generations = int(generations)

			best_generation, details = train(generation, details, generations=generations,
											view=args.view)

			best_generation = sort_generation(best_generation)

			save(best_generation, details, args.name)

		else:

			print()
			view_answer = get_yes_no("Do you want to view the model in action?")
			if not view_answer:
				exit()

			print()
			best_answer = get_yes_no("Do you want to see only the best one?")
			if best_answer:

				g = game(details["game_size"], True, details["duration"])
				g.add_snake(generation[0])

				while g.snake.is_alive:
					g.play()
					esc_exit()

				print("Snake points are:", g.snake.fitness)

			else:

				for sn in generation:

					g = game(details["game_size"], True, details["duration"])
					g.add_snake(sn)

					while g.snake.is_alive:
						g.play()
						esc_exit()

					print("Snake points are:", g.snake.fitness)
			
	else:

		print("Please run with --help flag to see available options")


if __name__ == "__main__":
	main()