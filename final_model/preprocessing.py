__author__ = 'thiagocastroferreira'

import json
import nltk
import os

def word_freq(mentions, sentence):
    intervals = map(lambda x: (x['startIndex']-1, x['endIndex']-1), mentions)

    words = []
    for i, token in enumerate(sentence['tokens']):
        if len(filter(lambda x: x[0] >= i >= x[1], intervals)) == 0:
            words.append(token['word'])

    return nltk.FreqDist(words)

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
def filter_entities(N, mention_dir):
    '''
    :param N: only entities with more than N mentions should be considered
    :param mention_dir: directory where the mention files are present
    :return:
    '''
    result = {}

    files = os.listdir(mention_dir)
    for i, fname in enumerate(files):
        print i, fname, '\r',
        mentions = json.load(open(os.path.join(mention_dir, fname)))

        for entity in mentions:
            if entity not in result:
                result[entity] = []
            for mention in filter(lambda mention: mention['type'] == 'PROPER', mentions[entity]):
                mention['fname'] = fname
                result[entity].append(mention)

    return dict(map(lambda x: (x, result[x]), filter(lambda e: len(result[e]) > N, result.keys())))