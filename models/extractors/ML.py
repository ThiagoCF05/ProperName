from ML.extractors import utilities

__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 04/07/2016
Description:
    This script aims to prepare a file with features and classes for machine learning.
"""

import json
import os

if __name__ == '__main__':
    # prepare features and classes for machine learning
    fdir = '/roaming/tcastrof/names/regnames/mentions'
    fnames = os.listdir(fdir)
    text2id = []

    features, classes = [], []
    text_id = 0
    for fname in fnames:
        print fname, '\r',
        text_id = text_id + 1
        text2id.append((fname, text_id))

        references = json.load(open(os.path.join(fdir, fname)))
        for entity in references:
            X, y = utilities.extract_features(references[entity], text_id)
            features.extend(X)
            classes.extend(y)

    utilities.write(features, classes, text2id, '../features/feat.json')