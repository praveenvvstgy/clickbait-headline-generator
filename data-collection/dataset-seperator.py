# -*- coding: utf-8 -*-
import json
import codecs
import re

enc = []
dec = []
with codecs.open("spanish_data.json", "r", "utf-8") as json_file, codecs.open("text_data", "w", "utf-8") as text_data:
	data = json.load(json_file)
	for record in data:
		enc.append(record["body"])
		dec.append(record["headline"])
		headline = record["headline"]
		body = record["body"]
		headline = re.sub(r"\n", " ", headline).strip()
		line = body + "\t" + headline + "\n"
		text_data.write(line)


with codecs.open("train.enc", "w", "utf-8") as train_enc_file:
	for line in enc:
		line = re.sub("article=<d><p><s>", "", line).strip()
		line = re.sub("</s></p></d>", "", line).strip()
		line = re.sub("</s> <s>", "", line).strip()
		line = line + "\n"
		train_enc_file.write(line)

with codecs.open("train.dec", "w", "utf-8") as train_dec_file:
	for line in dec:
		line = re.sub(r"\n", " ", line).strip()
		line = re.sub("abstract=<d><p><s>", "", line).strip()
		line = re.sub("</s></p></d>", "", line).strip()
		line = line + "\n"
		train_dec_file.write(line)