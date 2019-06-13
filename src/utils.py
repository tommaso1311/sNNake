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

	assert isinstance(filename, str), "Expected a string, received a " + type(filename).__name__
	for sn in generation:
		assert isinstance(sn, snake), "Expected a snake, received a " + type(snake).__name__
	assert isinstance(details, dict), "Expected a dictionary, received a " + type(details).__name__

	# setting path filename and checking if it already exists

	if not os.path.exists("models"):
		os.mkdir('models')

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

	assert isinstance(filename, str), "Expected a string, received a " + type(filename).__name__

	# setting path filename and checking if it already exists
	path_filename = "models/" + filename
	exists = os.path.isfile(path_filename)

	if exists:
		with open(path_filename, "rb") as f:
			generation = pickle.load(f)
			details = pickle.load(f)

		for sn in generation:
			assert isinstance(sn, snake)
			sn.is_alive = True
			sn.length = 1
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

	assert isinstance(question, str), "Expected a string, received a " + type(question).__name__

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
			print("Please respond with yes or no!")


def train(generation=[], details={}, snakes=10, shape=[], generations=1,
	size=10, view=False, end=100):
	"""
	Used to train the model
	"""

	assert isinstance(generation, list), "Expected a list, received a " + type(generation).__name__
	assert isinstance(details, dict), "Expected a dict, received a " + type(details).__name__
	assert isinstance(snakes, int), "Expected an int, received a " + type(snakes).__name__
	assert isinstance(shape, list), "Expected a string, received a " + type(shape).__name__
	assert isinstance(generations, int), "Expected an int, received a " + type(generations).__name__
	assert isinstance(size, int), "Expected an int, received a " + type(size).__name__
	assert isinstance(view, bool), "Expected a bool, received a " + type(view).__name__
	assert isinstance(end, int), "Expected an int, received a " + type(end).__name__

	# initializing best results
	best_generation = []
	best_result = -1
	best_index = 0

	if not generation:

		generation = create_generation(generation, snakes, shape)

	else:

		for e in generation:
			assert isinstance(e, snake), "Expected a snake, received a " + type(e).__name__

		snakes = len(generation)
		size = details["game_size"]
		end = details["duration"]

	# running the train simulation
	for gen in range(generations):

		generation = create_generation(generation)

		for sn in generation:

			g = game(size, view, end)
			g.add_snake(sn)

			while g.snake.is_alive:

				g.play()
				if view: esc_exit()

		result = np.mean([x.fitness for x in generation])
		print("generation", gen+1, "/", generations, ":", result)

		# updating best results
		if result > best_result:
			best_generation = generation
			best_result = result
			best_index = gen

	print("Saving generation", best_index+1, "with a result of", best_result, "...")

	best_generation = sort_generation(best_generation)

	if not bool(details):
		details = {"trained": generations,
					"game_size": size,
					"duration": end,
					"best": best_generation[0].fitness}
	else:
		details["trained"] += generations

	return best_generation, details


def esc_exit():
	"""
	Used to stop graphical representation
	"""

	events = pygame.event.get()
	for event in events:
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE: quit()