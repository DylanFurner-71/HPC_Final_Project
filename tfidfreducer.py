#!/usr/bin/env python

import sys
import csv
from math import log10
from collections import defaultdict

words = []										# liste de mots
last_word_docid_pair = None									# pour le calcul du wordcount
df_t_dict = defaultdict(lambda: set())				# pour le calcul du df_t
docid_list = set()										# nombre de doc dans la collection


for line in sys.stdin:
	line = line.strip()
	key,wordcount,wordcount_per_doc,df_t = line.split("\t")
	wordcount_per_doc=int(wordcount_per_doc)
	wordcount = int(wordcount)
	df_t = int(df_t)
	word,docid = key.split(",")
	docid = int(docid)
	word_docid_pair = (word,docid)
	if last_word_docid_pair is None:					
		last_word_docid_pair = word_docid_pair
		last_wordcount = 0
		last_wordcount_per_doc = wordcount_per_doc
		last_df_t = df_t
	if word_docid_pair == last_word_docid_pair:
		last_wordcount += wordcount
	else:
		words.append([last_word_docid_pair,last_wordcount,last_wordcount_per_doc,last_df_t])
		last_word_docid_pair = word_docid_pair
		last_wordcount = wordcount
		last_wordcount_per_doc = wordcount_per_doc
		last_df_t = df_t
	dic_value = df_t_dict[word]
	dic_value.add(docid)
	df_t_dict[word] = dic_value
	docid_list.add(docid)


words.append([last_word_docid_pair,last_wordcount,last_wordcount_per_doc,last_df_t])
N = len(docid_list)

for word_block in words:
	word,docid,wordcount,wordcount_per_doc,df_t = word_block[0][0],int(word_block[0][1]),int(word_block[1]),int(word_block[2]),int(word_block[3])
	df_t = len(df_t_dict[word])
	# Calcule TF-IDF = wordcount x wordcount_per_doc x log10(N/df_t)
	word_block.append(wordcount * wordcount_per_doc * log10(N/df_t))
	TFIDF = word_block[4]
	# 7. ***OUTPUT DATA*** | ensemble de paires ((mot, doc_ID), TF-IDF) sur chaque ligne de stdout
	key_formated = '{:_<30}'.format("%s,%i" % (word,docid))
	print("%s\t%i\t%i\t%i\t%.*f" % (key_formated,wordcount,wordcount_per_doc,df_t,5,TFIDF))

# for docid in docid_list:
# 	words_top20_tfidf = sorted([word_block for word_block in words if word_block[0][1] == docid], key=lambda x: x[4], reverse=True)[:20]
# 	document_name = 'words_top20_tfidf_docid'
# 	document_name +="%s" %(docid)
	#with open('%s.csv' % document_name, 'w') as f:
	#	csv.writer(f).writerow(words_top20_tfidf)