import pytest
from snake import *

@pytest.fixture
def test_snake():

	return snake()

def test_init_snake(test_snake):

	assert test_snake.length == 1
	assert test_snake.fitness == 0
	assert test_snake.direction in ['U', 'R', 'D', 'L']

@pytest.mark.xfail(reason="video system not initialized")
def test_move(test_snake):

	test_snake.position = [1, 1]

	test_snake.move()

	if test_snake.direction == 'U':
		assert test_snake.position == [0, 1]
	elif test_snake.direction == 'R':
		assert test_snake.position == [1, 2]
	elif test_snake.direction == 'D':
		assert test_snake.position == [2, 1]
	else:
		assert test_snake.position == [1, 0]