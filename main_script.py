__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 14/09/2016
Description:
    Main method EACL 2017 model and baselines (Version 2)
    Appliying Individual Variation
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
from random import randint, shuffle
from sklearn.cross_validation import KFold

fdbpedia = '/roaming/tcastrof/names/eacl/name_base.json'
fentities = '/roaming/tcastrof/names/eacl/entities.json'
titles_dir = '/roaming/tcastrof/names/eacl/all_titles.json'
appositives_dir = '/roaming/tcastrof/names/eacl/appositives.json'
mention_dir = '/roaming/tcastrof/names/eacl/mentions'
parsed_dir = '/roaming/tcastrof/names/regnames/parsed'
vocabulary_dir = '/roaming/tcastrof/names/eacl/stats/voc.json'
evaluation_dir = '/roaming/tcastrof/names/eacl/evaluation/intrinsic'

# initialize vocabulary, dbpedia, entities, appositives and vocabulary
def init():
    print 'Initializing appositives...'
    appositives = json.load(open(appositives_dir))
    print 'Initializing entities_info...'
    entities_info = json.load(open(fentities))

    print 'Initializing titles...'
    titles = json.load(open(titles_dir))
    dbpedia = json.load(open(fdbpedia))

    print 'Initializing dbpedia...'
    base = {}
    for entity in dbpedia:
        base[entity] = []
        base[entity].extend(dbpedia[entity]['first_names'])
        base[entity].extend(dbpedia[entity]['middle_names'])
        base[entity].extend(dbpedia[entity]['last_names'])

        # insert END token
        base[entity].append('END')

        base[entity].extend(titles)
        base[entity] = list(set(base[entity]))

    return entities_info, base, appositives, dbpedia

def bayes_selection(features, entity, model, k):
    if k != None:
        prob = model.select_content_backoff(features, entity, k)
    else:
        prob = model.select_content(features, entity)
    return prob

def bayes_variation(references, form_distribution, test_set_same_features, entity, model, words, appositive, name):
    distribution = {}
    for form in form_distribution:
        distribution[form[0]] = len(references) * form[1]

    shuffle(references)
    for i, reference in enumerate(references):
        form = filter(lambda x: distribution[x] == max(distribution.values()), distribution.keys())[0]

        label = filter(lambda x: x[0] == form, form_distribution)[0]
        realizer = model.realizeWithWords(form, entity, test_set_same_features[i]['syntax'], words, appositive)
        references[i][name] = { 'label': label, 'reference': realizer }

        distribution[form] -= 1
    return references

def process_entity(entity, words, mentions, dbpedia, appositive, fname):
    results = {}

    # compute cross validation
    fold = 1
    kf = KFold(mentions.shape[0], n_folds=10)
    for train, test in kf:
        print 'Fold', str(fold)
        results[fold] = []

        # train and test sets
        train_set, test_set = mentions[train], mentions[test]

        # compute the set of features (vocabulary) for the bayes model
        content_vocabulary, realization_vocabulary = [], []
        for mention in train_set:
            parsed = json.load(open(os.path.join(parsed_dir, mention['fname'])))

            content_data, realization_data = prep.process_tokens(mention, parsed, entity, False)
            content_vocabulary.append(content_data)
            realization_vocabulary.extend(realization_data)

        # Consider data from other entities in the training set
        # content_vocabulary.extend(general_voc)

        # initialize our official model
        clf = Bayes(content_vocabulary, realization_vocabulary, True)
        # initialize random baseline
        baseline_random = Random(dbpedia=dbpedia)
        # initialize Siddharthan baseline
        baseline1 = Siddharthan(dbpedia=dbpedia)
        # initialize Deemter baseline
        baseline2 = Deemter(dbpedia=dbpedia, parsed_dir=parsed_dir)


        for _givenness in ['new', 'old']:
            for _sgivenness in ['new', 'old']:
                for _syntax in ['np-subj', 'np-obj', 'subj-det']:
                    # Group proper name references from the test fold by feature values
                    test_set_same_features = filter(lambda x: x['givenness'] == _givenness \
                                                              and x['sentence-givenness'] == _sgivenness \
                                                              and x['syntax'] == _syntax, test_set)

                    features = {
                        # 's_e': mention['label'],
                        'discourse_se': _givenness,
                        'sentence_se': _sgivenness,
                        'syntax_se': _syntax
                    }

                    # Bayes model selection
                    form_distribution = bayes_selection(features, entity, clf, None)

                    # Siddharthan model
                    siddharthan_result = baseline1.run(entity, _givenness, _syntax)

                    # Bayes model with no variation (Realization with the most likely referential form)
                    bayes_result = clf.realizeWithWords(form_distribution[0][0], entity, _syntax, words, appositive)

                    # Generate proper names for each group of features
                    group_result = []
                    for filtered_mention in test_set_same_features:
                        result = {
                            'real': {
                                'label': filtered_mention['label'],
                                'reference': filtered_mention['text']
                            },
                            'features': {
                                'giveness': filtered_mention['givenness'],
                                'sentence-givenness': filtered_mention['sentence-givenness'],
                                'syntax': filtered_mention['syntax']
                            }
                        }

                        # Random model
                        r = baseline_random.run(entity, filtered_mention['syntax'])
                        result['random'] = { 'label': r[0], 'reference': r[1] }

                        result['siddharthan'] = { 'label': siddharthan_result[0], 'reference': siddharthan_result[1] }

                        # Deemter model
                        ms = json.load(open(os.path.join(mention_dir, filtered_mention['fname'])))[entity]
                        r = baseline2.run(entity, filtered_mention, ms, 3, filtered_mention['syntax'])
                        result['deemter'] = { 'label': r[0], 'reference': r[1] }

                        result['bayes_no_variation'] = { 'label': form_distribution[0], 'reference': bayes_result }

                        # Bayes model with random choice of proper name form
                        index = randint(0, len(form_distribution)-1)
                        realizer = clf.realizeWithWords(form_distribution[index][0], entity, filtered_mention['syntax'], words, appositive)
                        result['bayes_random'] = { 'label': form_distribution[index], 'reference': realizer }

                        group_result.append(result)

                    # Generate proper names with individual variation in the for choice
                    group_result = bayes_variation(group_result, form_distribution, test_set_same_features, entity, clf, words, appositive, 'bayes_variation')
                    results[fold].extend(group_result)
        fold = fold + 1
    print 'Saving results for ', str(entity)
    p.dump(results, open(os.path.join(evaluation_dir, fname), 'w'))
    print 10 * '-'

def run():
    if not os.path.exists(evaluation_dir):
        os.makedirs(evaluation_dir)

    # filter entities and their references (more than X references and less than Y)
    print 'Filter entities and their references (more than X references and less than Y)'
    references = prep.filter_entities(50, 0, mention_dir)

    # voc contains only the proper names / titles from DBpedia for each entity
    entities_info, tested_words, appositives, dbpedia = init()

    # Sort entities and start the process
    entities = references.keys()
    entities.sort()

    number_mentions = 0

    for entity in entities:
        # get entity id in our corpus
        entity_id = filter(lambda x: x['url'] == entity, entities_info)[0]['id']
        if not os.path.exists(os.path.join(evaluation_dir, entity_id)):
            print entity
            # Get appositive
            if entity in appositives:
                appositive = appositives[entity]
            else:
                appositive = ''

            # Get proper nouns to be tested whether should be included in the reference
            words = tested_words[entity]

            # pool.apply_async(func=process_entity, args=(entity, words, references[entity], vocabulary, dbpedia, appositive, entity_id))
            process_entity(entity, words, np.array(references[entity]), dbpedia, appositive, entity_id)
            number_mentions = number_mentions + len(references[entity])
    print 'Number of entities: ', len(entities)
    print 'Number of mentions: ', number_mentions

if __name__ == '__main__':
    run()