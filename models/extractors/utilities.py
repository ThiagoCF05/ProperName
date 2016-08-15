__author__ = 'thiagocastroferreira'

import json
import os

# initialize features
giveness2id = {'new':0, 'old':1}
syntax2id = {'np-subj':0, 'np-obj':1, 'subj-det':2}
binary2id = {False:0, True:1}

def load_mentions(fname):
    return json.load(open(fname))

def extract_features(mentions, text_id):
    Xs, ys = [], []
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
        Xs.append(X)
        ys.append(y)
    return Xs, ys

# Save a json with all the information parsed
def write(features = [], classes = [], text2id = [], fname = ''):
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
    json.dump(j, open(fname, 'w'))

# Get references mapped by entity and file
def get_references(furls, fdir):
    # load urls.txt document
    with open(furls) as f:
        urls = f.read()
        urls = map(lambda x: x.split('\n'), urls.split('\n\n'))
        urls = dict(map(lambda x: (x[0], map(lambda y: y.split('\t'),x[1:])), urls))

    references = {}
    for e in urls.keys():
        references[e] = {}
        for url in urls[e]:
            try:
                print url[0], '\r',
                mentions = json.load(open(os.path.join(fdir, url[0])))
                if url[0] not in references[e]:
                    references[e][url[0]] = []
                references[e][url[0]].extend(mentions[e])
            except:
                pass
    return references