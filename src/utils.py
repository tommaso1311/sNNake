import pickle
import os
import sys
from genetic_algorithm import *
from game import *


def save(generation, details, filename="generation"):
	"""
	Saves a snakes generation after checking if a file with same name
	already exists (also asks for a new name before exiting)
	"""

	assert isinstance(filename, str)
	for sn in generation:
		assert isinstance(sn, snake)

	filename = filename
	path_filename = "models/" + filename

	already_exists = os.path.isfile(path_filename)

	if already_exists:

		answer = get_yes_no("A file with this name already exists, do you want to overwrite it? [yes/no]")

		if not answer:
			filename = input("Please enter the new name: ")
			save(generation, details, filename)
			exit()

	with open(path_filename, "wb") as f:
		pickle.dump(generation, f)
		pickle.dump(details, f)

	print(filename + " is correctly saved!")


def load(filename="generation"):
	"""
	Loads a snakes generation
	"""

	assert isinstance(filename, str)
	path_filename = "models/" + filename

	exists = os.path.isfile(path_filename)

	if exists:
		with open(path_filename, "rb") as f:
			generation = pickle.load(f)
			details = pickle.load(f)

		for sn in generation:
			assert isinstance(sn, snake)
			sn.is_alive = True
			sn.length = 0
			sn.occupied = []
			sn.fitness = 0

		return generation, details

	else:
		print("Error: file not found")
		exit()


def get_yes_no(question):
	"""
	Used to get a yes or no answer
	"""

	assert isinstance(question, str)

	yes = {"yes", "y", "ye"}
	no = {"no", "n"}

	while True:

		print(question)
		answer = input().lower()

		if answer in no:
			return False
		elif answer in yes:
			return True
		else:
			print("Please respond with yes or no")
			print()

def train(generation=[], details=None, snakes=10, nn=[], generations=1, size=[10, 10], view=False, end=100):

	assert isinstance(generation, list)

	best_generation = []
	best_result = -1
	best_index = 0

	if not generation:

		generation = create_generation(generation, snakes, nn)

	else:

		for el in generation:
			assert isinstance(el, snake)

		snakes = len(generation)
		size = details["game_size"]
		end = details["duration"]


	for gen in range(generations):

		generation = create_generation(generation)

		for sn in generation:

			g = game(size, view, end)
			g.add_snake(sn)

			while g.snake.is_alive:

				g.play()

		result = np.mean([x.fitness for x in generation])
		print("generation", gen+1, "/", generations, ":", result)

		if result > best_result:
			best_generation = generation
			best_result = result
			best_index = gen

	print("Saving generation", best_index+1, "with a result of", best_result, "...")

	best_generation = sort_generation(best_generation)

	if details == None:
		details = {"trained": generations,
					"game_size": size,
					"duration": end,
					"best:": best_generation[0].fitness}
	else:
		details["trained"] += generations

	return best_generation, details