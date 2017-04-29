# -*- coding: utf-8 -*-
import glob
import sys

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
# from sumy.summarizers.kl import KLSummarizer as Summarizer
# from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

reload(sys)
sys.setdefaultencoding('utf-8')
lang = "spanish"
sent_count = 5

def get_top_sentences(data, count):
	parser = PlaintextParser.from_string(data, Tokenizer(lang))
	stemmer = Stemmer(lang)
	summarizer = Summarizer(stemmer)
	summarizer.stop_words = get_stop_words(lang)

	return summarizer(parser.document, count)

if __name__ == "__main__":
	file1 = open("train(1).enc")
	file2 = open("train(1).dec")
	output_file = open("data", "w")
	counter = 1
	for article, headline in zip(file1, file2):
		data = "article=<d><p>"
		top_sents = get_top_sentences(article, sent_count)
		for sent in top_sents:
			data += "<s>" + str(sent) + "</s>"
		data += "</p></d>\t"
		data += "abstract=<d><p>" + headline.rstrip("\n") + "</p></d>\n"
		output_file.write(data)
		print "{} out of 798 done.".format(counter)
		counter += 1
	