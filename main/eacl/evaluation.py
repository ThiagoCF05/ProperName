__author__ = 'thiagocastroferreira'

import cPickle as p
import nltk
import numpy as np
import os

from nltk.metrics.distance import edit_distance, jaccard_distance
from sklearn.metrics import accuracy_score

if __name__ == '__main__':
    fentities = '/roaming/tcastrof/names/eacl/fentities.json'
    entities_dir = '/roaming/tcastrof/names/eacl/evaluationVariation'
    entities = os.listdir(entities_dir)

    results = {}

    _random, bayes_random, bayes_no_variation, bayes_variation, siddharthan, deemter  = {}, {}, {}, {}, {}, {}
    for _id in entities:
        results[_id] = {}

        evaluation = p.load(open(os.path.join(entities_dir, _id)))

        for fold in evaluation:
            results[_id][fold] = {}
            if fold not in bayes_random:
                _random[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
                bayes_random[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
                bayes_no_variation[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
                bayes_variation[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
                siddharthan[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
                deemter[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}

            for item in evaluation[fold]:
                string_real = item['real']['reference']
                string_random = item['random']['reference'][0]
                string_bayes_random = item['bayes_random']['reference'][0][0]
                string_bayes_no_variation = item['bayes_no_variation']['reference'][0][0]
                string_bayes_variation = item['bayes_variation']['reference'][0][0]
                string_siddharthan = item['siddharthan']['reference']
                string_deemter = item['deemter']['reference']

                dist_random = edit_distance(string_random, string_real)
                dist_bayes_random = edit_distance(string_bayes_random, string_real)
                dist_bayes_no_variation = edit_distance(string_bayes_no_variation, string_real)
                dist_bayes_variation = edit_distance(string_bayes_variation, string_real)
                dist_siddharthan = edit_distance(string_siddharthan, string_real)
                dist_deemter = edit_distance(string_deemter, string_real)

                tokens_real = set(nltk.word_tokenize(string_real))
                tokens_random = set(nltk.word_tokenize(string_random))
                tokens_bayes_random = set(nltk.word_tokenize(string_bayes_random))
                tokens_bayes_no_variation = set(nltk.word_tokenize(string_bayes_no_variation))
                tokens_bayes_variation = set(nltk.word_tokenize(string_bayes_variation))
                tokens_siddharthan = set(nltk.word_tokenize(string_siddharthan))
                tokens_deemter = set(nltk.word_tokenize(string_deemter))

                jaccard_random = jaccard_distance(tokens_random, tokens_real)
                jaccard_bayes_random = jaccard_distance(tokens_bayes_random, tokens_real)
                jaccard_bayes_no_variation = jaccard_distance(tokens_bayes_no_variation, tokens_real)
                jaccard_bayes_variation = jaccard_distance(tokens_bayes_variation, tokens_real)
                jaccard_siddharthan = jaccard_distance(tokens_siddharthan, tokens_real)
                jaccard_deemter = jaccard_distance(tokens_deemter, tokens_real)

                bayes_random[fold]['y_real'].append(item['real']['label'])
                bayes_random[fold]['y_pred'].append(item['bayes_random']['label'][0])
                bayes_random[fold]['string'].append(dist_bayes_random)
                bayes_random[fold]['jaccard'].append(jaccard_bayes_random)

                bayes_no_variation[fold]['y_real'].append(item['real']['label'])
                bayes_no_variation[fold]['y_pred'].append(item['bayes_no_variation']['label'][0])
                bayes_no_variation[fold]['string'].append(dist_bayes_no_variation)
                bayes_no_variation[fold]['jaccard'].append(jaccard_bayes_no_variation)

                bayes_variation[fold]['y_real'].append(item['real']['label'])
                bayes_variation[fold]['y_pred'].append(item['bayes_variation']['label'][0])
                bayes_variation[fold]['string'].append(dist_bayes_variation)
                bayes_variation[fold]['jaccard'].append(jaccard_bayes_variation)

                _random[fold]['y_real'].append(item['real']['label'])
                _random[fold]['y_pred'].append(item['random']['label'])
                _random[fold]['string'].append(dist_random)
                _random[fold]['jaccard'].append(jaccard_random)

                siddharthan[fold]['y_real'].append(item['real']['label'])
                siddharthan[fold]['y_pred'].append(item['siddharthan']['label'])
                siddharthan[fold]['string'].append(dist_siddharthan)
                siddharthan[fold]['jaccard'].append(jaccard_siddharthan)

                deemter[fold]['y_real'].append(item['real']['label'])
                deemter[fold]['y_pred'].append(item['deemter']['label'])
                deemter[fold]['string'].append(dist_deemter)
                deemter[fold]['jaccard'].append(jaccard_deemter)

                result = {
                    'bayes_random': {
                        'label': (item['real']['label'], item['bayes_random']['label'][0]),
                        'string': dist_bayes_random,
                        'jaccard': jaccard_bayes_random
                    },
                    'bayes_no_variation': {
                        'label': (item['real']['label'], item['bayes_no_variation']['label'][0]),
                        'string': dist_bayes_no_variation,
                        'jaccard': jaccard_bayes_no_variation
                    },
                    'bayes_variation': {
                        'label': (item['real']['label'], item['bayes_variation']['label'][0]),
                        'string': dist_bayes_variation,
                        'jaccard': jaccard_bayes_variation
                    },
                    'random': {
                        'label': (item['real']['label'], item['random']['label']),
                        'string': dist_random,
                        'jaccard': jaccard_random
                    },
                    'siddharthan': {
                        'label': (item['real']['label'], item['siddharthan']['label']),
                        'string': dist_siddharthan,
                        'jaccard': jaccard_siddharthan
                    },
                    'deemter': {
                        'label': (item['real']['label'], item['deemter']['label']),
                        'string': dist_deemter,
                        'jaccard': jaccard_deemter
                    }
                }

    general_random = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
    general_bayes_random = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
    general_bayes_no_variation = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
    general_bayes_variation = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
    general_siddharthan = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
    general_deemter = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}

    for fold in bayes_random:
        general_random['y_real'].extend(_random[fold]['y_real'])
        general_random['y_pred'].extend(_random[fold]['y_pred'])
        general_random['string'].extend(_random[fold]['string'])
        general_random['jaccard'].extend(_random[fold]['jaccard'])

        general_siddharthan['y_real'].extend(siddharthan[fold]['y_real'])
        general_siddharthan['y_pred'].extend(siddharthan[fold]['y_pred'])
        general_siddharthan['string'].extend(siddharthan[fold]['string'])
        general_siddharthan['jaccard'].extend(siddharthan[fold]['jaccard'])

        general_deemter['y_real'].extend(deemter[fold]['y_real'])
        general_deemter['y_pred'].extend(deemter[fold]['y_pred'])
        general_deemter['string'].extend(deemter[fold]['string'])
        general_deemter['jaccard'].extend(deemter[fold]['jaccard'])

        general_bayes_random['y_real'].extend(bayes_random[fold]['y_real'])
        general_bayes_random['y_pred'].extend(bayes_random[fold]['y_pred'])
        general_bayes_random['string'].extend(bayes_random[fold]['string'])
        general_bayes_random['jaccard'].extend(bayes_random[fold]['jaccard'])

        general_bayes_no_variation['y_real'].extend(bayes_no_variation[fold]['y_real'])
        general_bayes_no_variation['y_pred'].extend(bayes_no_variation[fold]['y_pred'])
        general_bayes_no_variation['string'].extend(bayes_no_variation[fold]['string'])
        general_bayes_no_variation['jaccard'].extend(bayes_no_variation[fold]['jaccard'])

        general_bayes_variation['y_real'].extend(bayes_variation[fold]['y_real'])
        general_bayes_variation['y_pred'].extend(bayes_variation[fold]['y_pred'])
        general_bayes_variation['string'].extend(bayes_variation[fold]['string'])
        general_bayes_variation['jaccard'].extend(bayes_variation[fold]['jaccard'])

        print 'Fold', fold
        print 'Labels: '
        print 'Random: ', accuracy_score(_random[fold]['y_real'], _random[fold]['y_pred'])
        print 'Siddharthan: ', accuracy_score(siddharthan[fold]['y_real'], siddharthan[fold]['y_pred'])
        print 'Deemter: ', accuracy_score(deemter[fold]['y_real'], deemter[fold]['y_pred'])
        print 'Bayes Random: ', accuracy_score(bayes_random[fold]['y_real'], bayes_random[fold]['y_pred'])
        print 'Bayes No Variation: ', accuracy_score(bayes_no_variation[fold]['y_real'], bayes_no_variation[fold]['y_pred'])
        print 'Bayes Variation: ', accuracy_score(bayes_variation[fold]['y_real'], bayes_variation[fold]['y_pred'])
        print 20 * '-'
        print 'String Distance: '
        print 'Random: ', np.mean(_random[fold]['string'])
        print 'Siddharthan: ', np.mean(siddharthan[fold]['string'])
        print 'Deemter: ', np.mean(deemter[fold]['string'])
        print 'Bayes Random: ', np.mean(bayes_random[fold]['string'])
        print 'Bayes No Variation: ', accuracy_score(bayes_no_variation[fold]['y_real'], bayes_no_variation[fold]['y_pred'])
        print 'Bayes Variation: ', accuracy_score(bayes_variation[fold]['y_real'], bayes_variation[fold]['y_pred'])
        print 20 * '-'
        print 'Jaccard Distance: '
        print 'Random: ', np.mean(_random[fold]['jaccard'])
        print 'Siddharthan: ', np.mean(siddharthan[fold]['jaccard'])
        print 'Deemter: ', np.mean(deemter[fold]['jaccard'])
        print 'Bayes Random: ', np.mean(bayes_random[fold]['jaccard'])
        print 'Bayes No Variation: ', accuracy_score(bayes_no_variation[fold]['y_real'], bayes_no_variation[fold]['y_pred'])
        print 'Bayes Variation: ', accuracy_score(bayes_variation[fold]['y_real'], bayes_variation[fold]['y_pred'])
        print 20 * '-'
        print '\n'

    print 'GENERAL'
    print 'Labels: '
    print 'Random: ', accuracy_score(general_random['y_real'], general_random['y_pred'])
    print 'Siddharthan: ', accuracy_score(general_siddharthan['y_real'], general_siddharthan['y_pred'])
    print 'Deemter: ', accuracy_score(general_deemter['y_real'], general_deemter['y_pred'])
    print 'Bayes Random: ', accuracy_score(general_bayes_random['y_real'], general_bayes_random['y_pred'])
    print 'Bayes No Variation: ', accuracy_score(general_bayes_no_variation['y_real'], general_bayes_no_variation['y_pred'])
    print 'Bayes Variation: ', accuracy_score(general_bayes_variation['y_real'], general_bayes_variation['y_pred'])
    print 20 * '-'
    print 'String Distance: '
    print 'Random: ', np.mean(general_random['string'])
    print 'Siddharthan: ', np.mean(general_siddharthan['string'])
    print 'Deemter: ', np.mean(general_deemter['string'])
    print 'Bayes Random: ', np.mean(general_bayes_random['string'])
    print 'Bayes No Variation: ', np.mean(general_bayes_no_variation['string'])
    print 'Bayes Variation: ', np.mean(general_bayes_variation['string'])
    print 20 * '-'
    print 'Jaccard Distance: '
    print 'Random: ', np.mean(general_random['jaccard'])
    print 'Siddharthan: ', np.mean(general_siddharthan['jaccard'])
    print 'Deemter: ', np.mean(general_deemter['jaccard'])
    print 'Bayes Random: ', np.mean(general_bayes_random['jaccard'])
    print 'Bayes No Variation: ', np.mean(general_bayes_no_variation['jaccard'])
    print 'Bayes Variation: ', np.mean(general_bayes_variation['jaccard'])
    print 20 * '-'
    print '\n'