__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 13/09/2016
Description:
    This script aims to create retrieve all possible titles for each entity
"""
import json
import os

# get all the titles possible for an entity
def get_titles(mention_dir, write_dir):
    files = os.listdir(mention_dir)

    result = {}
    for i, fname in enumerate(files):
        print i, fname, '\r',
        mentions = json.load(open(os.path.join(mention_dir, fname)))

        for entity in mentions:
            if entity not in result:
                result[entity] = []
            for mention in filter(lambda mention: mention['type'] == 'PROPER', mentions[entity]):
                titles = map(lambda title: title.split()[0].strip(), mention['titles'])
                result[entity].extend(titles)

    for entity in result:
        result[entity] = list(set(result[entity]))

    json.dump(result, open(write_dir, 'w'), indent=4, separators=(',', ': '))

if __name__ == '__main__':
    mention_dir = '/roaming/tcastrof/names/eacl/mentions'
    write_dir = '/roaming/tcastrof/names/eacl/titles.json'

    get_titles(mention_dir, write_dir)