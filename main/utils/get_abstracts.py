__author__ = 'thiagocastroferreira'

import json
import urllib2

entities_dir = '/roaming/tcastrof/names/eacl/entities.json'
write_dir = '/roaming/tcastrof/names/eacl/abstracts.json'

dbpedia_url = 'http://dbpedia.org/data/'
resource_url = 'http://dbpedia.org/resource/'

def get_abstract(entity):
    print entity['url'], '\r',
    tag = entity['url'].split('/')[-1]

    url = dbpedia_url + tag + '.json'
    response = urllib2.urlopen(url)
    page = json.loads(response.read())

    resource = resource_url + entity

    abstracts = page[resource]['http://dbpedia.org/ontology/abstract']

    abstract = filter(lambda x: x['lang'] == 'en', abstracts)[0]['value']
    return (entity['url'], abstract)

if __name__ == '__main__':
    entities = json.load(open(entities_dir))
    abstracts = []

    for entity in entities:
        abstracts.append(get_abstract(entity))

    json.dump(dict(abstracts), open(write_dir, 'w'), indent=4, separators=(',', ': '))