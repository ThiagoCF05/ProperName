__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 15/08/2016
Description:
    Main method EACL 2017 model
"""

import json
import numpy as np
import os
import preprocessing

from Bayes import Bayes
from sklearn.cross_validation import KFold

def run():
    # filter entities and their references (more than 49 references)
    mention_dir = '/roaming/tcastrof/names/eacl/mentions'
    parsed_dir = '/roaming/tcastrof/names/regnames/parsed'

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
                print clf.select_content(features, entity)
                print 10 * '-'

if __name__ == '__main__':
    run()