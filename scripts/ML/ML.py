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
    # initialize features
    giveness2id = {'new':0, 'old':1}
    syntax2id = {'np-subj':0, 'np-obj':1, 'subj-det':2}
    binary2id = {False:0, True:1}
    text2id = []

    # prepare features and classes for machine learning
    fdir = '/roaming/tcastrof/names/mentions'
    fnames = os.listdir(fdir)

    features, classes = [], []
    text_id = 0
    for fname in fnames:
        print fname, '\r',
        mentions = json.load(open(os.path.join(fdir, fname)))
        text_id = text_id + 1
        text2id.append((fname, text_id))
        for mention in filter(lambda mention: mention['type'] == 'PROPER', mentions):
            X = [
                text_id,
                giveness2id[mention['givenness']],
                giveness2id[mention['sentence-givenness']],
                syntax2id[mention['syntax']],
                mention['sentNum'],
                mention['startIndex']
            ]

            y = [
                binary2id[mention['has_title']],
                binary2id[mention['has_firstName']],
                binary2id[mention['has_middleName']],
                binary2id[mention['has_lastName']],
                binary2id[mention['has_appositive']]
            ]

            features.append(X)
            classes.append(y)

    # Save a json with all the information parsed
    idxfeature = ['text_id', 'givenness', 'sentence-givenness', 'syntax', 'sentNum', 'startIndex']
    idxclasses = ['has_title', 'has_firstName', 'has_middleName', 'has_lastName', 'has_appositive']

    j = {
        'text2id':dict(text2id),
        'giveness2id':giveness2id,
        'syntax2id':syntax2id,
        'binary2id':binary2id,
        'idxfeature':idxfeature,'features':features,
        'idxclasses':idxclasses, 'classes':classes
    }
    json.dump(j, open('ML.json', 'w'))