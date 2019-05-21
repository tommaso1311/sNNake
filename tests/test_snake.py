import pytest
from snake import *

def test_init_snake():

	test_snake = snake()

	assert test_snake.lenght == 1
	assert test_snake.fitness == 0
	assert test_snake.direction in ['U', 'R', 'D', 'L']