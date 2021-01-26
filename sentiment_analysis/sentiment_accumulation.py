from peewee import *

from db import Stories, Ftselinkstories, Ftse



def sentiment_accumulation():

	# get the empty rows of cumulative sentiment column from FTSE table
	query = Ftse.select().where(Ftse.cumulative_sentiment.is_null())

	for ftse in query:
		ftse_id = ftse.id 

		# get the ftse id, get the all articles related to this ftse id. We need the sentiment score of each articles.
		# So, we link to the Stories table and get the content sentiment column. 
		link_table = Ftselinkstories.select(Stories.content_sentiment).join(Stories).where((Ftselinkstories.stories_id == Stories.id) & (Ftselinkstories.ftse_id == ftse_id ))

		# number of articles in 15 min-interval
		count = 0

		# total sentiment score of all the articles inside the 15 min-interval
		sentiment_accumulator = 0


		for links in link_table:#
			
			# get the sentiment score of each content
			content_sentiment = links.stories.content_sentiment

			# add it to total score
			sentiment_accumulator += content_sentiment

			# increment the article number
			count += 1

		# compute the average sentiment score of all the articles inside 15 min-interval 
		average_sentiment = sentiment_accumulator / count

		# insert the average sentiment score inside the relevant column in database and save
		ftse.cumulative_sentiment = average_sentiment
		ftse.save()
		print ("ftse id:", ftse_id, "cumulative sentiment: ", average_sentiment)


if __name__ == "__main__":
	sentiment_accumulation()		
