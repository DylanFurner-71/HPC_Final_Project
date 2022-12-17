#!/usr/bin/env python

import sys

sys.path.append('./')
from cleaning_functions import find_title, find_author, clean_end_of_text, clean_start_of_text

title = ""
author = ""
lines = []
for line in sys.stdin:
    line = line.strip()
    lines.append(line)
    if author == "":
        author = find_author(line)
    if title == "":
        title = find_title(line)

if author == "":
    author = "not_known"
if title == "":
    title = "not_known"

text = " ".join(lines)

# text = sys.stdin.readlines()
text = clean_end_of_text(text)
text = clean_start_of_text(text, title, author)
author_title = str(author + "-" + title + "--")
# one option
print('%s\t%s' % (author_title, text))
# another option not sure which is right
# print '%s\t%s' % (author_title, text)