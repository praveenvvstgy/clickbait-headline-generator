from scrapy.spiders import Spider
import nltk
import json
import re
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

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

		parser = PlaintextParser.from_string(body, Tokenizer("spanish"))
		stemmer = Stemmer("spanish")

		summarizer = Summarizer(stemmer)
		summarizer.stop_words = get_stop_words("spanish")

		body = summarizer(parser.document, 3)

		body = map(lambda x: "<s>" + str(x) + "</s>", body)
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