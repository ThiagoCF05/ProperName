__author__ = 'thiagocastroferreira'

import json
import nltk
import os

# return the proper name form
def get_label(name, dbpedia):
    label = ''
    # Check first name
    for first in dbpedia['first_names']:
        if str(first).lower() in str(name).lower():
            label = label + '+f'
            break

    # Check middle name
    for middle in dbpedia['middle_names']:
        if str(middle).lower() in str(name).lower():
            label = label + '+m'
            break

    # Check last name
    for last in dbpedia['last_names']:
        if str(last).lower() in str(name).lower():
            label = label + '+l'
            break

    return label

def word_freq(mentions, sentence):
    intervals = map(lambda x: (x['startIndex']-1, x['endIndex']-1), mentions)

    words = []
    for i, token in enumerate(sentence['tokens']):
        if len(filter(lambda x: i in range(x[0], x[1]+1), intervals)) == 0:
            words.append(token['word'])

    return nltk.FreqDist(words)

# prepare the set of features to train our bayes model
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

    # CONTENT SELECTION
    # elements from the form
    elems = []
    if '+f' in mention['label']:
        elems.append('+f')
    if '+m' in mention['label']:
        elems.append('+m')
    if '+l' in mention['label']:
        elems.append('+l')
    if '+t' in mention['label']:
        elems.append('+t')
    if '+a' in mention['label']:
        elems.append('+a')

    content_data = {
        'entity': entity,
        'givenness': mention['givenness'],
        'sentence-givenness': mention['sentence-givenness'],
        'syntax': mention['syntax'],
        'label': mention['label'],
        'label_elems': elems
    }

    realization_data = []
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
        realization_data.append(t)

    t = {
        'word': 'END',
        'bigram': ('END', prev),
        'entity': entity,
        'givenness': mention['givenness'],
        'sentence-givenness': mention['sentence-givenness'],
        'syntax': mention['syntax'],
        'label': mention['label']
    }
    realization_data.append(t)
    return content_data, realization_data

# filter entities with more than N mentions and process the mentions
def filter_entities(N_min, N_max, mention_dir):
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

        # Exclude this entity from the set
        entities = filter(lambda x: x != 'http://en.wikipedia.org/wiki/Whoopi_Goldberg', mentions)
        for entity in entities:
            if entity not in result:
                result[entity] = []
            for mention in filter(lambda mention: mention['type'] == 'PROPER', mentions[entity]):
                mention['fname'] = fname
                result[entity].append(mention)
    if N_max == 0:
        return dict(map(lambda x: (x, result[x]), filter(lambda e: len(result[e]) >= N_min, result.keys())))
    else:
        return dict(map(lambda x: (x, result[x]), filter(lambda e: N_min <= len(result[e]) <= N_max, result.keys())))