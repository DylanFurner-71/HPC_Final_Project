import sys
import zipimport
importer = zipimport.zipimporter('nltk.mod')
nltk = importer.load_module('nltk')

for line in sys.stdin:
    line = line.strip()
    if len(line) > 0:
        try:
            # Gather filename, chunk index, and senteces from mapper
            filename, chunk_index, sentences = line.strip().split('\t',2)
            # Split the sentences on backslashes
            for sentence in sentences.split('\\'):
                # Extract features from each sentence
                tokens = nltk.word_tokenize(sentence)
                # POS-tagging
                tagged = nltk.pos_tag(tokens)
                # Sentiment analyzer
                ss = sid.polarity_scores(sentence)
                polarities = []
                for k in ss:
                    polarities.append('{},{}'.format(k, ss[k]))
                print('{}\t{}\t{}\t{}'.format(filename, sentence, tagged, polarities))
        except Exception as e:
            print('FAILURE with line [{}], exception: {}'.format(line, repr(e)))
            continue