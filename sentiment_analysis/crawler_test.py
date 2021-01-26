import pytest
from crawler import *


def test_crawl_page_get_content_good_url():
	link =  "https://www.google.com"
	content = crawl_page_get_content(link)
	
	# check we got bytes back from crawling the URL
	assert isinstance(content, bytes)

	# check the content contains the word "Google" in the title
	assert b"<title>Google" in content
	

def test_crawl_page_get_content_bad_url():
	link =  "https://www.google23459898dsf98092345kjsdkfujiu24359dffffzzz.com"
	content = crawl_page_get_content(link)

	# when we crawl a bad url we should just get an empty string back
	assert isinstance(content, str)

def test_extract_links():
	target = "https://www.bbc.com/news/business"
	
	with open(os.path.dirname(os.path.abspath(__file__))+'/../test_data/business_page.txt', 'r') as test_data:
		content = test_data.read()

	links = extract_links(target, content)

	# check we got a set of links back
	assert isinstance(links, set)

	# check we got the 57 article links in the test data
	links_len = len(links)

	assert links_len == 57


