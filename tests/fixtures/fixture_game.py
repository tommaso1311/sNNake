import pytest
from game import *

@pytest.fixture
def fixture_game(fixture_size):

	return game(fixture_size[:-1])