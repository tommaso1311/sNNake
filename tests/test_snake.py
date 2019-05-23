from fixtures.fixture_snake import *
from fixtures.fixture_food import *


def test_init_snake(fixture_snake):
	"""
	Tests correct snake initialization
	"""

	assert fixture_snake.length == 1
	assert fixture_snake.fitness == 0
	assert fixture_snake.direction in ['U', 'R', 'D', 'L']
	assert fixture_snake.is_alive
	assert not len(fixture_snake.occupied)


@pytest.mark.xfail(reason="video system not initialized")
def test_move(fixture_snake):
	"""
	Tests correct snake movement
	"""	

	fixture_snake.position = np.array([1, 1])
	fixture_snake.direction = 'U'
	fixture_snake.move()

	assert (fixture_snake.position == np.array([0, 1])).all()

	fixture_snake.position = np.array([1, 1])
	fixture_snake.direction = 'R'
	fixture_snake.move()

	assert (fixture_snake.position == np.array([1, 2])).all()

	fixture_snake.position = np.array([1, 1])
	fixture_snake.direction = 'D'
	fixture_snake.move()
	
	assert (fixture_snake.position == np.array([2, 1])).all()

	fixture_snake.position = np.array([1, 1])
	fixture_snake.direction = 'L'
	fixture_snake.move()
	
	assert (fixture_snake.position == np.array([1, 0])).all()


def test_eat_not(fixture_snake, fixture_food):
	"""
	Tests correct length and fitness improve after food eating
	"""

	fixture_snake.position = np.array([1, 1])
	fixture_food.position = np.array([1, 0])

	assert fixture_snake.eat_not(fixture_food)

	fixture_food.position = np.array([1, 1])
	fitness_before = fixture_snake.fitness
	length_before = fixture_snake.length

	assert not fixture_snake.eat_not(fixture_food)
	assert fixture_snake.fitness > fitness_before
	assert fixture_snake.length > length_before