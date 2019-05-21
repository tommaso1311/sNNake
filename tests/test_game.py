import pytest
from src.game import *

@pytest.fixture
def window_size():

	return

@pytest.mark.parametrize("width, square, total",
						[(40, 20, 800),
						(10, 10, 100)])
def test_window(width, square, total):
	"""
	Tests correct game window size
	"""

	G = game([width, square])

	assert G.window.get_size() == (total, total)