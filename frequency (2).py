from collections import Counter
from itertools import chain
from string import punctuation
import re
import pickle
import random
import pyConTextNLP.itemData as ItemData

import os
import json

import pyConTextNLP.pyConTextGraph as pyConText
import pyConTextNLP.helpers as helpers
import unicodecsv
from wordcloud import WordCloud


filtered_words = []

file = '' #FILE_PATH
rand = random.randint(1,500000)
print(rand)


def countInFile(filename):
    if filename.lower().endswith(('.txt','.csv','.rtf','.doc',)): # Checking file type
        with open(filename) as f:
            linewords = (line.translate(None, punctuation).lower().split() for line in f)

            x = Counter(chain.from_iterable(linewords))
            with open('freq' + str(rand) + '.pickle', 'wb') as handle:
                pickle.dump(x, handle, protocol=pickle.HIGHEST_PROTOCOL)
            #pycontext logic

            freq1, freq2,freq3,freq4 = x.most_common(4)

            data = ItemData(
                [freq1],[freq2],[freq3],[freq4]) # grabbing just the top 4 frequent words for the itemData

            markup = pyConText.ConTextMarkup()
            markup.setRawText(filename.lower())
            markup.cleanText()
            #markup.markItems(modifiers, mode="modifier")
            #print(markup.nodes(data=True))
            #print(type(markup.nodes()[0]))


            #generating visual aid
            cloud = WordCloud().generate_from_frequencies(x).to_file('image.png')

            with open('cloud' + str(rand) + '.pickle', 'wb') as handle:
                pickle.dump(cloud, handle, protocol=pickle.HIGHEST_PROTOCOL)
            x.pop('to',None)
            #converting to json
            data = json.dumps(x)
            json_data = json.loads(data)
            for key, value in sorted(json_data.iteritems(), key=lambda (k, v): (v, k), reverse=True):
                k = list(key)

    elif filename.lower().endswith(('.docx','.odt','.pdf','.xlsx')):
        print('Please convert to readable file type, I.E. (.txt)')
    else:
        print('Invalid file type')
        return
countInFile(file)