from bs4 import	 BeautifulSoup
import json
import requests
from langdetect import detect

url_file = "urls.json"
output_file = "output.json"

extracted_content = []

def extract_page(url):
	resp = requests.get(url)

	if resp.status_code != 200:
		return False

	soup = BeautifulSoup(resp.content)

	for script in soup(["script", "style"]):
		script.extract()

	headline = get_headline(soup)
	if headline == None:
		print url
	else:
		body = get_body(soup)
		if body == None:
			print url
			exit(1)
		else:
			record = {
				"HEADLINE": headline,
				"BODY": body,
				"lang": detect(headline + " " + body)
				}
			print record
			extracted_content.append(record)


def get_headline(soup):
	headline = None
	if len(soup.select('#post-title')) > 0:
		headline = soup.select('#post-title')
	elif len(soup.select(".buzz-title")) > 0:
		headline = soup.select('.buzz-title')
	
	if headline:
		headline = get_plain_text(headline)
	return headline

def get_body(soup):
	body = None
	if len(soup.select('#js-post-container')) > 0:
		body = soup.select('#js-post-container')
	elif len(soup.select("hgroup p")) > 0:
		body = soup.select('hgroup p')
	
	if body:
		body = get_plain_text(body)
	return body

def get_plain_text(soup_content):
	stripped_strings = map(lambda x: x.stripped_strings, soup_content)
	return " ".join(map(lambda x: " ".join(x), stripped_strings))


with open(url_file) as input_file:
	urls = json.load(input_file)
	for url in urls[:]:
		extract_page(url)

with open(output_dataset) as output_file:
	json.dump(extracted_content, output_file)
