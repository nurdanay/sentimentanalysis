
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from db import Stories, Ftselinkstories

sia = SentimentIntensityAnalyzer()



def get_sentiment(text):
	'''
	Computes the sentiment score of a given text.
	'''
	sentiment_score = sia.polarity_scores(text)['compound']
	return sentiment_score


def proc_sentiment():

	# select the empty rows of content sentiment from Stories table in database 
	query = Stories.select().where(Stories.content_sentiment.is_null())
	for story in query:
		# compute the sentiment score of titles 
		title = story.text_title
		title_sentiment = get_sentiment(title)

		# compute sentiment score of each stories' content 
		content = story.text_content
		content_sentiment = get_sentiment(content)

		# insert the sentiment scores inside the relevant column and save them
		story.title_sentiment = title_sentiment
		story.content_sentiment = content_sentiment
		story.save()

		print("Sentiment: ", content_sentiment, " Title: ", title)


	
if __name__ == "__main__":
	proc_sentiment()

