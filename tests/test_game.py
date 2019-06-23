import numpy as np
import pytest
from fixtures import fixture_game, fixture_size

@pytest.mark.xfail(reason="video system not initialized")
def test_init_window(fixture_size, fixture_game):
	"""
	Tests correct game window size
	"""

	assert fixture_game._window.get_size()[0] == fixture_size*20
	assert fixture_game._window.get_size()[1] == fixture_size*20

@pytest.mark.xfail(reason="video system not initialized")
def test_is_over(fixture_game):
	"""
	Tests correct end game condition
	"""

	positions = [np.array([-1, 0]), np.array([0, -1]),
		np.array([fixture_game.size+1, 0]), np.array([0, fixture_game.size+1])]

	fixture_game.add_snake()

	fixture_game.snake.position = np.array([0, 0])
	fixture_game._is_over()

	assert fixture_game.snake.is_alive

	fixture_game.snake.occupied.insert(1, np.array([0, 0]))
	fixture_game.snake.position = np.array([0, 0])
	fixture_game._is_over()

	assert not fixture_game.snake.is_alive

	for pos in positions:

		fixture_game.snake.is_alive = True
		fixture_game.snake.position = pos
		fixture_game._is_over()
		
		assert not fixture_game.snake.is_alive

	