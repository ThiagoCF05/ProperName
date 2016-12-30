__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 12/04/2016
Description:
    This script aims to get all the possible variations of a proper name bigger than 2. For instance, for 'Philip Frederick Anschutz',
    the possible variations are 'Philip', 'Frederick', 'Anschutz', 'Philip Frederick', 'Philip Anschutz' and
    'Frederick Anschutz'.
"""

import itertools

def get_variations(name):
    variations = []

    tokens = name.replace(',', '').split()
    for size in range(1, len(tokens)+1):
        variations.extend(map(lambda x: ' '.join(x), itertools.combinations(tokens, size)))

    return filter(lambda x: len(x) > 2, map(lambda x: x.lower(), variations))

''' ['foaf_names', 'dbp_names', 'birthNames', 'givenNames', 'surnames', 'first_names', 'middle_names', 'last_names'] '''

def get_variations_db(dbpedia_names = {}, type_names = ['first_names', 'middle_names', 'last_names']):
    variations = []
    for key in type_names:
        for name in dbpedia_names[key]:
            variations.extend(get_variations(name))
    return set(variations)

def names_variation(classes):
    combinations = []
    for size in range(1, len(classes)+1):
        l = list(itertools.combinations(classes, size))
        combinations.extend(l)
    return combinations
