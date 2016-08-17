__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 15/08/2016
Description:
    Main method EACL 2017 model
"""

import json
import numpy as np
import operator
import os
import preprocessing

from Bayes import Bayes
from sklearn.cross_validation import KFold

def run():
    # filter entities and their references (more than 49 references)
    mention_dir = '/roaming/tcastrof/names/eacl/mentions'
    parsed_dir = '/roaming/tcastrof/names/regnames/parsed'

    label_results = []
    references = preprocessing.filter_entities(49, mention_dir)

    for entity in references:
        # Retrieve all the mentions to the entity
        mentions = np.array(references[entity])

        # compute cross validation
        kf = KFold(mentions.shape[0], n_folds=10)
        for train, test in kf:
            train_set, test_set = mentions[train], mentions[test]

            vocabulary = []
            for mention in train_set:
                parsed = json.load(open(os.path.join(parsed_dir, mention['fname'])))
                vocabulary.extend(preprocessing.process_tokens(mention, parsed, entity, False))

            clf = Bayes(vocabulary, True)
            for mention in test_set:
                features = {
                    # 's_e': mention['label'],
                    'discourse_se': mention['givenness'],
                    'sentence_se': mention['sentence-givenness'],
                    'syntax_se': mention['syntax']
                }

                print mention['label']
                print entity, mention['givenness'], mention['sentence-givenness'], mention['syntax']
                prob = clf.select_content(features, entity)
                prob = sorted(prob.items(), key=operator.itemgetter(1))
                prob.reverse()
                print prob[:3]
                print 10 * '-'

                result = {
                    'R': mention['label'],
                    'P': prob,
                    'giveness': mention['givenness'],
                    'sentence-givenness': mention['sentence-givenness'],
                    'syntax': mention['syntax'],
                    'entity': entity
                }
                label_results.append(result)

                print clf.realize(prob[0][0], entity)
    # json.dump(label_results, open('results.json', 'w'))

if __name__ == '__main__':
    run()