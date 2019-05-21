from snake import *

class game:
	"""
	Main class used to play the game Snake

	Attributes
	----------
	size : list
		a list of integers used to represent the game window
	background_color : tuple
		describes the background color of the game window
	snake_color : tuple
		describes the snake color in the game window
	clock : pygame.time object
		used to control the refresh of the game window
	window : pygame.display object
		used to represent the game
	field : array
		used to represent the game

	Methods
	-------
	field_update()
		updates the field array
	play()
		runs the game
	represent(frequency=30)
		depicts the game window
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
		self.snake_color = (66, 149, 71)
		self.clock = pygame.time.Clock()
		self.window = pygame.display.set_mode((self.size[0]*self.size[1],
											self.size[0]*self.size[1]))
		self.field = np.zeros((self.size[0], self.size[0]), dtype=int)


	# def field_update(self):

	# 	self.field = np.zeros((self.size[0], self.size[0]), dtype=int)
	# 	for coord in self.snake.occupied:
	# 		self.field[coord] = 1


	def play(self):

		self.snake = snake()
		self.snake.x_head = np.random.randint(0, self.size[0])
		self.snake.y_head = np.random.randint(0, self.size[0])

		while True:
			self.snake.move()
			self.represent()


	def represent(self, frequency=30):

		self.window.fill(self.background_color)

		for coord in self.snake.occupied:
			pygame.draw.rect(self.window, self.snake_color,
				pygame.Rect(coord[1]*self.size[1], coord[0]*self.size[1],
					self.size[1], self.size[1]))

		pygame.display.flip()
		self.clock.tick(frequency)


def main():

	parser = argparse.ArgumentParser()

	parser.add_argument("-s", "--size", nargs=2, default=[40, 20],
						help="specifies field size", action="store",
						type=int)

	args = parser.parse_args()

	G = game(args.size)

	while True:
		G.play()


if __name__ == "__main__":
	main()