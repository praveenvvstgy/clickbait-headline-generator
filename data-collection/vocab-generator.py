# -*- coding: utf-8 -*-
import json
import codecs
import re
import nltk.tokenize
from nltk.probability import FreqDist

words = []
with codecs.open("spanish_data.json") as json_file:
	data = json.load(json_file)
	for record in data:
		headline = record["headline"]
		headline = re.sub(r"\n", " ", headline).strip()
		headline = re.sub(r"<d>", "", headline).strip()
		headline = re.sub(r"</d>", "", headline).strip()
		headline = re.sub(r"<p>", "", headline).strip()
		headline = re.sub(r"</p>", "", headline).strip()
		headline = re.sub(r"abstract=", "", headline).strip()
		body = record["body"]
		body = re.sub(r"<d>", "", body).strip()
		body = re.sub(r"</d>", "", body).strip()
		body = re.sub(r"<p>", "", body).strip()
		body = re.sub(r"</p>", "", body).strip()
		body = re.sub(r"article=", "", body).strip()
		words.append(headline)
		words.append(body)
words = " ".join(words)
words = nltk.tokenize.word_tokenize(words)
fdist = FreqDist(words)

print fdist

with codecs.open("vocab_data", "w") as vocab_file:
	for word, count in fdist.iteritems():
		line = word + " " + str(count) + "\n"
		line = line.encode("utf-8")
		vocab_file.write(line)
