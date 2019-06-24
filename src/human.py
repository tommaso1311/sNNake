import pygame

class human:
	"""
	Class used to listen tu human input
	"""

	def decide(self, direction, *kwargs):

		events = pygame.event.get()

		# listens to key pressure
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP and direction is not 'D':
					return 'U'
				elif event.key == pygame.K_RIGHT and direction is not 'L':
					return 'R'
				elif event.key == pygame.K_DOWN and direction is not 'U':
					return 'D'
				elif event.key == pygame.K_LEFT and direction is not 'R':
					return 'L'
				elif event.key == pygame.K_ESCAPE: quit()

		return direction