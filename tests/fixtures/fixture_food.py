import pytest
import food

@pytest.fixture
def fixture_food():
	return food.food()