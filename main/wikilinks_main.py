from main import utils as kb

__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 05/2016
Description:
    This script aims to extract the mentions from the selected texts from Wikilinks
"""

import os
import sys
import traceback
import json

if __name__ == '__main__':
    root_dir = '/roaming/tcastrof/names/eacl'
    parsed_dir = "/roaming/tcastrof/names/parsed"
    mentions_dir = "/roaming/tcastrof/names/eacl/mentions"

    # urls, entities = loader.run(os.path.join(root_dir, 'furls.json'), os.path.join(root_dir, 'fdbpedia.json'))
    urls = json.load(open(os.path.join(root_dir, 'furls.json')))
    entities = json.load(open(os.path.join(root_dir, 'fdbpedia.json')))

    nfiles = 0
    notfound = 0
    for entity in urls.keys():
        dbpedia = kb.update(entities[entity])

        for url in urls[entity]:
            nfiles += 1
            if nfiles % 100 == 0:
                print nfiles, "processed / ", notfound, 'not found'

            try:
                mentions = get_mentions.run(os.path.join(parsed_dir, url['id']), dbpedia)

                if os.path.isfile(os.path.join(mentions_dir, url['id'])):
                    j = json.load(open(os.path.join(mentions_dir, url['id'])))
                    j[entity] = mentions
                else:
                    j = { entity:mentions }
                json.dump(j, open(os.path.join(mentions_dir, url['id']), 'w'), separators=(',',':'))
            except ValueError:
                nfiles -= 1
                notfound += 1
            except IOError:
                nfiles -= 1
                notfound += 1
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)

    # root_dir = 'data/test'
    # urls, entities = loader.run(os.path.join(root_dir, 'urls-top50-new.txt'), os.path.join(root_dir, 'dbpedia.txt'))
    # dbpedia = update(entities['http://en.wikipedia.org/wiki/Francisco_Franco'])
    # try:
    #     mentions = get_mentions.run(os.path.join(root_dir, '5072656.json'), dbpedia)
    #     if os.path.isfile(os.path.join(root_dir, '5072656.json')):
    #         j = json.load(open('5072656.json'))
    #         j['aaa'] = mentions
    #     else:
    #         j = { 'aaa':mentions }
    #         json.dump(j, open('5072656.json', 'w'), separators=(',',':'))
    # except Exception,e:
    #     print str(e)