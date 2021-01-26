import pytest
from sentiment_analysis import get_sentiment

def test_get_sentiment():
	test_text = "How to get BBC News on smart speakers"

	# check we got the correct sentiment score of the given text
	sentiment = get_sentiment(test_text)
	assert sentiment == 0.4019

