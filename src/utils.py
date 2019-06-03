import pickle
import os
import sys
from genetic_algorithm import *


def save(generation, details, filename="generation"):
	"""
	Saves a snakes generation after checking if a file with same name
	already exists (also asks for a new name before exiting)
	"""

	assert isinstance(filename, str)
	for sn in generation:
		assert isinstance(sn, snake)

	filename = filename + ".snn"
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