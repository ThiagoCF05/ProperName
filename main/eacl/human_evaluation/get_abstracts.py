__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 20/09/2016
Description:
    This script aims to get the abstracts from each entity in their DBpedia page.
"""

import json
import os
import urllib2

abstracts_dir = '/roaming/tcastrof/names/eacl/evaluation/extrinsic/abstracts'
entities_dir = '/roaming/tcastrof/names/eacl/entities.json'
mention_dir = '/roaming/tcastrof/names/eacl/mentions'
write_dir = '/roaming/tcastrof/names/eacl/abstracts.json'

dbpedia_url = 'http://dbpedia.org/data/'
resource_url = 'http://dbpedia.org/resource/'

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

def get_abstract(entity):
    print entity['url'], '\r',
    tag = entity['url'].split('/')[-1]

    url = dbpedia_url + tag + '.json'
    response = urllib2.urlopen(url)
    page = json.loads(response.read())

    resource = resource_url + tag

    try:
        abstracts = page[resource]['http://dbpedia.org/ontology/abstract']
        abstract = filter(lambda x: x['lang'] == 'en', abstracts)[0]['value']
    except:
        abstract = ''
    return (entity['url'], abstract)

if __name__ == '__main__':
    entities = json.load(open(entities_dir))
    abstracts = []

    fentities = filter_entities(50, mention_dir)

    for e in fentities:
        entity = filter(lambda x: x['url'] == e, entities)
        url, abstract = get_abstract(entity)
        abstracts.append((url, abstract))

        with open(os.path.join(abstracts_dir, entity['id']), 'w') as f:
            f.write(abstract.encode('utf-8'))

    json.dump(dict(abstracts), open(write_dir, 'w'), indent=4, separators=(',', ': '))