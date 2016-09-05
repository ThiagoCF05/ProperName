from eacl.models import Bayes

__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 15/08/2016
Description:
    Main method EACL 2017 model and baselines
"""

import json
import numpy as np
import operator
import os
import preprocessing

from sklearn.cross_validation import KFold

mention_dir = '/roaming/tcastrof/names/eacl/mentions'
parsed_dir = '/roaming/tcastrof/names/regnames/parsed'

def bayes_model(mention, entity, model, mentions):
    features = {
        # 's_e': mention['label'],
        'discourse_se': mention['givenness'],
        'sentence_se': mention['sentence-givenness'],
        'syntax_se': mention['syntax']
    }

    # CONTENT SELECTION
    prob = model.select_content(features, entity)
    prob = sorted(prob.items(), key=operator.itemgetter(1))
    prob.reverse()

    # REALIZATION
    #TO DO: review this penalty function
    # compute the frequency of the words in the sentence (words that are not part of the mention)
    # parsed = json.load(open(os.path.join(parsed_dir, mention['fname'])))['sentences'][mention['sentNum']-1]
    # mentions_same_entity = filter(lambda x: x['fname'] == mention['fname'] and x['sentNum'] == mention['sentNum'], mentions)
    # words_freq = dict(preprocessing.word_freq(mentions_same_entity, parsed))

    words_freq = {}
    realizer = model.realize(prob[0][0], entity, words_freq)

    # Save results
    result = {
        'content': {
            'R': mention['label'],
            'P': prob
        },
        'realization': {
            'R': mention['text'],
            'P': realizer
        },
        'giveness': mention['givenness'],
        'sentence-givenness': mention['sentence-givenness'],
        'syntax': mention['syntax'],
        'entity': entity
    }
    return result

def run():
    # filter entities and their references (more than 49 references)
    results = {}
    references = preprocessing.filter_entities(49, mention_dir)

    for entity in references:
        results[entity] = {}

        # Retrieve all the mentions to the entity
        mentions = np.array(references[entity])

        # compute cross validation
        fold = 1
        kf = KFold(mentions.shape[0], n_folds=10)
        for train, test in kf:
            results[entity][fold] = []

            # train and test sets
            train_set, test_set = mentions[train], mentions[test]

            # compute the set of features (vocabulary) for the bayes model
            vocabulary = []
            for mention in train_set:
                parsed = json.load(open(os.path.join(parsed_dir, mention['fname'])))
                vocabulary.extend(preprocessing.process_tokens(mention, parsed, entity, False))

            # initialize our official model
            clf = Bayes(vocabulary, True)
            for mention in test_set:
                # Bayes model
                result = bayes_model(mention, entity, clf, mentions)
                results[entity][fold].append(result)
            fold = fold + 1
    json.dump(results, open('results.json', 'w'))

if __name__ == '__main__':
    run()