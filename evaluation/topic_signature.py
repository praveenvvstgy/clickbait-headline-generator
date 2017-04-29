# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, unicode_literals

import math
import itertools
import glob
import nltk
import string

from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

class TopicSigGen():
	
	def __init__(self):
		self.tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')
		self.stemmer = SnowballStemmer('spanish',ignore_stopwords=True)
		self.stop_words = nltk.corpus.stopwords.words('spanish') + nltk.corpus.stopwords.words("english")
		# self.all_words = self._get_all_words()
		with open('all_words.txt') as f:
			self.all_words = map(lambda x: x.strip(), f.readlines())
		self.total_word_freq = self._compute_word_freq(self.all_words)

	def get_keywords(self, sentences):
		return self._get_topic_signatures(sentences, self.all_words, self.total_word_freq)

	def _get_topic_signatures(self, document, all_words, total_word_freq):
		all_words_in_rel_doc = self._get_all_content_words_in_doc(document)
		relevant_word_freq = self._compute_word_freq(all_words_in_rel_doc)
		
		total_words = len(all_words)
		total_words_in_rel_doc = len(all_words_in_rel_doc)
		topic_signatures = {}
		p = total_words_in_rel_doc/total_words
		cutoff = 10.83 
		for w in list(set(all_words_in_rel_doc)):
			#print (w)
			try:
				p1 = relevant_word_freq[w]/(total_word_freq[w])
				if p1 == 1.0 :
					p1 = 0.9999
				p2 = (total_words_in_rel_doc - relevant_word_freq[w])/(total_words - total_word_freq[w])
				if p2 == 1.0 :
					p2 = 0.9999
				elif p2 == 0:
					p2 = 0.0001
				o11 = relevant_word_freq[w]
				o12 = total_word_freq[w] - relevant_word_freq[w]
				# if o12 == 0:
				#     o12 = 1
				o21 = total_words_in_rel_doc - relevant_word_freq[w]
				o22 = total_words - total_words_in_rel_doc - o12

				print ("p = {6}, p1 = {0}, p2 = {1}, o11 = {2}, o12 = {3}, o21 = {4}, o22 = {5}".format(p1,p2,o11,o12,o21,o22, p))
				weight = -2 * ((o11 + o21) * math.log(p) + (o12 + o22) * math.log(1-p) - (o11 * math.log(p1) + o12 * math.log(1-p1) + o21 * math.log(p2) + o22 * math.log(1-p2)))
				if weight >= cutoff:
					topic_signatures[w] = topic_signatures.get(w, 0) + weight
			except KeyError:
				print "ignoring", w
		return topic_signatures
		

	def _get_all_content_words_in_doc(self, sentences):
		normalized_words = list(itertools.chain.from_iterable([word_tokenize(str(s.lower()).translate(None, string.punctuation)) for s in sentences]))
		normalized_content_words = [w for w in normalized_words if w not in self.stop_words]
		return normalized_content_words


	def _get_rating_of_sentence(self, sentence_as_a_word,topic_signature):
		Score = sum([topic_signature[w] for w in sentence_as_a_word if topic_signature.has_key(w)])
		return Score

	def _get_all_words(self):
		all_words = []
		for filename in glob.glob("train.enc"):
			sentences = self.tokenizer.tokenize(open(filename).read().decode('utf-8'))
			all_words += self._get_all_content_words_in_doc(sentences)
		print "Done"
		return all_words

	def _compute_word_freq(self, list_of_words):
		word_freq = {}
		for w in list_of_words:
			if w not in self.stop_words:
			   word_freq[w] = word_freq.get(w, 0) + 1
			else:
				word_freq[w] = word_freq.get(w, 0) + 0
		return word_freq

# def Count():
ts = TopicSigGen()

print "counting done"
with open("test-output.txt") as f:
	headlines = map(lambda x: x.strip(), f.readlines())

actual_headlines = {}
generated_headlines = {}

for index, headline in enumerate(headlines):
	idx, headline = headline.split("$$$$")
	if index %2 == 0:
		actual_headlines[int(idx)] = str(headline).translate(None, string.punctuation)
	else:
		generated_headlines[int(idx)] = str(headline).translate(None, string.punctuation)

with open("train.enc") as f:
	body_text = map(lambda x: str(x).strip().translate(None, string.punctuation), f.readlines())

actual_scores = []
generated_scores = []
for index in actual_headlines.keys():
	actual_headline = actual_headlines[index].lower()
	generated_headline = generated_headlines[index].lower()
	body = body_text[index].lower()

	topic_signatures = ts.get_keywords(nltk.tokenize.sent_tokenize(body))

	actual_score = len(set(actual_headline.split()).intersection(set(topic_signatures)))/len(set(actual_headline.split()))
	generated_score = len(set(generated_headline.split()).intersection(set(topic_signatures)))/len(set(generated_headline.split()))
	actual_scores.append(actual_score)
	generated_scores.append(generated_score)
	# print "Index: ", index, ", Actual = ", actual_score, ", Generated =", generated_score
	# raw_input()

print "Actual Average ", sum(actual_scores)/len(actual_scores)
print "Generated Average ", sum(generated_scores)/len(generated_scores)