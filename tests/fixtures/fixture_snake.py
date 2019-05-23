import pytest
from snake import *

@pytest.fixture
def fixture_snake():
	return snake()