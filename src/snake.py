import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import argparse
import sys
import random
from food import *
from neuralnet import *


class snake:
	"""
	Class used to simulate the snake

	Attributes
	----------
	human : bool
		tells if the snake is controlled by user or neural network
	neural_network : neuralnet
		neural network from neuralnet
	length : int
		length of the snake
	fitness : int
		fitness of the snake
	is_alive : bool
		tells if the snake is alive
	position : array
		position of the snake
	direction : character
		direction in which the snake is moving
	occupied : list
		list of coordinates occupied
	status : array
		status[0:3] is distances from obstacles
		status[3] is distance from food
		status[4] is angle between snake and food

	Methods
	-------
	__init__()
		initialize a new snake
	move(game_size, food_obj)
		gets inputs and moves the snake
	eat_not(food_obj)
		checks if the snake has eaten food
	get_status(game_size, food_obj)
		gets the status vector
	"""


	def __init__(self, human=True, neural_network=None):

		assert isinstance(human, bool)

		self.human = human

		if not self.human and isinstance(neural_network, neuralnet):
			self.neural_network = neural_network
		elif not self.human and isinstance(neural_network, tuple):
			self.neural_network = neuralnet(neural_network)
		elif not self.human:
			raise ValueError("Error: snake is not human controlled but neural_network is neither a neuralnet object nor a tuple!")

		self.length = 1
		self.fitness = 0
		self.is_alive = True
		self.position = None

		self.directions = ['R', 'D', 'L', 'U']
		self.direction = random.choice(self.directions)
		self.occupied = []

		self.status = None


	def move(self, game_size=None, food_obj=None):
		"""
		Parameters
		----------
		game_size : array
		food_obj : food object
		"""

		if self.human:

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

		else:

			assert isinstance(game_size, np.ndarray), "game_size is not an array"
			assert isinstance(food_obj, food), "food_obj is not a food object"

			self.get_status(game_size, food_obj)
			
			out = self.neural_network.get_output(self.status)
			max_index = out.argmax(axis=0)
			direction_index = self.directions.index(self.direction)

			# changing direction based on the neural network result
			if max_index == 0:
				self.direction = self.directions[(direction_index-1) % len(self.directions)]
			elif max_index == 2:
				self.direction = self.directions[(direction_index+1) % len(self.directions)]

		# upgrade the position
		if self.direction == 'U': self.position[0] -= 1
		elif self.direction == 'R': self.position[1] += 1
		elif self.direction == 'D': self.position[0] += 1
		else: self.position[1] -= 1

		# upgrade occupied list
		self.occupied.insert(0, self.position.copy())
		if len(self.occupied) > self.length:
			del self.occupied[-1]


	def eat_not(self, food_obj):
		"""
		Parameters
		----------
		food : food object
		"""

		assert isinstance(food_obj, food), "food_obj is not a food object"

		if (self.position == food_obj.position).all():
			self.fitness += 10
			self.length += 1
			return False
		else:
			return True


	def get_status(self, game_size, food_obj):
		"""
		Parameters
		----------
		game_size : array
		food_obj : food object
		"""

		assert isinstance(game_size, np.ndarray)
		assert isinstance(food_obj, food)

		self.status = np.zeros(5)

		# creating a vector with distances from boundaries
		boundaries = np.array([self.position[1], self.position[0],
				game_size[0]-self.position[1]-1, game_size[0]-self.position[0]-1])

		# creating a vector with distances from the body
		body = np.array([game_size[0]]*4)

		if self.occupied[1:]:

			temp = self.position - self.occupied[1:]
			temp = temp[np.any(temp==0, axis=1)]

			if temp[temp[:,1]>0, 0].size != 0:
				body[0] = min(temp[temp[:,1]>0, 1])-1
			if temp[temp[:,0]>0, 0].size != 0:
				body[1] = min(temp[temp[:,0]>0, 0])-1
			if temp[temp[:,1]<0, 0].size != 0:
				body[2] = min(np.abs(temp[temp[:,1]<0, 1]))-1
			if temp[temp[:,0]<0, 0].size != 0:
				body[3] = min(np.abs(temp[temp[:,0]<0, 0]))-1

		# creating a vector with minimum distances from something and normalizes it
		seen = np.minimum(boundaries, body)/game_size[0]

		# reducing the size of the vector removing the information regarding the direction
		# opposed to the movement
		index = self.directions.index(self.direction)
		seen = np.delete(seen, index)
		seen = np.roll(seen, -index)

		# adding distances from food and angle to the final status vector
		self.status[0:3] = seen
		self.status[3] = np.sqrt((food_obj.position[0]-self.position[0])**2+(food_obj.position[1]-self.position[1])**2)/(game_size[0]*1.41421356237)
		coord = np.subtract(food_obj.position, self.position)

		if index == 3:
			self.status[4] = np.arctan2(-coord[1], -coord[0])/np.pi
		elif index == 2:
			self.status[4] = np.arctan2(coord[0], -coord[1])/np.pi
		elif index == 1:
			self.status[4] = np.arctan2(coord[1], coord[0])/np.pi
		else:
			self.status[4] = np.arctan2(-coord[0], coord[1])/np.pi