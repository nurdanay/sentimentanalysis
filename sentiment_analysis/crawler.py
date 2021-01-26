import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from urllib.request import urlopen, urljoin
from bs4 import BeautifulSoup

from db import Stories, Ftselinkstories

def start_crawler(ftse_id: int):
	
	# get home page
	target = "https://www.bbc.com/news/business"
	homepage_html = crawl_page_get_content(target)

	# save home page content
	story = Stories.create(
		is_top_level=True, 
		html=homepage_html, 
		url=target
	)

	# add the top level business page story the link table
	story = Ftselinkstories.create(
		ftse_id=ftse_id,
		stories_id=story.id
	)

	# extract connected articles in the page downloaded above
	new_links = extract_links(target, homepage_html)

	# download and save connected articles
	for link in new_links:
		# responsible scraping, sleep for a bit
		time.sleep(0.5)
		process_article_page(link, ftse_id)


	print('Done with scrape')


def process_article_page(link: str, ftse_id: int):

	story_id = None

	# checks if we already downloaded this article url into our stories table
	count = Stories.select().where(Stories.url==link).count()

	# if the story url exists we have a count of 1
	if(count >= 1):
		# if we already downloaded the story, we just link to it 
		# and do not download it again
		story = Stories.get(Stories.url==link)
		story_id = story.id

		print("Duplicate story found for url: ",link, " story id: ", story_id)

	else:
		print("Downloading new story for  ", link )
		article_html = crawl_page_get_content(link)

		# only create a new db story entry if we received some html
		if(article_html != ""):
			story = Stories.create(
				is_top_level=False, 
				html=article_html, 
				url=link
			)

			story_id = story.id

	# if there isn't a story found or newly downloaded, we don't create a link
	if(story_id != None):
		link = Ftselinkstories.create(
			ftse_id=ftse_id,
			stories_id=story_id
		)	
		

def extract_links(target: str, html: str) -> set:
	soup = BeautifulSoup(html, "html.parser")
	new_links = set()

	# get all the links
	for link in soup.find_all("a"):
		new_url = urljoin(target, link.get("href")).strip("/").split("#")[0]

		# all bbc article links contain a hypen
		# so we only add those
		if "-" in new_url:
			new_links.add(new_url)

	return new_links


def crawl_page_get_content(link: str) -> str:
	# note in the code below we swallow any errors / exceptions in fetching 
	# specific pages because we want the crawler to keep going
	html = ""
	try:
		page = urlopen(link)
		html = page.read()
	except ValueError:
		print("bad link (", link, ")")
	except:
		print("Could not open ", link)

	return html


if __name__ == "__main__":
	start_crawler(1)
