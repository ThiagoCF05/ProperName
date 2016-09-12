__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 15/08/2016
Description:
    This script aims to prepare a training and test set of our corpus.
    It also extract the features to train our proposed bayesian model for words (stats/word2voc.json)
"""

import os
import json

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

# filter entities with more than N mentions and process the mentions
def filter_entities(N, parsed_dir, mention_dir, isFilter):
    '''
    :param N: only entities with more than N mentions should be considered
    :param mention_dir: directory where the mention files are present
    :param parsed_dir: directory where the parsed files are present
    :param isFilter: when processing a reference, should only the tokens among proper nouns be filtered?
    :return:
    '''
    result = {}

    files = os.listdir(mention_dir)
    for i, fname in enumerate(files):
        print i, fname, '\r',
        mentions = json.load(open(os.path.join(mention_dir, fname)))
        parsed = json.load(open(os.path.join(parsed_dir, fname)))

        for entity in mentions:
            if entity not in result:
                result[entity] = []
            for mention in filter(lambda mention: mention['type'] == 'PROPER', mentions[entity]):
                result[entity].extend(process_tokens(mention, parsed, entity, isFilter))

    return dict(map(lambda x: (x, result[x]), filter(lambda e: len(result[e]) > N, result.keys())))

def run(N, out='wtd'):
    root_dir = '/roaming/tcastrof/names'
    mdir = os.path.join(root_dir, 'eacl', 'mentions')
    pdir = os.path.join(root_dir, 'regnames', 'parsed')

    data = reduce(lambda x, y: x+y, filter_entities(N, pdir, mdir, False).values())
    fdata = reduce(lambda x, y: x+y, filter_entities(N, pdir, mdir, True).values()) # filtered data

    if out == 'wtd':
        json.dump(data, open('/roaming/tcastrof/names/eacl/stats/word2voc.json', 'w'), separators=(',',':'))
        json.dump(fdata, open('/roaming/tcastrof/names/eacl/stats/fword2voc.json', 'w'), separators=(',',':'))
    return data, fdata

if __name__ == '__main__':
    run(49)