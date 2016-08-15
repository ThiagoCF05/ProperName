__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 25/07/2016
Description:
    This script aims to count words based on the result of the word2voc.py script for probabilistic reasons
"""

import cPickle as p
import json
import nltk

# priori probability conditioned by discourse and sentence givenness
def priori_ds(entity, vocabulary):
    counts = {}

    f1 = filter(lambda x: x['entity'] == entity, vocabulary)

    # discourse and sentence new
    f2 = filter(lambda x: x['givenness'] == 'new' and x['sentence-givenness'] == 'new', f1)
    f3 = filter(lambda y: y['bigram'][1] == '*', f2)
    counts[(entity, 'new', 'new')] = dict(nltk.FreqDist(map(lambda x: x['word'], f3)))

    # discourse old and sentence new
    f2 = filter(lambda x: x['givenness'] == 'old' and x['sentence-givenness'] == 'new', f1)
    f3 = filter(lambda y: y['bigram'][1] == '*', f2)
    counts[(entity, 'old', 'new')] = dict(nltk.FreqDist(map(lambda x: x['word'], f3)))

    # discourse and sentence old
    f2 = filter(lambda x: x['givenness'] == 'old' and x['sentence-givenness'] == 'old', f1)
    f3 = filter(lambda y: y['bigram'][1] == '*', f2)
    counts[(entity, 'old', 'old')] = dict(nltk.FreqDist(map(lambda x: x['word'], f3)))

    return counts

# priori probability conditioned by syntax, and discourse and sentence givenness
def priori_sds(entity, vocabulary):
    counts = {}

    f1 = filter(lambda x: x['entity'] == entity, vocabulary)

    # subject / discourse and sentence new
    f2 = filter(lambda x: x['givenness'] == 'new' and x['sentence-givenness'] == 'new' and x['syntax'] == 'np-subj', f1)
    f3 = filter(lambda y: y['bigram'][1] == '*', f2)
    counts[(entity, 'new', 'new', 'np-subj')] = dict(nltk.FreqDist(map(lambda x: x['word'], f3)))

    # object / discourse and sentence new
    f2 = filter(lambda x: x['givenness'] == 'new' and x['sentence-givenness'] == 'new' and x['syntax'] == 'np-obj', f1)
    f3 = filter(lambda y: y['bigram'][1] == '*', f2)
    counts[(entity, 'new', 'new', 'np-obj')] = dict(nltk.FreqDist(map(lambda x: x['word'], f3)))

    # subj-det / discourse and sentence new
    f2 = filter(lambda x: x['givenness'] == 'new' and x['sentence-givenness'] == 'new' and x['syntax'] == 'subj-det', f1)
    f3 = filter(lambda y: y['bigram'][1] == '*', f2)
    counts[(entity, 'new', 'new', 'subj-det')] = dict(nltk.FreqDist(map(lambda x: x['word'], f3)))

    # subject / discourse old and sentence new
    f2 = filter(lambda x: x['givenness'] == 'old' and x['sentence-givenness'] == 'new' and x['syntax'] == 'np-subj', f1)
    f3 = filter(lambda y: y['bigram'][1] == '*', f2)
    counts[(entity, 'old', 'new', 'np-subj')] = dict(nltk.FreqDist(map(lambda x: x['word'], f3)))

    # object / discourse old and sentence new
    f2 = filter(lambda x: x['givenness'] == 'old' and x['sentence-givenness'] == 'new' and x['syntax'] == 'np-obj', f1)
    f3 = filter(lambda y: y['bigram'][1] == '*', f2)
    counts[(entity, 'old', 'new', 'np-obj')] = dict(nltk.FreqDist(map(lambda x: x['word'], f3)))

    # subj-det / discourse old and sentence new
    f2 = filter(lambda x: x['givenness'] == 'old' and x['sentence-givenness'] == 'new' and x['syntax'] == 'subj-det', f1)
    f3 = filter(lambda y: y['bigram'][1] == '*', f2)
    counts[(entity, 'old', 'new', 'subj-det')] = dict(nltk.FreqDist(map(lambda x: x['word'], f3)))

    # subject / discourse and sentence old
    f2 = filter(lambda x: x['givenness'] == 'old' and x['sentence-givenness'] == 'old' and x['syntax'] == 'np-subj', f1)
    f3 = filter(lambda y: y['bigram'][1] == '*', f2)
    counts[(entity, 'old', 'old', 'np-subj')] = dict(nltk.FreqDist(map(lambda x: x['word'], f3)))

    # object / discourse and sentence old
    f2 = filter(lambda x: x['givenness'] == 'old' and x['sentence-givenness'] == 'old' and x['syntax'] == 'np-obj', f1)
    f3 = filter(lambda y: y['bigram'][1] == '*', f2)
    counts[(entity, 'old', 'old', 'np-obj')] = dict(nltk.FreqDist(map(lambda x: x['word'], f3)))

    # subj-det / discourse and sentence old
    f2 = filter(lambda x: x['givenness'] == 'old' and x['sentence-givenness'] == 'old' and x['syntax'] == 'subj-det', f1)
    f3 = filter(lambda y: y['bigram'][1] == '*', f2)
    counts[(entity, 'old', 'old', 'subj-det')] = dict(nltk.FreqDist(map(lambda x: x['word'], f3)))

    return counts

# calculate count(w_t | w_tm1, e)
def wt_given_wtm1(voc):
    grams = map(lambda x: (x['bigram'][1], x['bigram'][0], x['entity']), voc)
    return dict(nltk.FreqDist(grams))

# calculate givenness count(d | w, e)
def discourse_given_w(voc, bigram=False):
    if bigram:
        grams = map(lambda x: (x['givenness'], tuple(x['bigram']), x['entity']), voc)
    else:
        grams = map(lambda x: (x['givenness'], x['word'], x['entity']), voc)
    return dict(nltk.FreqDist(grams))

# calculate sentence givenness count(s | w, e)
def sentence_given_w(voc, bigram=False):
    if bigram:
        grams = map(lambda x: (x['sentence-givenness'], tuple(x['bigram']), x['entity']), voc)
    else:
        grams = map(lambda x: (x['sentence-givenness'], x['word'], x['entity']), voc)
    return dict(nltk.FreqDist(grams))

# calculate entity given w count(e | w)
def entity_given_w(voc):
    grams = map(lambda x: (x['entity'], x['word']), voc)
    return dict(nltk.FreqDist(grams))

# calculate entity given w count(syntax | w, e)
def syntax_given_w(voc, bigram=False):
    if bigram:
        grams = map(lambda x: (x['syntax'], tuple(x['bigram']), x['entity']), voc)
    else:
        grams = map(lambda x: (x['syntax'], x['word'], x['entity']), voc)
    return dict(nltk.FreqDist(grams))

def run(vocabulary, entities, bigram=False):
    _priori = {}

    for e in entities:
        print e, '\r',
        _priori.update(priori_sds(e, vocabulary))

    wt_wtm1 = wt_given_wtm1(vocabulary)
    discourse_w = discourse_given_w(vocabulary, bigram)
    sentence_w = sentence_given_w(vocabulary, bigram)
    entity_w = entity_given_w(vocabulary)
    syntax_w = syntax_given_w(vocabulary, bigram)

    results = {
        'priori': _priori,
        'wt_wtm1': wt_wtm1,
        'dg_w': discourse_w,
        'sg_w': sentence_w,
        'e_w': entity_w,
        's_w': syntax_w
    }

    return results

if __name__ == '__main__':
    vocabulary = json.load(open('/roaming/tcastrof/names/stats/attrib2voc.json'))
    entities = set(map(lambda x: x['entity'], vocabulary))

    results = run(vocabulary, entities)
    p.dump(results, open('/roaming/tcastrof/names/stats/stats.pickle', 'w'))