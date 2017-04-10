from scrapy.spiders import Spider
import nltk
import json
import re

class BuzzFeedSpider(Spider):
	name = "buzzfeedextractor"
	with open('langstats.json') as url_file:
		start_urls = [record["url"] for record in json.load(url_file) if record["lang"] == "es"]

	def parse(self, response):
		stopwords = ["\n", "BuzzFeed", "Staff", "Mexico", "Share", "On", "facebook", "pinterest", "lineapp", "twitter", "email", "whatsapp", "more", "tumblr", "stumbleupon", "linkedin", "reddit", "googleplus", "link", "@", "Compartir", "Ver comentarios en Facebook", "Pin", "sms", "more", "This Link", "vk", "View this image", "Sponsored", "EDIT", "Photography", "Please select the newsletters you'd like to receive.", "Oops! We had a problem sending your message."]
		body = nltk.clean_html(" ".join(response.css("#js-post-container .clearfix").extract()))
		if len(body) == 0:
			body = nltk.clean_html(" ".join(response.css("[id^=superlist_]").extract()))
		for word in stopwords:
			body = body.replace(word, '')
		body = re.sub(r"\t", " ", body).strip()
		body = re.sub(r"\s+", " ", body).strip()
		body = re.sub('Twitter: \w+', ' ', body).strip()
		body = nltk.tokenize.sent_tokenize(body)
		body = map(lambda x: "<s>" + x + "</s>", body)
		body = " ".join(body)
		body = re.sub(r"=", " ", body).strip()
		body = "article=<d><p>" + body + "</p></d>"
		headline = response.css(".buzz-title::text").extract_first()
		if headline == None:
			headline = response.css("#post-title::text").extract_first()
		headline = re.sub(r"=", " ", headline).strip()
		headline = "abstract=<d><p><s>" + headline + "</s></p></d>"
		yield { 
		"headline": headline if headline is not None else response.url,
		"body": body
		}