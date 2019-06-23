import numpy as np
import pytest
import food
import neuralnet
import snake
import game


@pytest.fixture
def fixture_size():

	size = np.random.randint(10, 100)

	return size


@pytest.fixture
def fixture_shape():

	a = np.random.randint(1, 50)
	b = np.random.randint(1, 25)
	shape = [5, a, b, 3]

	return shape


@pytest.fixture
def fixture_food():
	return food.food()


@pytest.fixture
def fixture_neural_network(fixture_shape):

	return neuralnet.neuralnet(fixture_shape)


@pytest.fixture
def fixture_neural_network2(fixture_shape):

	return neuralnet.neuralnet(fixture_shape)


@pytest.fixture
def fixture_snake():
	return snake.snake()


@pytest.fixture
def fixture_game(fixture_size):

	return game.game(fixture_size, True)