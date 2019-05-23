import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import argparse
import sys
import random


class snake:
	"""
	Class used to simulate the snake

	Attributes
	----------
	length : int
		length of the snake
	fitness : int
		fitness of the snake
	is_alive : boolean
		tells if the snake is alive
	position : array
		position of the snake
	direction : character
		direction in which the snake is moving
	occupied : list
		list of coordinates occupied

	Methods
	-------
	__init__()
		initialize a new snake
	move()
		gets inputs and moves the snake
	eat_not()
		checks if the snake has eaten food
	"""


	def __init__(self):

		self.length = 1
		self.fitness = 0
		self.is_alive = True
		self.position = None

		self.direction = random.choice(['U', 'R', 'D', 'L'])
		self.occupied = []


	def move(self):

		events = pygame.event.get()

		# listens to key pressure
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP and self.direction is not 'D':
					self.direction = 'U'
				elif event.key == pygame.K_RIGHT and self.direction is not 'L':
					self.direction = 'R'
				elif event.key == pygame.K_DOWN and self.direction is not 'U':
					self.direction = 'D'
				elif event.key == pygame.K_LEFT and self.direction is not 'R':
					self.direction = 'L'
				elif event.key == pygame.K_ESCAPE: quit()

		# upgrade the position
		if self.direction == 'U': self.position[0] -= 1
		elif self.direction == 'R': self.position[1] += 1
		elif self.direction == 'D': self.position[0] += 1
		else: self.position[1] -= 1

		# upgrade occupied list
		self.occupied.insert(0, self.position.copy())
		if len(self.occupied) > self.length:
			del self.occupied[-1]


	def eat_not(self, food):
		"""
		Parameters
		----------
		food : food object
		"""

		if (self.position == food.position).all():
			self.fitness += 10
			self.length += 1
			return False
		else:
			return True