import pytest
import numpy as np

@pytest.fixture
def fixture_size():

	a = np.random.randint(10, 100)
	b = np.random.randint(1, 10)
	size = np.array([a, b, a*b])

	return size