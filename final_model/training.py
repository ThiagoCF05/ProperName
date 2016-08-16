__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 15/08/2016
Description:
    This script aims to count words based on the result of the word2voc.py script for probabilistic reasons
"""

import cPickle as p
import json
import nltk
import settings

# CONTENT SELECTION
# calculate count(s | e)
def s_given_e(voc):
    grams = map(lambda x: (x['label'], x['entity']), voc)
    return dict(nltk.FreqDist(grams))

# calculate givenness count(dg | s, e)
def discourse_given_s(voc):
    grams = map(lambda x: (x['givenness'], x['label'], x['entity']), voc)
    return dict(nltk.FreqDist(grams))

# calculate sentence givenness count(sg | s, e)
def sentence_given_s(voc):
    grams = map(lambda x: (x['sentence-givenness'], x['label'], x['entity']), voc)
    return dict(nltk.FreqDist(grams))

# calculate count(syntax | s, e)
def syntax_given_s(voc):
    grams = map(lambda x: (x['syntax'], x['label'], x['entity']), voc)
    return dict(nltk.FreqDist(grams))

# REALIZATION
# calculate entity given w count(e | w)
def entity_given_w(voc):
    grams = map(lambda x: (x['entity'], x['word']), voc)
    return dict(nltk.FreqDist(grams))

# calculate count(s | w, e)
def s_given_we(voc, bigram=False):
    if bigram:
        grams = map(lambda x: (x['label'], x['bigram'][0], x['bigram'][1], x['entity']), voc)
    else:
        grams = map(lambda x: (x['label'], x['word'], x['entity']), voc)
    return dict(nltk.FreqDist(grams))

# calculate entity given w count(w | e)
def w_given_e(voc, bigram=False):
    if bigram:
        grams = map(lambda x: (x['bigram'][0], x['bigram'][1], x['entity']), voc)
    else:
        grams = map(lambda x: (x['word'], x['entity']), voc)
    return dict(nltk.FreqDist(grams))

def run(train_set, bigram=False, out='wtd'):
    # CONTENT SELECTION
    s_e = s_given_e(train_set)
    discourse_se = discourse_given_s(train_set)
    sentence_se = sentence_given_s(train_set)
    syntax_se = syntax_given_s(train_set)

    # REALIZATION
    e_w = entity_given_w(train_set)
    s_we = s_given_we(train_set, bigram)
    w_e = w_given_e(train_set, bigram)

    train_set = {
        'e_w': e_w,
        'content': {
            's_e': s_e,
            'discourse_se': discourse_se,
            'sentence_se': sentence_se,
            'syntax_se': syntax_se
        },
        'realization': {
            's_we': s_we,
            'w_e': w_e
        }
    }

    laplace = {
        'content': {
            's_e': 28,
            'discourse_se': 2,
            'sentence_se': 2,
            'syntax_se': 3,
            },
        'realization': {
            's_we': 28,
            'w_e': len(set(map(lambda x: x['word'], train_set)))
        }
    }

    if out=='wtd':
        p.dump(results, open('/roaming/tcastrof/names/stats/stats.pickle', 'w'))
    return train_set, laplace

if __name__ == '__main__':
    vocabulary = json.load(open('/roaming/tcastrof/names/stats/attrib2voc.json'))
    vocabulary = filter(lambda x: x['label'] in settings.labels, vocabulary)
    entities = set(map(lambda x: x['entity'], vocabulary))

    results = run(vocabulary, True, 'wtd')