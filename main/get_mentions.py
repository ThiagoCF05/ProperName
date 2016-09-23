__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 20/09/2016
Description:
    Method for preparing the trial to the extrinsic evaluation
"""

import os
import sys
import traceback
import json
import utilities

from corpus_builder import get_mentions

parsed_dir = "/roaming/tcastrof/names/eacl/evaluation/extrinsic/parsed"
mentions_dir = "/roaming/tcastrof/names/eacl/evaluation/extrinsic/mentions"
m_dir = '/roaming/tcastrof/names/eacl/mentions'

# filter entities with more than N mentions and process the mentions
def filter_entities(N_min, N_max, mention_dir):
    '''
    :param N: only entities with more than N mentions should be considered
    :param mention_dir: directory where the mention files are present
    :return:
    '''
    result = {}

    files = os.listdir(mention_dir)
    for i, fname in enumerate(files):
        print i, fname, '\r',
        mentions = json.load(open(os.path.join(mention_dir, fname)))

        # Exclude this entity from the set
        entities = filter(lambda x: x != 'http://en.wikipedia.org/wiki/Whoopi_Goldberg', mentions)
        for entity in entities:
            if entity not in result:
                result[entity] = []
            for mention in filter(lambda mention: mention['type'] == 'PROPER', mentions[entity]):
                mention['fname'] = fname
                result[entity].append(mention)
    if N_max == 0:
        return dict(map(lambda x: (x, result[x]), filter(lambda e: len(result[e]) >= N_min, result.keys())))
    else:
        return dict(map(lambda x: (x, result[x]), filter(lambda e: N_min <= len(result[e]) <= N_max, result.keys())))

if __name__ == '__main__':
    dbpedia = json.load(open(utilities.dbpedia_dir))
    entities = json.load(open(utilities.entities_dir))

    fentities = filter_entities(50, 0, m_dir)

    if not os.path.exists(mentions_dir):
        os.makedirs(mentions_dir)

    nfiles = 0
    notfound = 0
    for i, e in enumerate(fentities):
        print i, e
        # try:
        entity = filter(lambda x: x['url'] == e, entities)[0]
        mentions = get_mentions.run(os.path.join(parsed_dir, entity['id']), dbpedia[entity['url']])

        if os.path.isfile(os.path.join(mentions_dir, entity['id'])):
            j = json.load(open(os.path.join(mentions_dir, entity['id'])))
            j[entity['url']] = mentions
        else:
            j = { entity['url']:mentions }
        json.dump(j, open(os.path.join(mentions_dir, entity['id']), 'w'), indent=4, separators=(',', ': '))
        # except ValueError:
        #     nfiles -= 1
        #     notfound += 1
        # except IOError:
        #     nfiles -= 1
        #     notfound += 1
        # except:
        #     exc_type, exc_value, exc_traceback = sys.exc_info()
        #     traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)