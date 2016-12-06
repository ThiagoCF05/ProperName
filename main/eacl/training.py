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
# calculate count(w | w_m1, f, p)
def w_given_wm1fp(voc, bigram=True):
    if bigram:
        grams = map(lambda x: (x['bigram'][0], x['bigram'][1], x['label'], x['entity']), voc)
    else:
        grams = map(lambda x: (x['word'], x['label'], x['entity']), voc)
    return dict(nltk.FreqDist(grams))

# form attribute by person
def elem_given_p(voc):
    elem_p = []
    for v in voc:
        for elem in v['label_elems']:
            elem_p.append((elem, v['entity']))
    return dict(nltk.FreqDist(elem_p))

# calculate entity given w count(p | w)
def entity_given_w(voc):
    grams = map(lambda x: (x['entity'], x['word']), voc)
    return dict(nltk.FreqDist(grams))

# calculate count(s | w, p)
def s_given_wp(voc, bigram=True):
    if bigram:
        grams = map(lambda x: (x['label'], x['bigram'][0], x['bigram'][1], x['entity']), voc)
    else:
        grams = map(lambda x: (x['label'], x['word'], x['entity']), voc)
    return dict(nltk.FreqDist(grams))

# calculate entity given w count(w | p)
def w_given_p(voc, bigram=True):
    if bigram:
        grams = map(lambda x: (x['bigram'][0], x['bigram'][1], x['entity']), voc)
    else:
        grams = map(lambda x: (x['word'], x['entity']), voc)
    return dict(nltk.FreqDist(grams))

def run_content(voc):
    # CONTENT SELECTION
    s = f(voc)
    s_e = f_given_p(voc)
    discourse_se = discourse_given_fp(voc)
    sentence_se = sentence_given_fp(voc)
    syntax_se = syntax_given_fp(voc)
    elem_p = elem_given_p(voc)

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
        'syntax_s': syntax_s,
        'elem_p': elem_p
    }

    laplace = {
        's_e': len(settings.labels),
        'discourse_se': len(settings.features['givenness']),
        'sentence_se': len(settings.features['sentence-givenness']),
        'syntax_se': len(settings.features['syntax']),
    }
    return train_set, laplace

def run_realization(voc, bigram=True):
    # REALIZATION
    e_w = entity_given_w(voc)
    w_wm1fe = w_given_wm1fp(voc, bigram)

    train_set = {
        'e_w': e_w,
        'w_wm1fe': w_wm1fe
    }
    return train_set