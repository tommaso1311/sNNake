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
		lenght of the snake
	fitness : int
		fitness of the snake
	x_head : int
	y_head : int
		xy position of the snake head
	direction : character
		direction in which the snake is moving
	occupied : list
		list of coordinates occupied

	Methods
	-------
	move()
		gets inputs and moves the snake
	"""

	def __init__(self):

		self.lenght = 1
		self.fitness = 0

		self.x_head = None
		self.y_head = None

		self.direction = random.choice(['U', 'R', 'D', 'L'])
		self.occupied = []

	def move(self):

		events = pygame.event.get()

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

		if self.direction is 'U': self.y_head -= 1
		elif self.direction is 'R': self.x_head += 1
		elif self.direction is 'D': self.y_head += 1
		else: self.x_head -= 1

		self.position = (self.y_head, self.x_head)

		self.occupied.insert(0, self.position)
		if len(self.occupied) > self.lenght:
			del self.occupied[-1]