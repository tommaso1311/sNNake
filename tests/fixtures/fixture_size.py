import pytest
import numpy as np

@pytest.fixture
def fixture_size():

	size = np.random.randint(10, 100)

	return size