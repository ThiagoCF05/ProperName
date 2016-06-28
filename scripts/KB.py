__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 23/05/2016
Description:
    This script aims to create a proper name knowledge base as the one described in the INLG paper.
    Attributes: first, middle and last names
"""

import utils.loader as loader

def update(dbpedia):
    dbpedia['first_names'] = []
    dbpedia['middle_names'] = []
    dbpedia['last_names'] = []

    for givenName in dbpedia['givenNames']:
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
    entities = loader.get_entities_indir('/roaming/tcastrof/names/entities')

