__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 15/08/2016
Description:
    Label the nominal references according to their attribute-set.
    (Attributes: title, first, middle, last, appositive)
"""

def label(mention):
    attribute_set = ''
    if mention['has_title']:
        attribute_set = attribute_set + '+t'

    if mention['has_firstName']:
        attribute_set = attribute_set + '+f'

    if mention['has_middleName']:
        attribute_set = attribute_set + '+m'

    if mention['has_lastName']:
        attribute_set = attribute_set + '+l'

    if mention['has_appositive']:
        attribute_set = attribute_set + '+a'

    return attribute_set