import pytest
import numpy as np

@pytest.fixture
def fixture_shape():

	a = np.random.randint(1, 50)
	b = np.random.randint(1, 25)
	shape = (5, a, b, 3)

	return shape