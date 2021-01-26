import argparse

from sentiment_plot import plot_graph1
from sentiment_plot2 import plot_graph2

from run_crawler import run_crawler
from text_extract import text_extract
from sentiment_analysis import proc_sentiment
from sentiment_accumulation import sentiment_accumulation



def get_argument_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description="Investigate the correlation between Ftse values and BBC business news")
	
	parser.add_argument("-d", "--data", help="Do crawl of the FTSE value and current bbc stories and store them in the database. Do data analysis and store results in the DB", action="store_true")
	parser.add_argument("-g", "--graphs", help="Show graphs for existing data in the database", action="store_true")

	return parser


def do_data():
	print("Starting data crawling")
	run_crawler()
	print("Completed crawling, starting data analysis")

	print("Extracting text")
	text_extract()

	print("Processing sentiment")
	proc_sentiment()

	print("Accumulating sentiment")#
	sentiment_accumulation()

	print("Completed data analysis.")


def show_graphs():
	print("Starting showing graphs")
	plot_graph1()
	plot_graph2()

	print("Completed showing graphs")


def main():
	parser = get_argument_parser()
	args = parser.parse_args()

	if args.data:
		do_data()

	if args.graphs:
		show_graphs()

	print("Program complete")



if __name__ == "__main__":
	main()

	
