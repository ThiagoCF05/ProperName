__author__ = 'thiagocastroferreira'

import os

"""
Author: Thiago Castro Ferreira
Date: 12/04/2016
Description:
    This script aims to get information about the wikilinks entities studied in the project.
    The information concerns the proper names classes extracted from DBpedia, and the wikilinks pages
    where the entity was mentioned
"""

def get_entity(entity):
    attributes = {}

    birthPlaces = entity[1].split('\t')
    attributes[birthPlaces[0]] = filter(lambda x: x != '', birthPlaces[1:])

    surnames = entity[2].split('\t')
    attributes[surnames[0]] = filter(lambda x: x != '', surnames[1:])

    birthNames = entity[3].split('\t')
    attributes[birthNames[0]] = filter(lambda x: x != '', birthNames[1:])

    givenNames = entity[4].split('\t')
    attributes[givenNames[0]] = filter(lambda x: x != '', givenNames[1:])

    foaf_names = entity[5].split('\t')
    attributes[foaf_names[0]] = filter(lambda x: x != '', foaf_names[1:])

    birthDates = entity[6].split('\t')
    attributes[birthDates[0]] = filter(lambda x: x != '', birthDates[1:])

    dbp_names = entity[7].split('\t')
    attributes[dbp_names[0]] = filter(lambda x: x != '', dbp_names[1:])

    aliases = entity[8].split('\t')
    attributes[aliases[0]] = filter(lambda x: x != '', aliases[1:])
    return (entity[0], attributes)

def get_entities(fname='', list_entities = []):
    entities = []

    with open(fname) as f:
        doc = f.read().split('\n\n\n')[:-1]

        for entity in doc:
            entity = entity.split('\n')
            if len(list_entities) == 0 or entity[0] in list_entities:
                entities.append(get_entity(entity))
    return dict(entities)

def get_entities_indir(fdir):
    people = {}
    l = os.listdir(fdir)

    for _f in l:
        people[_f] = get_entities(os.path.join(fdir, _f))

    return people

def get_urls(fname):
    def parse_urls(urls):
        urls = urls.split('\n')
        entity, urls = urls[0], map(lambda x: x.split('\t'), urls[1:])
        return (entity, urls)

    with open(fname) as f:
        urls = f.read().split('\n\n')[:-1]
        return dict(map(lambda x: parse_urls(x), urls))

def run(fname = '/Users/thiagocastroferreira/Documents/Doutorado/Second Chapter/Names/Models/data/urls-top50.txt', \
        fentities = '/Users/thiagocastroferreira/Documents/Doutorado/Second Chapter/Names/Models/data/entities/'):
    urls = get_urls(fname)
    entities = get_entities(fname=fentities, list_entities=urls.keys())

    return urls, entities