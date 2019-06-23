import numpy as np
import neuralnet
from fixtures import fixture_size, fixture_shape, fixture_food, fixture_snake


def test_init_snake(fixture_snake):
	"""
	Tests correct snake initialization
	"""

	assert fixture_snake.length == 1
	assert fixture_snake.fitness == 0
	assert fixture_snake.direction in ['R', 'D', 'L', 'U']
	assert fixture_snake.is_alive
	assert not len(fixture_snake.occupied)


def test_move(fixture_snake, fixture_size, fixture_food):
	"""
	Tests correct snake movement
	"""	

	final_positions = [np.array([1, 0]), np.array([0, 1]),
						np.array([1, 2]), np.array([2, 1])]

	for i in range(len(fixture_snake.directions)):

		fixture_snake.position = np.array([1, 1])
		fixture_snake.direction = fixture_snake.directions[i]
		fixture_snake.move()
		
		assert (fixture_snake.position == final_positions[i]).all()


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


def test_get_status(fixture_snake, fixture_food, fixture_size):
	"""
	Tests correct status vector is created
	"""

	half = int(fixture_size/2)/fixture_size
	half2 = int((fixture_size-1)/2)/fixture_size
	step = 1/fixture_size

	fixture_food.position = np.array([0, 0])
	fixture_snake.position = np.array([int(fixture_size/2)]*2)

	fixture_snake.occupied.append(fixture_snake.position)
	fixture_snake.occupied.append(np.array([int(fixture_size/2), int(fixture_size/2)+2]))
	fixture_snake.occupied.append(np.array([int(fixture_size/2)-4, int(fixture_size/2)]))

	obstacles_answers = [half2, half, 3*step, step]
	angles_answers = [-0.25, 0.25, 0.75, -0.75]
	distance = np.linalg.norm(fixture_snake.position-fixture_food.position)/(fixture_size*1.41421356237)

	for i in range(len(fixture_snake.directions)):

		fixture_snake.direction = fixture_snake.directions[i]
		fixture_snake.get_status(fixture_size, fixture_food)

		np.testing.assert_allclose(fixture_snake.status[0:3], np.roll(obstacles_answers, -i)[0:-1])
		assert fixture_snake.status[3] == distance
		assert fixture_snake.status[4] == angles_answers[i]


def test_decide(fixture_snake):
	"""
	Tests if the correct decision is made by the neuralnetwork
	"""

	fixture_snake.neural_network = neuralnet.neuralnet([3, 3])
	fixture_snake.neural_network.weights[0] = np.eye(3)

	for j in range(3):

		fixture_snake.status = np.zeros(3)
		fixture_snake.status[j] = 1

		for i in range(len(fixture_snake.directions)):

			fixture_snake.direction = fixture_snake.directions[i]
			fixture_snake.decide()

			assert fixture_snake.direction == fixture_snake.directions[(i+j-1)%4]


def test_has_eaten_himself(fixture_snake):

	fixture_snake.position = np.array([0, 0])
	fixture_snake.occupied.append(fixture_snake.position)
	fixture_snake.occupied.insert(1, np.array([0, 0]))

	assert fixture_snake.has_eaten_himself()


def test_has_exited(fixture_snake, fixture_size):

	positions = [np.array([-1, 0]), np.array([0, -1]),
		np.array([fixture_size+1, 0]), np.array([0, fixture_size+1])]

	for pos in positions:

		fixture_snake.position = pos
		
		assert fixture_snake.has_exited(fixture_size)