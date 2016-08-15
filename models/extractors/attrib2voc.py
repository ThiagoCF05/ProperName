from ML.extractors import utilities

__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 26/07/2016
Description:
    This script aims to count attributes (title, first, last, etc.) based on the result of the word2voc.py
    script for probabilistic reasons
    This script aims to prepare a file with features for our proposed bayesian model for attributes
"""

import copy
import json

if __name__ == '__main__':
    furls = '/roaming/tcastrof/names/regnames/urls.txt'
    fdir = '/roaming/tcastrof/names/regnames/mentions'

    references = utilities.get_references(furls, fdir)

    classes = ['has_title', 'has_firstName', 'has_middleName', 'has_lastName', 'has_appositive']
    grams = []
    for i in range(len(classes)):
        for j in range(i+1, len(classes)):
            grams.append((classes[j], classes[i]))

    voc = []
    for entity in references:
        print entity, '\r',
        mentions = []
        for url in references[entity]:
            for mention in filter(lambda mention: mention['type'] == 'PROPER', references[entity][url]):
                prev = '*'
                empty = True
                for c in classes:
                    if mention[c]:
                        empty = False
                        t = {
                            'word': c,
                            'bigram': (c, prev),
                            'entity': entity,
                            'givenness': mention['givenness'],
                            'sentence-givenness': mention['sentence-givenness'],
                            'syntax': mention['syntax']
                        }
                        voc.append(t)
                        prev = copy.copy(c)
                if not empty:
                    t = {
                        'word': 'END',
                        'bigram': ('END', prev),
                        'entity': entity,
                        'givenness': mention['givenness'],
                        'sentence-givenness': mention['sentence-givenness'],
                        'syntax': mention['syntax']
                    }
                    voc.append(t)
    json.dump(voc, open('/roaming/tcastrof/names/regnames/stats/attrib2voc.json', 'w'), separators=(',',':'))