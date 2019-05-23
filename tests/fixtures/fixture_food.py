import pytest
from food import *

@pytest.fixture
def fixture_food():
	return food()