import sys
import os

import time
from bs4 import BeautifulSoup
import re

from db import Stories, Ftselinkstories
import json


def proc_normal_story(soup: BeautifulSoup):

	# get the title of the story by finding its html element
	title = soup.find("h1")
	print(title.text)

	final_content = ""

	# find where the html div containing the story
	story_body = soup.find("div", {"class": "story-body__inner"})

	# get all the story content inside the p elements
	for content in story_body.find_all("p"):
		print(content.text)
		final_content +=  content.text + " "

	return title.text, final_content


def proc_index_page(html):

	# extract story json because the html is hard to parse
	# find where json starts and ends, so we can reach the content
	start = html.split("window.__component_data__['index-page'] = ")
	start_part = start[1]
	content = start_part.split("</script>")[0].rstrip().rstrip(";")
	page_json =  json.loads(content)
	
	# get the index page title in json
	title = page_json['title']

	# find all the index stories in json
	stories_list = page_json['topStories']['stories']['items']

	final_content = ""

	# loop over stories to get their content
	for selected_story in stories_list:
		print("title: ", selected_story['title'])

		final_content +=  selected_story['title'] + " " 
		
		if('summary' in selected_story):
			final_content += selected_story['summary'] + " "
		else: 
			# some articles don't have a summary 
			print("No summary")

	return title, final_content
	

def proc_video_page(soup: BeautifulSoup):

	
	body = soup.find("div", {"class": "vxp-media__body"})
	# get the title of the story by finding its html element
	title = body.find("h1")
	print(title.text)

	# find the story text inside the html
	summary = body.find("div", {"class": "vxp-media__summary"})

	final_content = ""

	for content in summary.find_all("p"):
		print(content.text)
		final_content += content.text + " "
		
	return title.text, final_content

"""
The BBC has different kinds of story pages linked on it's business page.
To extract the text of these pages we have to treat each type differently.
This function checks what kind of page the html is,and processes it
"""
def extract_story(html, url):
	soup = BeautifulSoup(html, "html.parser")

	# handle the index page of the business section
	if(soup.find("div", {"id": "index-page"}) is not None):
		print("story is Index page")
		title, final_content = proc_index_page(html)

	# Normal articles have this format
	elif(soup.find("div", {"class": "story-body__inner"}) is not None):
		print("story is Normal article page / live reporting page")
		title, final_content = proc_normal_story(soup)

	# Video pages with short stories
	elif(soup.find("div", {"class": "vxp-media__body"}) is not None):
		print("story is Video page")
		title, final_content = proc_video_page(soup)

	# Market data pages - no useful text to process
	elif(url == "https://www.bbc.com/news/business/market-data"):
		print("Market data - ignoring")
		title = ""
		final_content = ""

	else:
		# sometimes the BBC links general interest articles on it's business pages
		# these articles are usually hidden far down the page, so we are ignoring these types
		print("story is Unkown story type - not business related")
		title = ""
		final_content = ""

	return title, final_content

# the main function of the text extraction
def text_extract():

	# find DB rows with text title in Stories table
	# this is the new rows that need text extraction 
	query = Stories.select().where(Stories.text_title.is_null())
	
	# loop over new rows and extract
	for story in query:
		print("processing story id: ", story.id)

		title, final_content = extract_story(story.html, story.url)

		# insert the title, story content inside the relevant row and save them
		story.text_title = title
		story.text_content = final_content.rstrip()
		story.save()



if __name__ == "__main__":
	text_extract()