__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 05/2016
Description:
    This script aims to extract the mentions from the selected texts from Wikilinks
"""

import os
import sys
sys.path.append('../')
import properties
import traceback
import json

from corpus_builder import get_mentions

if __name__ == '__main__':
    # root_dir = '/roaming/tcastrof/names/eacl'
    # parsed_dir = "/roaming/tcastrof/names/parsed"
    # mentions_dir = "/roaming/tcastrof/names/eacl/mentions"

    # urls, entities = loader.run(os.path.join(root_dir, 'furls.json'), os.path.join(root_dir, 'fdbpedia.json'))
    urls = json.load(open(properties.file_urls))
    entities = json.load(open(properties.file_dbpedia))

    nfiles = 0
    notfound = 0
    for entity in urls.keys():
        dbpedia = entities[entity]

        for url in urls[entity]:
            nfiles += 1
            if nfiles % 100 == 0:
                print nfiles, "processed / ", notfound, 'not found'

            try:
                mentions = get_mentions.run(os.path.join(properties.parsed_dir, url['id']), dbpedia)

                if os.path.isfile(os.path.join(properties.mentions_dir, url['id'])):
                    j = json.load(open(os.path.join(properties.mentions_dir, url['id'])))
                    j[entity] = mentions
                else:
                    j = { entity:mentions }
                json.dump(j, open(os.path.join(properties.mentions_dir, url['id']), 'w'), indent=4, separators=(',', ': '))
            except ValueError:
                nfiles -= 1
                notfound += 1
            except IOError:
                nfiles -= 1
                notfound += 1
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)