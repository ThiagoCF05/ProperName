__author__ = 'thiagocastroferreira'

__author__ = 'thiagocastroferreira'

from main.eacl import preprocessing as prep
from random import randint

class Random(object):
    def __init__(self, dbpedia):
        self.dbpedia = dbpedia

        self.entity = None

    # return the last, first and complete name from the entity (int this order)
    def _get_names(self):
        if len(self.dbpedia[self.entity]['givenNames']) > 0:
            givenNames = self.dbpedia[self.entity]['givenNames']
            first = filter(lambda x: len(x) == min(map(lambda x: len(x), givenNames)), givenNames)[0]

            surnames = self.dbpedia[self.entity]['surnames']
            last = filter(lambda x: len(x) == min(map(lambda x: len(x), surnames)), surnames)[0]

            first = str(first).strip()
            last = str(last).strip()
            name = first + ' ' + last
        else:
            birthNames = self.dbpedia[self.entity]['birthNames']
            name = str(filter(lambda x: len(x) == min(map(lambda x: len(x), birthNames)), birthNames)[0]).strip()

            aux = name.split()
            first = aux[0]
            last = aux[-1]
        return [last, first, name]

    def run(self, entity):
        self.entity = entity

        self.names = self._get_names()

        index = randint(0, len(self.names)-1)
        name = self.names[index]

        return prep.get_label(name, self.dbpedia[self.entity]), name