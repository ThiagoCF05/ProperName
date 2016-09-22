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

# calculate count(f)
def f(voc):
    grams = map(lambda x: x['label'], voc)
    return dict(nltk.FreqDist(grams))

# calculate count(f | p)
def f_given_p(voc):
    grams = map(lambda x: (x['label'], x['entity']), voc)
    return dict(nltk.FreqDist(grams))

# calculate givenness count(dg | f)
def discourse_given_f(voc):
    grams = map(lambda x: (x['givenness'], x['label']), voc)
    return dict(nltk.FreqDist(grams))

# calculate givenness count(dg | f, p)
def discourse_given_fp(voc):
    grams = map(lambda x: (x['givenness'], x['label'], x['entity']), voc)
    return dict(nltk.FreqDist(grams))

# calculate sentence givenness count(sg | f)
def sentence_given_f(voc):
    grams = map(lambda x: (x['sentence-givenness'], x['label']), voc)
    return dict(nltk.FreqDist(grams))

# calculate sentence givenness count(sg | f, p)
def sentence_given_fp(voc):
    grams = map(lambda x: (x['sentence-givenness'], x['label'], x['entity']), voc)
    return dict(nltk.FreqDist(grams))

# calculate count(syntax | f)
def syntax_given_f(voc):
    grams = map(lambda x: (x['syntax'], x['label']), voc)
    return dict(nltk.FreqDist(grams))

# calculate count(syntax | f, p)
def syntax_given_fp(voc):
    grams = map(lambda x: (x['syntax'], x['label'], x['entity']), voc)
    return dict(nltk.FreqDist(grams))

# REALIZATION
# calculate entity given w count(p | w)
def entity_given_w(voc):
    grams = map(lambda x: (x['entity'], x['word']), voc)
    return dict(nltk.FreqDist(grams))

# calculate count(s | w, p)
def s_given_wp(voc, bigram=False):
    if bigram:
        grams = map(lambda x: (x['label'], x['bigram'][0], x['bigram'][1], x['entity']), voc)
    else:
        grams = map(lambda x: (x['label'], x['word'], x['entity']), voc)
    return dict(nltk.FreqDist(grams))

# calculate entity given w count(w | p)
def w_given_p(voc, bigram=False):
    if bigram:
        grams = map(lambda x: (x['bigram'][0], x['bigram'][1], x['entity']), voc)
    else:
        grams = map(lambda x: (x['word'], x['entity']), voc)
    return dict(nltk.FreqDist(grams))

def run_content(voc, bigram=False, out='wtd'):
    # CONTENT SELECTION
    s = f(voc)
    s_e = f_given_p(voc)
    discourse_se = discourse_given_fp(voc)
    sentence_se = sentence_given_fp(voc)
    syntax_se = syntax_given_fp(voc)

    discourse_s = discourse_given_f(voc)
    sentence_s = sentence_given_f(voc)
    syntax_s = syntax_given_f(voc)

    train_set = {
        's_e': s_e,
        'discourse_se': discourse_se,
        'sentence_se': sentence_se,
        'syntax_se': syntax_se,
        's': s,
        'discourse_s': discourse_s,
        'sentence_s': sentence_s,
        'syntax_s': syntax_s
    }

    laplace = {
        's_e': 28,
        'discourse_se': 2,
        'sentence_se': 2,
        'syntax_se': 3,
    }

    if out=='wtd':
        p.dump(results, open('/roaming/tcastrof/names/stats/stats_content.pickle', 'w'))
    return train_set, laplace

def run_realization(voc, bigram=False, out='wtd'):
    # REALIZATION
    e_w = entity_given_w(voc)
    s_we = s_given_wp(voc, bigram)
    w_e = w_given_p(voc, bigram)

    train_set = {
        'e_w': e_w,
        's_we': s_we,
        'w_e': w_e
    }

    laplace = {
        's_we': 28,
        'w_e': len(set(map(lambda x: x['word'], voc)))
    }

    if out=='wtd':
        p.dump(results, open('/roaming/tcastrof/names/stats/stats_realization.pickle', 'w'))
    return train_set, laplace

def run(voc, bigram=False, out='wtd'):
    # CONTENT SELECTION
    s = f(voc)
    s_e = f_given_p(voc)
    discourse_se = discourse_given_fp(voc)
    sentence_se = sentence_given_fp(voc)
    syntax_se = syntax_given_fp(voc)

    discourse_s = discourse_given_f(voc)
    sentence_s = sentence_given_f(voc)
    syntax_s = syntax_given_f(voc)

    # REALIZATION
    e_w = entity_given_w(voc)
    s_we = s_given_wp(voc, bigram)
    w_e = w_given_p(voc, bigram)

    train_set = {
        'e_w': e_w,
        'content': {
            's_e': s_e,
            'discourse_se': discourse_se,
            'sentence_se': sentence_se,
            'syntax_se': syntax_se,
            's': s,
            'discourse_s': discourse_s,
            'sentence_s': sentence_s,
            'syntax_s': syntax_s
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
            'w_e': len(set(map(lambda x: x['word'], voc)))
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