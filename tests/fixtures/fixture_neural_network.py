import pytest
from neuralnet import *

@pytest.fixture
def fixture_neural_network(fixture_shape):

	return neuralnet(fixture_shape)

@pytest.fixture
def fixture_neural_network2(fixture_shape):

	return neuralnet(fixture_shape)