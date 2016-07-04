__author__ = 'thiagocastroferreira'

import os
import sys
import traceback
import json

import utils.get_mentions as get_mentions
import utils.loader as loader

def update(dbpedia):
    # del dbpedia['aliases']

    dbpedia['first_names'] = []
    dbpedia['middle_names'] = []
    dbpedia['last_names'] = []

    # select the given names in the citation format (Einstein, Albert)
    givenNames = filter(lambda given: ',' not in given, dbpedia['givenNames'])

    # select the shortest given name
    sizes = map(lambda given: len(given.split()), givenNames)
    if len(sizes) > 0:
        min_size = min(sizes)
        givenName = filter(lambda given: len(given.split()) == min_size, givenNames)[0]

        names = givenName.split()

        if len(names[0]) > 2:
            dbpedia['first_names'].append(names[0])
        for middle in names[1:]:
            if len(middle) > 2:
                dbpedia['middle_names'].append(middle)

    for birthName in dbpedia['birthNames']:
        names = birthName.split()

        if len(names[0]) > 2:
            dbpedia['first_names'].append(names[0])
        if len(names[-1]) > 2:
            dbpedia['last_names'].append(names[-1])
        names.remove(names[-1])
        for middle in names[1:]:
            if len(middle) > 2:
                dbpedia['middle_names'].append(middle)

    name = filter(lambda x: ',' not in x, dbpedia['foaf_names'])
    if len(name) > 0:
        names = name[0].split()

        if len(names[0]) > 2:
            dbpedia['first_names'].append(names[0])
        if len(names[-1]) > 2:
            dbpedia['last_names'].append(names[-1])
        names.remove(names[-1])
        for middle in names[1:]:
            if len(middle) > 2:
                dbpedia['middle_names'].append(middle)
    dbpedia['last_names'].extend(dbpedia['surnames'])

    dbpedia['first_names'] = list(set(dbpedia['first_names']))
    dbpedia['middle_names'] = list(set(dbpedia['middle_names']))
    dbpedia['last_names'] = list(set(dbpedia['last_names']))
    return dbpedia

if __name__ == '__main__':
    root_dir = '/roaming/tcastrof/names'
    parsed_dir = "/roaming/tcastrof/names/parsed"
    mentions_dir = "/roaming/tcastrof/names/mentions"

    urls, entities = loader.run(os.path.join(root_dir, 'urls-top50-new.txt'), os.path.join(root_dir, 'dbpedia.txt'))

    nfiles = 0
    notfound = 0
    for entity in urls.keys():
        dbpedia = update(entities[entity])

        for url in urls[entity]:
            nfiles += 1
            if nfiles % 100 == 0:
                print nfiles, "processed / ", notfound, 'not found'

            try:
                mentions = get_mentions.run(os.path.join(parsed_dir, url[0]), dbpedia)
                json.dump(mentions, open(os.path.join(mentions_dir, url[0]), 'w'), separators=(',',':'))
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
    #
    # try:
    #     mentions = get_mentions.run(os.path.join(root_dir, '5072656.json'), dbpedia)
    # except:
    #     pass