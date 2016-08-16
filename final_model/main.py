__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 15/08/2016
Description:
    Main method EACL 2017 model
"""

import w2voc
import training
import settings

def run():
    voc, fvoc = w2voc.run('std')

    train_set = filter(lambda x: x['label'] in settings.labels, fvoc)
    train = training.run(train_set, True, 'std')