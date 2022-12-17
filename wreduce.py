#!/usr/bin/python
from operator import itemgetter
import sys
import nltk
nltk.download('maxent_treebank_pos_tagger')

cur_word = None
cur_count = 0
word = None
# for line in sys.stdin:
#     line = line.strip()
#     word, count = line.split('\t', 1)
#     count = int(count)
#     if cur_word == word:
#         cur_count += count
#     else:
#         if cur_word:
#             print '%s\t%s' % (cur_word, cur_count)
#             cur_count = count
#             cur_word = word
#     if cur_word == word:
#         print '%s\t%s' % (cur_word, cur_count)