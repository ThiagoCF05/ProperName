__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 14/09/2016
Description:
    Main method EACL 2017 model and baselines (Version 2)
    Appliying Individual Variation
"""

import copy
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
titles_dir = '/roaming/tcastrof/names/eacl/titles.json'
appositives_dir = '/roaming/tcastrof/names/eacl/appositives.json'
mention_dir = '/roaming/tcastrof/names/eacl/mentions'
parsed_dir = '/roaming/tcastrof/names/regnames/parsed'
vocabulary_dir = '/roaming/tcastrof/names/eacl/stats/voc.json'
evaluation_dir = '/roaming/tcastrof/names/eacl/evaluationV3'

# initialize vocabulary, dbpedia, entities, appositives and vocabulary
def init():
    print 'Initializing appositives...'
    appositives = json.load(open(appositives_dir))
    print 'Initializing entities_info...'
    entities_info = json.load(open(fentities))

    print 'Initializing titles...'
    titles = json.load(open(titles_dir))
    dbpedia = json.load(open(fdbpedia))
    print 'Initializing vocabulary...'
    vocabulary = json.load(open(vocabulary_dir))

    print 'Initializing dbpedia...'
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

    return entities_info, base, appositives, dbpedia, vocabulary

# filter 1 toke per discourse feature value for the vocabulary. Overcome lack of resourses
def filter_voc(entity, vocabulary):
    result = []

    count = {'np-subj':0, 'np-obj':0, 'subj-det':0, 'givenness_new':0, 'givenness_old':0, 'sentence-givenness_new':0, 'sentence-givenness_old':0}
    for e in vocabulary:
        if e != entity:
            _max = max(count.values())

            f = filter(lambda x: x['syntax'] == 'np-subj', vocabulary[e])[:(_max+1)-count['np-subj']]
            count['np-subj'] += len(f)
            result.extend(f)

            f = filter(lambda x: x['syntax'] == 'np-obj', vocabulary[e])[:(_max+1)-count['np-obj']]
            count['np-obj'] += len(f)
            result.extend(f)

            f = filter(lambda x: x['syntax'] == 'subj-det', vocabulary[e])[:(_max+1)-count['subj-det']]
            count['subj-det'] += len(f)
            result.extend(f)

            f = filter(lambda x: x['givenness'] == 'new', vocabulary[e])[:(_max+1)-count['givenness_new']]
            count['givenness_new'] += len(f)
            result.extend(f)

            f = filter(lambda x: x['givenness'] == 'old', vocabulary[e])[:(_max+1)-count['givenness_old']]
            count['givenness_old'] += len(f)
            result.extend(f)

            f = filter(lambda x: x['sentence-givenness'] == 'new', vocabulary[e])[:(_max+1)-count['sentence-givenness_new']]
            count['sentence-givenness_new'] += len(f)
            result.extend(f)

            f = filter(lambda x: x['sentence-givenness'] == 'old', vocabulary[e])[:(_max+1)-count['sentence-givenness_old']]
            count['sentence-givenness_old'] += len(f)
            result.extend(f)

    return result


def bayes_selection(mention, entity, model, k):
    features = {
        # 's_e': mention['label'],
        'discourse_se': mention['givenness'],
        'sentence_se': mention['sentence-givenness'],
        'syntax_se': mention['syntax']
    }

    if k != None:
        prob = model.select_content_backoff(features, entity, k)
    else:
        prob = model.select_content(features, entity)
    return prob

def bayes_realization(form, mention, entity, model, words, appositive):
    return model.realizeWithWords(form, entity, mention['syntax'], words, appositive)

# check the feature values already processed
def get_features_visited(mention, features):
    result = copy.copy(features)

    if ('givenness', mention['givenness']) not in result:
        result.append(('givenness', mention['givenness']))

    if ('sentence-givenness', mention['sentence-givenness']) not in result:
        result.append(('sentence-givenness', mention['sentence-givenness']))

    if ('syntax', mention['syntax']) not in result:
        result.append(('syntax', mention['syntax']))
    return result

def bayes_variation(references, form_distribution, test_set_same_features, entity, model, words, appositive, name):
    distribution = {}
    for form in form_distribution:
        distribution[form[0]] = len(references) * form[1]

    shuffle(references)
    for i, reference in enumerate(references):
        form = filter(lambda x: distribution[x] == max(distribution.values()), distribution.keys())[0]

        label = filter(lambda x: x[0] == form, form_distribution)[0]
        realizer = bayes_realization(form, test_set_same_features[i], entity, model, words, appositive)
        references[i][name] = { 'label': label, 'reference': realizer }

        distribution[form] -= 1
    return references

def process_entity(entity, words, mentions, vocabulary, dbpedia, appositive, fname):
    results = {}

    # Retrieve all the mentions to the entity
    # mentions = np.array(references[entity])

    # compute the set of features (vocabulary) from other entities
    print 'Filter general training set'
    general_voc = filter_voc(entity, vocabulary)

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

            tokens = prep.process_tokens(mention, parsed, entity, False)
            content_vocabulary.extend(tokens)
            realization_vocabulary.extend(tokens)

        # Consider data from other entities in the training set
        content_vocabulary.extend(general_voc)

        # initialize our official model
        clf = Bayes(content_vocabulary, realization_vocabulary, True)
        # initialize random baseline
        baseline_random = Random(dbpedia=dbpedia)
        # initialize Siddharthan baseline
        baseline1 = Siddharthan(dbpedia=dbpedia)
        # initialize Deemter baseline
        baseline2 = Deemter(dbpedia=dbpedia, parsed_dir=parsed_dir)


        features = []
        for mention in test_set:
            # Check if the set of features was processed already
            aux = get_features_visited(mention, features)
            if aux != features:
                features = copy.copy(aux)

                # Group proper name references from the test fold by feature values
                test_set_same_features = filter(lambda x: x['givenness'] == mention['givenness'] \
                                                          and x['sentence-givenness'] == mention['sentence-givenness'] \
                                                          and x['syntax'] == mention['syntax'], test_set)

                # Bayes model selection
                form_distribution = bayes_selection(mention, entity, clf, None)
                form_distribution_k0 = bayes_selection(mention, entity, clf, 0)
                form_distribution_k2 = bayes_selection(mention, entity, clf, 2)

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

                    # Siddharthan model
                    r = baseline1.run(entity, filtered_mention['givenness'], filtered_mention['syntax'])
                    result['siddharthan'] = { 'label': r[0], 'reference': r[1] }

                    # Deemter model
                    ms = json.load(open(os.path.join(mention_dir, filtered_mention['fname'])))[entity]
                    r = baseline2.run(entity, filtered_mention, ms, 3, filtered_mention['syntax'])
                    result['deemter'] = { 'label': r[0], 'reference': r[1] }

                    # Bayes model with no variation (Realization with the most likely referential form)
                    realizer = bayes_realization(form_distribution[0][0], filtered_mention, entity, clf, words, appositive)
                    result['bayes_no_variation'] = { 'label': form_distribution[0], 'reference': realizer }

                    # Bayes backoff model with no variation (Realization with the most likely referential form)
                    realizer = bayes_realization(form_distribution_k0[0][0], filtered_mention, entity, clf, words, appositive)
                    result['bayes_backoffk0_no_variation'] = { 'label': form_distribution_k0[0], 'reference': realizer }

                    # Bayes backoff model with no variation (Realization with the most likely referential form)
                    realizer = bayes_realization(form_distribution_k2[0][0], filtered_mention, entity, clf, words, appositive)
                    result['bayes_backoffk2_no_variation'] = { 'label': form_distribution_k2[0], 'reference': realizer }

                    # Bayes model with random choice of proper name form
                    index = randint(0, len(form_distribution)-1)
                    realizer = bayes_realization(form_distribution[index][0], filtered_mention, entity, clf, words, appositive)
                    result['bayes_random'] = { 'label': form_distribution[index], 'reference': realizer }

                    group_result.append(result)

                # Generate proper names with individual variation in the for choice
                group_result = bayes_variation(group_result, form_distribution, test_set_same_features, entity, clf, words, appositive, 'bayes_variation')
                group_result = bayes_variation(group_result, form_distribution_k0, test_set_same_features, entity, clf, words, appositive, 'bayes_backoffk0_variation')
                group_result = bayes_variation(group_result, form_distribution_k2, test_set_same_features, entity, clf, words, appositive, 'bayes_backoffk2_variation')
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
    entities_info, tested_words, appositives, dbpedia, vocabulary = init()

    # Sort entities and start the process
    entities = vocabulary.keys()
    entities.sort()

    print 'Number of entities: ', len(entities)
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
            process_entity(entity, words, np.array(references[entity]), vocabulary, dbpedia, appositive, entity_id)

if __name__ == '__main__':
    run()