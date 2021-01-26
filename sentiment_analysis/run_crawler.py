import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import Ftse
from get_ftse_value import get_ftse_value
from crawler import start_crawler



def run_crawler():
	# get current ftse value
	new_ftse_value = get_ftse_value()
	print("New ftse value:", str(new_ftse_value))

	# save it to the database
	ftse_value = Ftse.create(value=new_ftse_value)


	# get the id of the new entry so we can connect it with the news
	# pages we will scrape
	ftse_id = ftse_value.id

	start_crawler(ftse_id)


	print('Done')


if __name__ == "__main__":
	run_crawler()