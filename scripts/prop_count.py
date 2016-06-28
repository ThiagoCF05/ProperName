__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 27/06/2016
Description:
    This script aims to compute the frequency of ontology properties in more than 100,000 entities.
"""

import json
import os
import urllib2
import cPickle as pickle

def get_entities(fname):
    f = open(fname)
    doc = f.read()
    f.close()

    return map(lambda x: x.split('\n')[0].split('/')[-1], doc.split('\n\n\n')[:-1])

def calc_properties(entity, fields):
    url = os.path.join('http://dbpedia.org/data', entity + '.json')
    response = urllib2.urlopen(url)
    js = json.loads(response.read())
    response.close()


    db = os.path.join('http://dbpedia.org/resource', entity)
    js = js[db]
    for p in filter(lambda x: 'ontology' in x or 'property' in x, js.keys()):
        if p not in fields.keys():
            fields[p] = 0
        fields[p] += 1
    return fields

if __name__ == '__main__':
    _dir = '/roaming/tcastrof/names/entities'
    files = os.listdir(_dir)

    print 'Retrieving entities...'
    entities = []
    for f in files:
        entities.extend(get_entities(os.path.join(_dir, f)))

    print 'Calculating frequencies...'
    fields = {}
    for entity in entities:
        print entity, '                                                \r',
        try:
            fields = calc_properties(entity, fields)
        except:
            pass

    pickle.dump(fields, open('properties', 'w'))