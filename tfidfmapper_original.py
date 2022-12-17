#!/usr/bin/env python

import sys
import re

words = []
wordcount = 1
wordcount_per_doc = 0
df_t = 1
doc_id = 1
for line in sys.stdin:
    line = line.strip()
    #doc_id = os.environ["mapred_job_id"]

    words_in_line = line.split()
    words_in_line = [word.lower() for word in words_in_line]
    words_in_line = [re.sub(r'[^\w]', '', word) for word in words_in_line]
    # filtering stop words
    stopwords = []
    words_in_line = [word for word in words_in_line if word not in stopwords]

    words_in_line = [word for word in words_in_line if len(word) > 2]
    words += words_in_line
    wordcount_per_doc += len(words_in_line)
for word in words:
    print("%s,%i\t%i\t%i\t%i" % (word, doc_id, wordcount, wordcount_per_doc, df_t))
