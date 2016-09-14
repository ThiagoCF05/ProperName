__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 15/08/2016
Description:
    Main method EACL 2017 model and baselines
"""

import cPickle as p
import json
import numpy as np
import os

import main.eacl.preprocessing as prep

from main.eacl.models.Bayes import Bayes
from main.eacl.models.random_baseline import Random
from main.eacl.models.siddharthan import Siddharthan
from main.eacl.models.deemter import Deemter
from sklearn.cross_validation import KFold

fdbpedia = '/roaming/tcastrof/names/eacl/name_base.json'
fentities = '/roaming/tcastrof/names/eacl/fentities.json'
titles_dir = '/roaming/tcastrof/names/eacl/titles.json'
appositives_dir = '/roaming/tcastrof/names/eacl/appositives.json'
mention_dir = '/roaming/tcastrof/names/eacl/mentions'
parsed_dir = '/roaming/tcastrof/names/regnames/parsed'

# initialize vocabulary, dbpedia, entities and appositives
def init():
    appositives = json.load(open(appositives_dir))
    entities_info = json.load(open(fentities))

    titles = json.load(open(titles_dir))
    dbpedia = json.load(open(fdbpedia))

    base = {}
    for entity in dbpedia:
        base[entity] = []
        base[entity].extend(dbpedia[entity]['first_names'])
        base[entity].extend(dbpedia[entity]['middle_names'])
        base[entity].extend(dbpedia[entity]['last_names'])

        # insert END token
        base[entity].append('END')

        if entity in titles:
            base[entity].extend(titles[entity])
        base[entity] = list(set(base[entity]))

    return entities_info, base, appositives, dbpedia

def bayes_model(mention, entity, model, words, appositive):
    features = {
        # 's_e': mention['label'],
        'discourse_se': mention['givenness'],
        'sentence_se': mention['sentence-givenness'],
        'syntax_se': mention['syntax']
    }

    # CONTENT SELECTION
    prob = model.select_content(features, entity)

    # REALIZATION
    #TO DO: review this penalty function
    # compute the frequency of the words in the sentence (words that are not part of the mention)
    # parsed = json.load(open(os.path.join(parsed_dir, mention['fname'])))['sentences'][mention['sentNum']-1]
    # mentions_same_entity = filter(lambda x: x['fname'] == mention['fname'] and x['sentNum'] == mention['sentNum'], mentions)
    # words_freq = dict(preprocessing.word_freq(mentions_same_entity, parsed))

    realizer = model.realizeWithWords(prob[0][0], entity, mention['syntax'], words, appositive)

    # Save results
    result = {
        'label': prob[0],
        'reference': realizer
    }
    return result

def run():
    evaluation_dir = '/roaming/tcastrof/names/eacl/evaluationV2'
    if not os.path.exists(evaluation_dir):
        os.makedirs(evaluation_dir)

    # filter entities and their references (more than X references and less than Y)
    results = {}
    references = prep.filter_entities(50, 0, mention_dir)

    # dbpedia contains only the proper names / titles from DBpedia for each entity
    entities_info, voc, appositives, dbpedia = init()

    # Sort entities and start the process
    entities = references.keys()
    entities.sort()
    for entity in entities:
        # get entity id in our corpus
        entity_id = filter(lambda x: x['url'] == entity, entities_info)[0]['id']
        if not os.path.exists(os.path.join(evaluation_dir, entity_id)):
            print entity
            results[entity] = {}

            # Get appositive
            if entity in appositives:
                appositive = appositives[entity]
            else:
                appositive = ''

            # Get proper nouns to be tested whether should be included in the reference
            words = voc[entity]

            # Retrieve 500 mentions to the entity
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

                    tokens = prep.process_tokens(mention, parsed, entity, False)
                    vocabulary.extend(tokens)

                # initialize our official model
                clf = Bayes(vocabulary, True)
                # initialize random baseline
                baseline_random = Random(dbpedia=dbpedia)
                # initialize Siddharthan baseline
                baseline1 = Siddharthan(dbpedia=dbpedia)
                # initialize Deemter baseline
                baseline2 = Deemter(dbpedia=dbpedia, parsed_dir=parsed_dir)

                for mention in test_set:
                    result = {
                        'real': {
                            'label': mention['label'],
                            'reference': mention['text']
                        },
                        'features': {
                            'giveness': mention['givenness'],
                            'sentence-givenness': mention['sentence-givenness'],
                            'syntax': mention['syntax']
                        }
                    }

                    # Bayes model
                    result['bayes'] = bayes_model(mention, entity, clf, words, appositive)

                    # Random model
                    r = baseline_random.run(entity)
                    result['random'] = { 'label': r[0], 'reference': r[1] }

                    # Siddharthan model
                    r = baseline1.run(entity, mention['givenness'], mention['syntax'])
                    result['siddharthan'] = { 'label': r[0], 'reference': r[1] }

                    # Deemter model
                    ms = json.load(open(os.path.join(mention_dir, mention['fname'])))[entity]
                    r = baseline2.run(entity, mention, ms, 3, mention['syntax'])
                    result['deemter'] = { 'label': r[0], 'reference': r[1] }

                    results[entity][fold].append(result)
                    # print result
                    # print 10 * '-'
                fold = fold + 1
            p.dump(results[entity], open(os.path.join(evaluation_dir, entity_id), 'w'))
    # p.dump(results, open('EVALUATION.pickle', 'w'))

if __name__ == '__main__':
    run()