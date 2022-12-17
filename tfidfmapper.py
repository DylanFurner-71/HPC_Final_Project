#!/usr/bin/env python

import sys
import re
import string
#sys.path.append('./')

words = []

wordcount = 1
wordcount_per_doc = 0
df_t = 1
doc_id = 1
stopwords1 = "gutenberg,https,http,i,me,my,myself,we,our,ours,ourselves,you,your,yours,yourself,yourselves,he,him,his,himself,she,her,hers,herself,it,its,itself,they,them,their,theirs,themselves,what,which,who,whom,this,that,these,those,am,is,are,was,were,be,been,being,have,has,had,having,do,does,did,doing,a,an,the,and,but,if,or,because,as,until,while,of,at,by,for,with,about,against,between,into,through,during,before,after,above,below,to,from,up,down,in,out,on,off,over,under,again,further,then,once,here,there,when,where,why,how,all,any,both,each,few,more,most,other,some,such,no,nor,not,only,own,same,so,than,too,very,s,t,can,will,just,don,should,now"
stopwords = stopwords1.split(',')
for line in sys.stdin:
    line = line.strip()
    if ".txt" in line:
        doc_id = line.split('.txt')[0]
        if "-" in line:
            doc_id = line.split("-")[0]
    words_list = line.split('-')
    words_in_line = []
    for word in words_list:
        l = word.split()
        for element in l:
            words_in_line.append(element)
    words_in_line = [word.lower() for word in words_in_line]
    words_in_line = [re.sub(r'[^\w]', '', word) for word in words_in_line]
    words_in_line = [word for word in words_in_line if word not in stopwords]
    words_in_line = [word for word in words_in_line if len(word) > 2]
    words += words_in_line
    wordcount_per_doc += len(words_in_line)

for word in words:
    print("%s,%i\t%i\t%i\t%i" % (word, doc_id, wordcount, wordcount_per_doc, df_t))
doc_id += 1