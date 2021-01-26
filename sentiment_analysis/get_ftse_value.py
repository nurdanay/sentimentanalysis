import requests as _requests
import json as _json


scrape_url = 'https://finance.yahoo.com/quote/^FTSE'


def get_ftse_value():

	# get html data from yahoo finance
	html = _requests.get(scrape_url).text

	# retry if data missing
	if "QuoteSummaryStore" not in html:
		html = _requests.get(scrape_url).text
		if "QuoteSummaryStore" not in html:
			return 0

	# extract json data from html
	json_str = html.split('root.App.main =')[1].split(
		'(this)')[0].split(';\n}')[0].strip()

	# extract current FTSE value from json data
	json_data = _json.loads(json_str)
	ftse_value = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['price']['regularMarketPrice']['raw']

	return ftse_value

