import pytest
from snake import *

@pytest.fixture
def test_snake():

	return snake()

def test_init_snake(test_snake):

	assert test_snake.lenght == 1
	assert test_snake.fitness == 0
	assert test_snake.direction in ['U', 'R', 'D', 'L']

def test_move(test_snake):

	test_snake.x_head = 1
	test_snake.y_head = 1

	test_snake.move()

	if test_snake.direction == 'U':
		assert test_snake.y_head == 0
		assert test_snake.x_head == 1
	elif test_snake.direction == 'R':
		assert test_snake.y_head == 1
		assert test_snake.x_head == 2
	elif test_snake.direction == 'D':
		assert test_snake.y_head == 2
		assert test_snake.x_head == 1
	else:
		assert test_snake.y_head == 1
		assert test_snake.x_head == 0