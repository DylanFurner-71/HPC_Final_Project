#!/usr/bin/env python

import sys
sys.path.append('./')
from cleaning_functions import find_title, find_author, clean_end_of_text, clean_start_of_text, check_start_of_text
title = ""
author = ""
lines = []
start_of_text = False
end_of_text = False
doc_id = 1
for line in sys.stdin:
    line = line.strip() #remove extra whitespaces
    if not start_of_text:
        line, start_of_text = check_start_of_text(line, start_of_text) #check if this line gives a signifier that we have started the text
    if author == "":
        author = find_author(line)
    if title == "":
        title = find_title(line)
    if not start_of_text:
        doc_id += 1
        continue
    else:
        if not end_of_text:
            if author == "" and title == "":
                    print("%s,\t%i\t%i\t%i" % (doc_id, str("unknown title"), str("unknown author"), line))
            else:
                if author == "":
                    print("%s,\t%i\t%s\t%i" % (doc_id, title, "unknown author", line))
                else:
                    print("%s,\t%i\t%i\t%i" % (doc_id, -1, author, line))
doc_id += 1

