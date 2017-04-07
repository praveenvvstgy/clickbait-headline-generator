# -*- coding: utf-8 -*-
import json
import codecs
import re

enc = []
dec = []
with codecs.open("spanish_data.json") as json_file:
	data = json.load(json_file)
	for record in data:
		enc.append(record["body"])
		dec.append(record["headline"])

with codecs.open("train.enc", "w") as train_enc_file:
	for line in enc:
		line = line + "\n"
		line = line.encode("utf-8")
		train_enc_file.write(line)

with codecs.open("train.dec", "w") as train_dec_file:
	for line in dec:
		line = re.sub(r"\n", " ", line).strip()
		line = line + "\n"
		line = line.encode("utf-8")
		train_dec_file.write(line)