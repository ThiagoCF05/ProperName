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

if __name__ == '__main__':
    dbpedia = json.load(open(utilities.dbpedia_dir))
    entities = json.load(open(utilities.entities_dir))

    if not os.path.exists(mentions_dir):
        os.makedirs(mentions_dir)

    nfiles = 0
    notfound = 0
    for entity in entities:
        # try:
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