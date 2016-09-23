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

entities_dir = '/roaming/tcastrof/names/eacl/entities.json'
abstracts_dir = '/roaming/tcastrof/names/eacl/evaluation/extrinsic/abstracts'
write_dir = '/roaming/tcastrof/names/eacl/abstracts.json'

dbpedia_url = 'http://dbpedia.org/data/'
resource_url = 'http://dbpedia.org/resource/'

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

    for entity in entities:
        url, abstract = get_abstract(entity)
        abstracts.append((url, abstract))

        with open(os.path.join(abstracts_dir, entity['id']), 'w') as f:
            f.write(abstract)

    json.dump(dict(abstracts), open(write_dir, 'w'), indent=4, separators=(',', ': '))