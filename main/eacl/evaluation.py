__author__ = 'thiagocastroferreira'

import cPickle as p
import nltk
import numpy as np
import os

from nltk.metrics.distance import edit_distance, jaccard_distance
from sklearn.metrics import accuracy_score

if __name__ == '__main__':
    fentities = '/roaming/tcastrof/names/eacl/fentities.json'
    entities_dir = '/roaming/tcastrof/names/eacl/evaluation'
    entities = os.listdir(entities_dir)

    results = {}

    bayes, siddharthan, deemter  = {}, {}, {}
    for _id in entities:
        results[_id] = {}

        evaluation = p.load(open(os.path.join(entities_dir, _id)))

        for fold in evaluation:
            results[_id][fold] = {}
            if fold not in bayes:
                bayes[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
                siddharthan[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
                deemter[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}

            for item in evaluation[fold]:
                string_real = item['real']['reference']
                string_bayes = item['bayes']['reference'][0][0]
                string_siddharthan = item['siddharthan']['reference']
                string_deemter = item['deemter']['reference']

                dist_bayes = edit_distance(string_bayes, string_real)
                dist_siddharthan = edit_distance(string_siddharthan, string_real)
                dist_deemter = edit_distance(string_deemter, string_real)

                tokens_real = set(nltk.word_tokenize(string_real))
                tokens_bayes = set(nltk.word_tokenize(string_bayes))
                tokens_siddharthan = set(nltk.word_tokenize(string_siddharthan))
                tokens_deemter = set(nltk.word_tokenize(string_deemter))

                jaccard_bayes = jaccard_distance(tokens_bayes, tokens_real)
                jaccard_siddharthan = jaccard_distance(tokens_siddharthan, tokens_real)
                jaccard_deemter = jaccard_distance(tokens_deemter, tokens_real)

                bayes[fold]['y_real'].append(item['real']['label'])
                bayes[fold]['y_pred'].append(item['bayes']['label'][0])
                bayes[fold]['string'].append(dist_bayes)
                bayes[fold]['jaccard'].append(jaccard_bayes)

                siddharthan[fold]['y_real'].append(item['real']['label'])
                siddharthan[fold]['y_pred'].append(item['siddharthan']['label'][0])
                siddharthan[fold]['string'].append(dist_siddharthan)
                siddharthan[fold]['jaccard'].append(jaccard_siddharthan)

                deemter[fold]['y_real'].append(item['real']['label'])
                deemter[fold]['y_pred'].append(item['deemter']['label'][0])
                deemter[fold]['string'].append(dist_deemter)
                deemter[fold]['jaccard'].append(jaccard_deemter)

                result = {
                    'bayes': {
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
    for fold in bayes:
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