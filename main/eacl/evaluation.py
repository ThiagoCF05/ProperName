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

    bayes_random, bayes_no_variation, bayes_variation, siddharthan, deemter  = {}, {}, {}, {}, {}
    for _id in entities:
        results[_id] = {}

        evaluation = p.load(open(os.path.join(entities_dir, _id)))

        for fold in evaluation:
            results[_id][fold] = {}
            if fold not in bayes_random:
                bayes_random[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
                bayes_no_variation[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
                bayes_variation[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
                siddharthan[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
                deemter[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}

            for item in evaluation[fold]:
                string_real = item['real']['reference']
                string_bayes_random = item['bayes_random']['reference'][0][0]
                string_bayes_no_variation = item['bayes_no_variation']['reference'][0][0]
                string_bayes_variation = item['bayes_variation']['reference'][0][0]
                string_siddharthan = item['siddharthan']['reference']
                string_deemter = item['deemter']['reference']

                dist_bayes_random = edit_distance(string_bayes_random, string_real)
                dist_bayes_no_variation = edit_distance(string_bayes_no_variation, string_real)
                dist_bayes_variation = edit_distance(string_bayes_variation, string_real)
                dist_siddharthan = edit_distance(string_siddharthan, string_real)
                dist_deemter = edit_distance(string_deemter, string_real)

                tokens_real = set(nltk.word_tokenize(string_real))
                tokens_bayes_random = set(nltk.word_tokenize(string_bayes_random))
                tokens_bayes_no_variation = set(nltk.word_tokenize(string_bayes_no_variation))
                tokens_bayes_variation = set(nltk.word_tokenize(string_bayes_variation))
                tokens_siddharthan = set(nltk.word_tokenize(string_siddharthan))
                tokens_deemter = set(nltk.word_tokenize(string_deemter))

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
                        'label': (item['real']['label'], item['bayes']['label'][0]),
                        'string': dist_bayes,
                        'jaccard': jaccard_bayes
                    },
                    'bayes_no_variation': {
                        'label': (item['real']['label'], item['bayes']['label'][0]),
                        'string': dist_bayes,
                        'jaccard': jaccard_bayes
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

    general_bayes = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
    general_siddharthan = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
    general_deemter = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}

    for fold in bayes:
        general_siddharthan['y_real'].extend(siddharthan[fold]['y_real'])
        general_siddharthan['y_pred'].extend(siddharthan[fold]['y_pred'])
        general_siddharthan['string'].extend(siddharthan[fold]['string'])
        general_siddharthan['jaccard'].extend(siddharthan[fold]['jaccard'])

        general_deemter['y_real'].extend(deemter[fold]['y_real'])
        general_deemter['y_pred'].extend(deemter[fold]['y_pred'])
        general_deemter['string'].extend(deemter[fold]['string'])
        general_deemter['jaccard'].extend(deemter[fold]['jaccard'])

        general_bayes['y_real'].extend(bayes[fold]['y_real'])
        general_bayes['y_pred'].extend(bayes[fold]['y_pred'])
        general_bayes['string'].extend(bayes[fold]['string'])
        general_bayes['jaccard'].extend(bayes[fold]['jaccard'])

        print 'Fold', fold
        print 'Labels: '
        print 'Siddharthan: ', accuracy_score(siddharthan[fold]['y_real'], siddharthan[fold]['y_pred'])
        print 'Deemter: ', accuracy_score(deemter[fold]['y_real'], deemter[fold]['y_pred'])
        print 'Bayes: ', accuracy_score(bayes[fold]['y_real'], bayes[fold]['y_pred'])
        print 20 * '-'
        print 'String Distance: '
        print 'Siddharthan: ', np.mean(siddharthan[fold]['string'])
        print 'Deemter: ', np.mean(deemter[fold]['string'])
        print 'Bayes: ', np.mean(bayes[fold]['string'])
        print 20 * '-'
        print 'Jaccard Distance: '
        print 'Siddharthan: ', np.mean(siddharthan[fold]['jaccard'])
        print 'Deemter: ', np.mean(deemter[fold]['jaccard'])
        print 'Bayes: ', np.mean(bayes[fold]['jaccard'])
        print 20 * '-'
        print '\n'

    print 'GENERAL'
    print 'Labels: '
    print 'Siddharthan: ', accuracy_score(general_siddharthan['y_real'], general_siddharthan['y_pred'])
    print 'Deemter: ', accuracy_score(general_deemter['y_real'], general_deemter['y_pred'])
    print 'Bayes: ', accuracy_score(general_bayes['y_real'], general_bayes['y_pred'])
    print 20 * '-'
    print 'String Distance: '
    print 'Siddharthan: ', np.mean(general_siddharthan['string'])
    print 'Deemter: ', np.mean(general_deemter['string'])
    print 'Bayes: ', np.mean(general_bayes['string'])
    print 20 * '-'
    print 'Jaccard Distance: '
    print 'Siddharthan: ', np.mean(general_siddharthan['jaccard'])
    print 'Deemter: ', np.mean(general_deemter['jaccard'])
    print 'Bayes: ', np.mean(general_bayes['jaccard'])
    print 20 * '-'
    print '\n'