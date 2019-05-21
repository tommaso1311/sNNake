import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import argparse
import sys


class game:
	"""
	Main class used to play the game Snake.

	Attributes
	----------
	size : list of integers
		a list of integers used to represent the game window
	background_color : tuple of integers
		describes the background color of the game window
	clock : pygame.time object
		used to control the refresh of the game window
	window : pygame.display

	Methods
	-------
	represent(frequency=24)
		Depicts the game window
	"""


	def __init__(self, size):
		"""
		Parameters
		----------
		size : list of int
			size[0] is the number of squares in the game field
			size[1] is the size in pixels of each square
		"""

		self.size = size
		self.background_color = (202, 202, 202)
		self.clock = pygame.time.Clock()
		self.window = pygame.display.set_mode((self.size[0]*self.size[1],
											self.size[0]*self.size[1]))

	def represent(self, frequency=24):

		self.window.fill(self.background_color)

		pygame.display.flip()
		self.clock.tick(frequency)


def main():

	parser = argparse.ArgumentParser()

	parser.add_argument("-s", "--size", nargs=2, default=[40, 20],
						help="specifies field size", action="store",
						type=int)

	args = parser.parse_args()

	print(args.size)

	G = game(args.size)

	while True:
		G.represent()


if __name__ == "__main__":
	main()