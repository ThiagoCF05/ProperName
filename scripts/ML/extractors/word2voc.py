__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 25/07/2016
Description:
    This script aims to prepare a file with features for our proposed bayesian model for words
"""

import os
import json

def process_tokens(mention, parsed, entity, filtered = False):
    '''
    :param mention: mention information
    :param parsed: parsed text where the mention is
    :param entity: entity mentioned
    :param filtered: should only the proper nouns be filtered?
    :return: set of features (word, previous word, entity, givenness, sentence givenness and syntax)
    '''
    def get_tokens():
        sentence = mention['sentNum'] - 1
        start, end = mention['startIndex']-1, mention['endIndex']-1

        tokens = parsed['sentences'][sentence]['tokens'][start:end]

        if filtered:
            PNs = []
            for i, token in enumerate(tokens):
                if token['pos'] == 'NNP':
                    PNs.append(i)
            if len(PNs) > 0:
                return tokens[PNs[0]:PNs[-1]+1]
            else:
                return []
        else:
            return tokens

    data = []
    tokens = get_tokens()
    prev = '*'
    for token in tokens:
        t = {
            'word': token['word'],
            'bigram': (prev, token['word']),
            'entity': entity,
            'givenness': mention['givenness'],
            'sentence-givenness': mention['sentence-givenness'],
            'syntax': mention['syntax'],
            'has_title': mention['has_title'],
            'has_appositive': mention['has_appositive']
        }
        prev = token['word']
        data.append(t)

    t = {
        'word': 'END',
        'bigram': (prev, 'END'),
        'entity': entity,
        'givenness': mention['givenness'],
        'sentence-givenness': mention['sentence-givenness'],
        'syntax': mention['syntax'],
        'has_title': mention['has_title'],
        'has_appositive': mention['has_appositive']
    }
    data.append(t)
    return data

def run():
    root_dir = '/roaming/tcastrof/names/regnames'
    mdir = os.path.join(root_dir, 'mentions')
    pdir = os.path.join(root_dir, 'parsed')

    data = []
    fdata = [] # filtered data

    files = os.listdir(mdir)
    for i, fname in enumerate(files):
        print i, fname, '\r',
        mentions = json.load(open(os.path.join(mdir, fname)))
        parsed = json.load(open(os.path.join(pdir, fname)))

        for entity in mentions:
            for mention in filter(lambda mention: mention['type'] == 'PROPER', mentions[entity]):
                data.extend(process_tokens(mention, parsed, entity, False))
                fdata.extend(process_tokens(mention, parsed, entity, True))
    json.dump(data, open('/roaming/tcastrof/names/stats/word2voc.json', 'w'), separators=(',',':'))
    json.dump(data, open('/roaming/tcastrof/names/stats/fword2voc.json', 'w'), separators=(',',':'))

if __name__ == '__main__':
    run()
