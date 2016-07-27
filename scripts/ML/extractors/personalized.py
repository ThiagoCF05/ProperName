__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 15/07/2016
Description:
    This script aims to prepare a file with features and classes by entity for machine learning.
"""

import os
import json
import utilities

fdir = '/roaming/tcastrof/names/regnames/mentions'
fwrite = '/home/tcastrof/names/classifiers/features/personal'
furls = '/roaming/tcastrof/names/regnames/urls.txt'

# parse features
def parse():
    references = utilities.get_references(furls, fdir)
    results = {}
    entity2id = {}
    _id = 0
    for entity in references:
        results[entity] = { 'X':[], 'y':[] }
        text2id = []
        _id = _id + 1
        entity2id[entity] = _id
        for fname in references[entity]:
            features, classes = utilities.extract_features(references[entity][fname], int(fname))
            text2id.append((fname, int(fname)))
            results[entity]['X'].extend(features)
            results[entity]['y'].extend(classes)
        utilities.write(results[entity]['X'], results[entity]['y'], text2id, os.path.join(fwrite, str(_id)))

    json.dump(entity2id, open('../features/entity2id.json', 'w'))

if __name__ == '__main__':
    parse()