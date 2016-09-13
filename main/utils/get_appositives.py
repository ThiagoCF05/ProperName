__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 13/09/2016
Description:
    This script aims to get the descriptions from each entity in their wikidata page. These descriptions will be used as
    appositives.
"""

import json
import urllib
import urllib2

def get_appositive(entity):
    entity = entity['url'].split('/')[-1].replace('_', ' ')

    url = 'https://www.wikidata.org/w/api.php'
    values = {'action' : 'wbsearchentities',
              'format' : 'json',
              'language' : 'en',
              'search' : entity}

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    page = json.loads(response.read())

    if len(page['search']) > 0:
        return page['search'][0]['description']
    else:
        return ''

def run(entity_dir, write_dir):
    appositives = {}
    entities = json.load(open(entity_dir))

    for entity in entities:
        appositives[entities] = get_appositive(entity)

    json.dump(appositives, open(write_dir, 'w'), indent=4, separators=(',', ': '))
    return appositives

if __name__ == '__main__':
    entity_dir = '/roaming/tcastrof/names/eacl/fentities.json'
    write_dir = '/roaming/tcastrof/names/eacl/appositives.json'

    run(entity_dir, write_dir)