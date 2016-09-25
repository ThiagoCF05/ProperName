__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 15/08/2016
Description:
    This script aims to prepare a training and test set of our corpus.
    It also extract the features to train our proposed bayesian model for words (stats/voc.json)
"""

import os
import json
import preprocessing as prep

def process_tokens(mention, parsed, entity, filtered = False):
    '''
    :param mention: mention information
    :param parsed: parsed text where the mention is
    :param entity: entity mentioned
    :param filtered: should only the tokens among proper nouns be filtered?
    :return: set of features (word, previous word, entity, givenness, sentence givenness and syntax)
    '''
    def get_tokens():
        sentence = mention['sentNum'] - 1
        if mention['startIndex'] > 2:
            start = mention['startIndex']-3
        elif mention['startIndex'] > 1:
            start = mention['startIndex']-2
        else:
            start = mention['startIndex']-1
        end = mention['endIndex']-1

        tokens = parsed['sentences'][sentence]['tokens'][start:end]

        if filtered:
            PNs = []
            for i, token in enumerate(tokens):
                if token['pos'] == 'NNP' or token['ner'] == 'TITLE':
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
            'bigram': (token['word'], prev),
            'entity': entity,
            'givenness': mention['givenness'],
            'sentence-givenness': mention['sentence-givenness'],
            'syntax': mention['syntax'],
            'label': mention['label']
        }
        prev = token['word']
        data.append(t)

    t = {
        'word': 'END',
        'bigram': ('END', prev),
        'entity': entity,
        'givenness': mention['givenness'],
        'sentence-givenness': mention['sentence-givenness'],
        'syntax': mention['syntax'],
        'label': mention['label']
    }
    data.append(t)
    return data

def run(N, out='wtd'):
    root_dir = '/roaming/tcastrof/names'
    mention_dir = os.path.join(root_dir, 'eacl', 'mentions')
    parsed_dir = os.path.join(root_dir, 'regnames', 'parsed')

    data = prep.filter_entities(N, 0, mention_dir)

    content_voc, realization_voc = {}, {}
    for i, entity in enumerate(data):
        print i+1, entity
        voc[entity] = []
        fnames = map(lambda x: x['fname'], data[entity])

        for fname in fnames:
            parsed = json.load(open(os.path.join(parsed_dir, fname)))

            mentions = filter(lambda x: x['fname'] == fname, data[entity])

            for mention in mentions:
                content_data, realization_data = prep.process_tokens(mention, parsed, entity, False)
                content_voc[entity].append(content_data)
                realization_voc[entity].extend(realization_data)

    if out == 'wtd':
        json.dump(content_voc, open('/roaming/tcastrof/names/eacl/stats/content_voc.json', 'w'), separators=(',',':'))
        json.dump(realization_voc, open('/roaming/tcastrof/names/eacl/stats/realization_voc.json', 'w'), separators=(',',':'))
    return data

if __name__ == '__main__':
    run(50)