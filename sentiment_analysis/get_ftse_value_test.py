import pytest
from get_ftse_value import get_ftse_value


def test_get_ftse_value():
	ftse_value = get_ftse_value()
	# check we got the ftse value as a float
	assert isinstance(ftse_value, float)
