import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

from db import Ftse


def plot_graph2():

	y1 = []
	y2 = []
	dates = []


	sentiment_tracker = 0

	query = Ftse.select().limit(2000)
	for sample in query:

		sentiment = sample.cumulative_sentiment
		# if the sentiment of the text is positive, add 1 to the tracker
		if(sentiment > 0):
			sentiment_tracker += 1
		# if the sentiment of the text is negative, subtrack 1 from the tracker
		else:
			sentiment_tracker -= 1
		
		# y1 axis shows the ftse value
		y1.append(sample.value)
		# y2 axis shows the sentiemnt score
		y2.append(sentiment_tracker)
		# x axis shows the dates
		dates.append(sample.timestamp)


	fig, ax1 = plt.subplots()

	color = 'tab:red'
	ax1.set_xlabel('Date')
	ax1.set_ylabel('ftse value', color=color)
	ax1.plot(dates, y1, color=color)
	ax1.tick_params(axis='y', labelcolor=color)

	ax2 = ax1.twinx()


	color = 'tab:blue'
	ax2.set_ylabel('tracked sentiment', color=color)  # we already handled the x-label with ax1
	ax2.plot(dates, y2, color=color)
	ax2.tick_params(axis='y', labelcolor=color)

	fig.tight_layout()  # otherwise the right y-label is slightly clipped
	plt.title("CORRELATION OF BUSINESS NEWS ARTICLES SENTIMENT AND FTSE VALUE WITH A DIFFERENT SENTIMENT SCORE METHOD ")
	plt.show()


if __name__ == "__main__":
	plot_graph2()	