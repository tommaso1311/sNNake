import numpy as np
import pygame
import sys

class game:

	def __init__(self, field_size=40, square=20):

		self.field_size = field_size
		self.square = square
		self.background_color = (202, 202, 202)
		self.clock = pygame.time.Clock()

	def represent(self, v=24):

		window = pygame.display.set_mode((self.field_size*self.square, self.field_size*self.square))
		window.fill(self.background_color)

		pygame.display.flip()
		self.clock.tick(v)

def main():

	G = game()

	while True:
		G.represent()

if __name__ == "__main__":
	main()