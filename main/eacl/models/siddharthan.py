__author__ = 'thiagocastroferreira'

import json
from main.utils import KB as kb
from main.eacl import preprocessing as prep

class Siddharthan(object):
    def __init__(self, dbpedia_dir):
        self.dbpedia = json.load(open(dbpedia_dir))

    def realize(self, name, syntax):
        if syntax == 'subj-det' and (name[-2:] != '\'s' or name[-1] != '\''):
            if name[-1] == 's':
                name = name + '\''
            else:
                name = name + '\'s'
        return name

    def run(self, entity, discourse, syntax):
        if discourse == 'new':
            if len(self.dbpedia[entity]['givenNames']) > 0:
                givenNames = self.dbpedia[entity]['givenNames']
                first = filter(lambda x: len(x) == min(map(lambda x: len(x), givenNames)), givenNames)[0]

                surnames = self.dbpedia[entity]['surnames']
                last = filter(lambda x: len(x) == min(map(lambda x: len(x), surnames)), surnames)[0]

                name = str(first).strip() + ' ' + str(last).strip()
            else:
                birthNames = self.dbpedia[entity]['birthNames']
                name = str(filter(lambda x: len(x) == min(map(lambda x: len(x), birthNames)), birthNames)[0]).strip()
        else:
            if len(self.dbpedia[entity]['surnames']) > 0:
                surnames = self.dbpedia[entity]['surnames']
                last = filter(lambda x: len(x) == min(map(lambda x: len(x), surnames)), surnames)[0]

                name = str(last).strip()
            else:
                birthNames = self.dbpedia[entity]['birthNames']
                name = str(filter(lambda x: len(x) == min(map(lambda x: len(x), birthNames)), birthNames)[0]).strip().split()[-1]

        name = self.realize(name, syntax)
        return prep.get_label(name, kb.update(self.dbpedia[entity])), name