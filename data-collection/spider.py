import requests
from bs4 import BeautifulSoup
import json

def parse_sitemap(url):
	resp = requests.get(url)
	
	# we didn't get a valid response, bail
	if 200 != resp.status_code:
		return False
	
	# BeautifulStoneSoup to parse the document
	soup = BeautifulSoup(resp.content)
	
	# find all the <url> tags in the document
	sitemaps = soup.findAll('sitemap')
	
	# no sitemaps? bail
	if not sitemaps:
		return False

	child_sitemaps = []

	for sitemap in sitemaps:
		loc = sitemap.find('loc').string
		child_sitemaps.append(loc)
	
	out = []
	#extract what we need from the url
	for child_sitemap in child_sitemaps:
		sitemap_resp = requests.get(child_sitemap)
		if 200 != sitemap_resp.status_code:
			continue
		soup = BeautifulSoup(sitemap_resp.content)
		urls = soup.find_all('url')
		for url in urls:
			loc = url.find('loc').string
			out.append(loc)
	return out

urls = parse_sitemap("https://www.buzzfeed.com/sitemaps/en-us/sitemap_all.xml")

with open("urls.json", "w") as url_file:
	json.dump(urls, url_file)