import pytest
import os
from text_extract import extract_story


def test_proc_normal_story():

	with open(os.path.dirname(os.path.abspath(__file__))+'/test_data/normal_story.txt', 'r') as test_data:
		content = test_data.read()

	title, final_content = extract_story(content, "")

	# check we get the correct title
	assert title == "Coronavirus: Amazon builds its own testing lab for staff"

	# check that the start of the content is present
	assert final_content.startswith("Retail giant Amazon says it will build its own coronavirus testing lab to monitor the health of its")

	# check that the end of the content is present
	assert final_content.endswith("The Pennsylvania warehouse receives products from manufacturer before sending them to smaller Amazon warehouses around the US. ")
	

def test_proc_index_page():
	with open(os.path.dirname(os.path.abspath(__file__))+'/test_data/business_page.txt', 'r') as test_data:
		content = test_data.read()

	title, final_content = extract_story(content, "")

	assert title == "Business"

	# check that the start of the content is present
	assert final_content.startswith("Trump promises 'help' to clinch oil cut deal Oil producers")

	# check that the end of the content is present
	assert final_content.endswith("Investors were in bullish mood despite record US job losses and continued coronavirus shutdowns. ")


def test_proc_video_page():
	with open(os.path.dirname(os.path.abspath(__file__))+'/test_data/video_page.txt', 'r') as test_data:
		content = test_data.read()

	title, final_content = extract_story(content, "")

	assert title == "Coronavirus: 'My parents' campervan has become my office'"

	# check that the start of the content is present
	assert final_content.startswith("It might not be absolutely fabulous")

	# check that the end of the content is present
	assert final_content.endswith("Film by digital reporter Dougal Shaw ")


def test_market_data_page():

	title, final_content = extract_story("123456789", "https://www.bbc.com/news/business/market-data")

	# check that we did not get a title
	assert title == ""

	# check that we did not get any content
	assert final_content == ""


def test_unknown_page():
	with open(os.path.dirname(os.path.abspath(__file__))+'/test_data/unknown_page.txt', 'r') as test_data:
		content = test_data.read()

	title, final_content = extract_story(content, "https://www.bbc.com/worklife/article/20200401-covid-19-why-we-wont-run-out-of-food-during-coronavirus")

	# check that we did not get a title
	assert title == ""

	# check that we did not get any content
	assert final_content == ""
