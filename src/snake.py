import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import argparse
import sys
import random
import food
import neuralnet


class snake:
	"""
	Class used to simulate the snake

	Attributes
	----------
	_human : bool
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
	_directions : list
		list of possibile directions
	_direction : character
		direction in which the snake is moving
	occupied : list
		list of coordinates occupied
	status : array
		status[0:3] is distances from obstacles
		status[3] is distance from food
		status[4] is angle between snake and food

	Methods
	-------
	move(game_size, food_obj)
		gets inputs and moves the snake
	has_not_eaten_food(food_obj)
		checks if the snake has eaten food
	_get_status(game_size, food_obj)
		gets the status vector
	_decide()
		changes direction based on neural network outputs
	has_exited()
		checks if the snake has exited the game window
	has_eaten_himself()
		checks if the snake has eaten himself
	dies()
		kills the snake and subtract 1 from fitness
	"""


	def __init__(self, neural_network=None, human=False):
		"""
		Parameters
		----------
		human : bool
			tells if the snake is controlled by user or neural network
		neural_network : tuple || neuralnet
			if it is None, human can be True (controlled) or False (used in tests)
			if it is a tuple, creates a new neuralnet object with that shape
			if it is a neuralnet object, copies the neural network
		"""

		assert isinstance(human, bool), "Expected a bool, received a " + type(human).__name__

		if neural_network == None:
			self.neural_network = None
			self._human = human
		elif isinstance(neural_network, neuralnet.neuralnet):
			self.neural_network = neural_network
			self._human = False
		elif isinstance(neural_network, list):
			neural_network = neural_network.copy()
			neural_network.insert(0, 5)
			neural_network.insert(len(neural_network), 3)
			self.neural_network = neuralnet.neuralnet(neural_network)
			self._human = False
		else:
			raise ValueError(("Error: neural_network is neither a neuralnet object nor a tuple!"))


		self.length = 1
		self.fitness = 0
		self.is_alive = True
		self.position = None

		self._directions = ['L', 'U', 'R', 'D']
		self._direction = random.choice(self._directions)
		self.occupied = []

		self.status = None


	def move(self, game_size=None, food_obj=None):
		"""
		Parameters
		----------
		game_size : array
		food_obj : food object
		"""

		if self._human:

			events = pygame.event.get()

			# listens to key pressure
			for event in events:
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP and self._direction is not 'D':
						self._direction = 'U'
					elif event.key == pygame.K_RIGHT and self._direction is not 'L':
						self._direction = 'R'
					elif event.key == pygame.K_DOWN and self._direction is not 'U':
						self._direction = 'D'
					elif event.key == pygame.K_LEFT and self._direction is not 'R':
						self._direction = 'L'
					elif event.key == pygame.K_ESCAPE: quit()

		elif self.neural_network != None:

			assert isinstance(game_size, int), "Expected an int, received a " + type(game_size).__name__
			assert isinstance(food_obj, food.food), "Expected a food objects, received a " + type(food_obj).__name__

			self._get_status(game_size, food_obj)
			self._decide()

		# upgrade the position
		if self._direction == 'U': self.position[0] -= 1
		elif self._direction == 'R': self.position[1] += 1
		elif self._direction == 'D': self.position[0] += 1
		else: self.position[1] -= 1

		# upgrade occupied list
		self.occupied.insert(0, self.position.copy())
		if len(self.occupied) > self.length:
			del self.occupied[-1]


	def has_not_eaten_food(self, food_obj):
		"""
		Parameters
		----------
		food : food object
		"""

		assert isinstance(food_obj, food.food), "Expected a food objects, received a " + type(food_obj).__name__

		# update length and fitness if food is eaten
		if (self.position == food_obj.position).all():
			self.fitness += 1
			self.length += 1
			return False
		else:
			return True


	def has_eaten_himself(self):

		if any((self.position == x).all() for x in self.occupied[1:]):
			return True
		else:
			return False


	def has_exited(self, size):
		"""
		Parameters
		----------
		size : number
			size of the game window
		"""

		if not (0<=self.position[0]<size and 0<=self.position[1]<size):
			return True
		else:
			return False


	def dies(self):

		self.fitness -= 1
		self.is_alive = False


def _get_status(self, game_size, food_obj):
		"""
		Parameters
		----------
		game_size : array
		food_obj : food object
		"""

		assert isinstance(game_size, int), "Expected an int, received a " + type(game_size).__name__
		assert isinstance(food_obj, food.food), "Expected a food objects, received a " + type(food_obj).__name__

		self.status = np.zeros(5)

		# creating a vector with distances from boundaries
		boundaries = np.array([self.position[1], self.position[0],
				game_size-self.position[1]-1, game_size-self.position[0]-1])

		# creating a vector with distances from the body
		body = np.array([game_size]*4)

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
		seen = np.minimum(boundaries, body)/game_size

		# reducing the size of the vector removing the information regarding the direction
		# opposed to the movement
		index = (self._directions.index(self._direction)+2) % 4
		seen = np.delete(seen, index)
		seen = np.roll(seen, -index)

		# adding distances from food and angle to the final status vector
		self.status[0:3] = seen
		self.status[3] = np.linalg.norm(self.position-food_obj.position)/(game_size*1.41421356237)
		
		coord = food_obj.position - self.position
		coords = [-coord[0], coord[1], coord[0], -coord[1]]

		self.status[4] = np.arctan2(coords[index%4], coords[(index+1)%4])/np.pi


	def _decide(self):
			
		out = self.neural_network.get_output(self.status)
		max_index = out.argmax(axis=0)
		direction_index = self._directions.index(self._direction)

		# changing direction based on the neural network result
		if max_index == 0:
			self._direction = self._directions[(direction_index-1) % 4]
		elif max_index == 2:
			self._direction = self._directions[(direction_index+1) % 4]