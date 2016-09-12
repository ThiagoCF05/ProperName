from main.corpus_builder import loader

__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 23/05/2016
Description:
    This script aims to create a proper name knowledge base as the one described in the INLG paper.
    Attributes: first, middle and last names
"""


def update(dbpedia):
    def is_added(name):
        if name in dbpedia['first_names'] or name in dbpedia['middle_names'] or name in dbpedia['last_names']:
            return True
        return False

    # del dbpedia['aliases']

    dbpedia['first_names'] = []
    dbpedia['middle_names'] = []
    dbpedia['last_names'] = []

    # add surname as last name
    dbpedia['last_names'].extend(dbpedia['surnames'])

    for birthName in dbpedia['birthNames']:
        names = birthName.split()

        if len(names[0]) > 2 and not is_added(names[0]):
            dbpedia['first_names'].append(names[0])
        if len(names[-1]) > 2 and not is_added(names[-1]):
            dbpedia['last_names'].append(names[-1])
        names.remove(names[-1])
        for middle in names[1:]:
            if len(middle) > 2 and not is_added(middle):
                dbpedia['middle_names'].append(middle)

    # remove the given names in the citation format (Einstein, Albert)
    givenNames = filter(lambda given: ',' not in given, dbpedia['givenNames'])
    # select the shortest given name
    sizes = map(lambda given: len(given.split()), givenNames)
    if len(sizes) > 0:
        min_size = min(sizes)
        givenName = filter(lambda given: len(given.split()) == min_size, givenNames)[0]

        names = givenName.split()

        if len(names[0]) > 2 and not is_added(names[0]):
            dbpedia['first_names'].append(names[0])
        for middle in names[1:]:
            if len(middle) > 2 and not is_added(middle):
                dbpedia['middle_names'].append(middle)

    name = filter(lambda x: ',' not in x, dbpedia['foaf_names'])
    if len(name) > 0:
        names = name[0].split()

        if len(names[0]) > 2 and not is_added(names[0]):
            dbpedia['first_names'].append(names[0])
        if len(names[-1]) > 2 and not is_added(names[-1]):
            dbpedia['last_names'].append(names[-1])
        names.remove(names[-1])
        for middle in names[1:]:
            if len(middle) > 2 and not is_added(middle):
                dbpedia['middle_names'].append(middle)

    dbpedia['first_names'] = list(set(dbpedia['first_names']))
    dbpedia['middle_names'] = list(set(dbpedia['middle_names']))
    dbpedia['last_names'] = list(set(dbpedia['last_names']))
    return dbpedia

if __name__ == '__main__':
    entities = loader.get_entities_indir('/roaming/tcastrof/names/entities')

