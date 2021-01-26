import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

from db import Ftse


def plot_graph1():
	y1 = []
	y2 = []
	dates = []

	query = Ftse.select().limit(2000)
	for sample in query:
		# y1 axis shows the ftse value
		y1.append(sample.value)
		# y2 axis shows the sentiment score
		y2.append(sample.cumulative_sentiment)
		# x axis shows the dates
		dates.append(sample.timestamp)


	fig, ax1 = plt.subplots()

	color = 'tab:red'
	ax1.set_xlabel('Date')
	ax1.set_ylabel('ftse value', color=color)
	# put the y1 axis into the plot
	ax1.plot(dates, y1, color=color)
	ax1.tick_params(axis='y', labelcolor=color)

	ax2 = ax1.twinx()


	color = 'tab:blue'
	ax2.set_ylabel('sentiment', color=color)  # we already handled the x-label with ax1
	# put the y2 axis into the plot
	ax2.plot(dates, y2, color=color)
	ax2.tick_params(axis='y', labelcolor=color)

	fig.tight_layout()  # otherwise the right y-label is slightly clipped
	plt.title("CORRELATION OF BUSINESS NEWS ARTICLES SENTIMENT AND FTSE VALUES")
	plt.show()



if __name__ == "__main__":
	plot_graph1()	