__author__ = 'thiagocastroferreira'

import json

class Siddharthan(object):
    def __init__(self, dbpedia_dir):
        self.dbpedia = json.load(open(dbpedia_dir))

    def run(self, entity, discourse):
        if discourse == 'new':
            if len(self.dbpedia[entity]['givenNames']) > 0:
                givenNames = self.dbpedia[entity]['givenNames']
                first = filter(lambda x: len(x) == min(map(lambda x: len(x), givenNames)), givenNames)[0]

                surnames = self.dbpedia[entity]['surnames']
                last = filter(lambda x: len(x) == min(map(lambda x: len(x), surnames)), surnames)[0]

                return str(first).strip() + ' ' + str(last).strip()
            else:
                birthNames = self.dbpedia[entity]['birthNames']
                name = filter(lambda x: len(x) == min(map(lambda x: len(x), birthNames)), birthNames)[0]
                return str(name).strip()
        else:
            if len(self.dbpedia[entity]['surnames']) > 0:
                surnames = self.dbpedia[entity]['surnames']
                last = filter(lambda x: len(x) == min(map(lambda x: len(x), surnames)), surnames)[0]

                return str(last).strip()
            else:
                birthNames = self.dbpedia[entity]['birthNames']
                name = filter(lambda x: len(x) == min(map(lambda x: len(x), birthNames)), birthNames)[0]
                return str(name).strip().split()[-1]