# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, unicode_literals

import math
import itertools
import glob
import nltk
import string

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer

import sys

reload(sys)
sys.setdefaultencoding("utf-8")
class TopicSigGen():
	
	def __init__(self, sentences):
		self.stop_words = nltk.corpus.stopwords.words('spanish') + nltk.corpus.stopwords.words("english")
		self.sentences = sentences

	def get_keywords(self):
		return self._get_topic_signatures(self.sentences)

	def _get_topic_signatures(self, document):
		with open("vocab_data") as f:
			vocab = {x.strip().split()[0]: int(x.strip().split()[1]) for x in f.readlines()}
		all_words = vocab.keys()
		all_words_in_rel_doc = self._get_all_content_words_in_doc(document)
		relevant_word_freq = self._compute_word_freq(all_words_in_rel_doc)
		total_word_freq = vocab
		total_words = sum(vocab.values())
		total_words_in_rel_doc = len(all_words_in_rel_doc)
		topic_signatures = {}
		p = total_words_in_rel_doc/total_words
		cutoff = 10.3 #10.83 given in paper
		#print (list(set(all_words_in_rel_doc)))
		for w in list(set(all_words_in_rel_doc)):
			#print (w)
			try:
				p1 = relevant_word_freq[w]/(total_word_freq[w])
				if p1 == 1.0 or p1 > 1:
					p1 = 0.9999
				p2 = (total_words_in_rel_doc - relevant_word_freq[w])/(total_words - total_word_freq[w])
				if p2 == 1.0 or p2 > 1:
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
		normalized_words = list(itertools.chain.from_iterable([s.split() for s in sentences]))
		normalized_content_words = [w for w in normalized_words if w not in self.stop_words]
		return normalized_content_words

	def _get_content_words_in_sentence(self, sentence):
		normalized_words = [self.normalize_word(w) for w in sentence.words]   
		normalized_content_words = [w for w in normalized_words if w not in self.stop_words]
		return normalized_content_words

	def _compute_ratings(self, sentences, document):       
		sentences_list = list(sentences)
		topic_signatures = self._get_topic_signatures(document)
		ratings = {}
		for s in sentences:
			sentence_as_words = self._get_content_words_in_sentence(s)
			ratings[s] = self._get_rating_of_sentence(sentence_as_words, topic_signatures)    
		return (ratings)

	def _get_rating_of_sentence(self, sentence_as_a_word,topic_signature):
		Score = sum([topic_signature[w] for w in sentence_as_a_word if topic_signature.has_key(w)])
		return Score

	def _get_all_words(self):
		all_words = []
		for filename in glob.glob("D*"):
			parser = PlaintextParser.from_file(filename, Tokenizer("spanish"))
			all_words += self._get_all_content_words_in_doc(parser.document.sentences)
		return all_words

	def _compute_word_freq(self, list_of_words):
		word_freq = {}
		for w in list_of_words:
			if w not in self.stop_words:
			   word_freq[w] = word_freq.get(w, 0) + 1
			else:
				word_freq[w] = word_freq.get(w, 0) + 0
		return word_freq

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

	topic_signatures = TopicSigGen(nltk.tokenize.sent_tokenize(body)).get_keywords()

	actual_score = len(set(actual_headline.split()).intersection(set(topic_signatures)))/len(set(actual_headline.split()))
	generated_score = len(set(generated_headline.split()).intersection(set(topic_signatures)))/len(set(generated_headline.split()))
	actual_scores.append(actual_score)
	generated_scores.append(generated_score)
	print "Index: ", index, ", Actual = ", actual_score, ", Generated =", generated_score

print "Actual Average ", sum(actual_scores)/len(actual_scores)
print "Generated Average ", sum(generated_scores)/len(generated_scores)
# sidd = Summarist(nltk.tokenize.sent_tokenize(body))
# A = sidd.get_keywords()
# print sorted(A, key=A.get)[-10:]