__author__ = 'thiagocastroferreira'

import json
import os

class Deemter(object):
    def __init__(self, dbpedia_dir, parsed_dir):
        self.dbpedia = json.load(open(dbpedia_dir))
        self.parsed_dir = parsed_dir

        self.distractors = None
        self.entity = None
        self.mentions = None
        self.parsed = None
        self.target = None
        self.win = None

    def _get_distractors(self, mentions):
        def isDistractor(mention, intervals):
            for i in range(mention['startIndex']-1,mention['endIndex']):
                if len(filter(lambda x: x[2] == mention['sentNum'] and i in range(x[0], x[1]+1), intervals)) != 0:
                    return False
            return True

        # select all the mentions to the target entity in the context window size win
        self.mentions = filter(lambda x: x['fname'] == self.target['fname'] \
                                         and self.target['sentNum']-self.win <= x['sentNum'] <= self.target['sentNum'], mentions)

        intervals = map(lambda x: (x['startIndex']-1, x['endIndex']-1, x['sentNum']), self.mentions)

        distractors = []
        for e in self.parsed['corefs']:
            # select all the mentions in the context window size win
            f = filter(lambda x: self.target['sentNum']-self.win <= x['sentNum'] <= self.target['sentNum'], self.parsed['corefs'][e])
            for mention in f:
                # check if the mention is a distractor
                if isDistractor(mention, intervals):
                    distractor = self.parsed['sentences'][mention['sentNum']-1]['tokens'][mention['startIndex']-1:mention['endIndex']-1]
                    distractors.append(distractor)
        return distractors

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

    def _get_reference(self):
        # get last, first and full name from the entity
        names = self._get_names()

        isResult = True
        for name in names:
            for distractor in self.distractors:
                if name in distractor['text']:
                    isResult = False
                    break
            if isResult:
                return name
        return names[-1]

    def run(self, entity, target, mentions, win):
        self.entity = entity
        self.target = target
        self.win = win

        self.parsed = json.load(open(os.path.join(self.parsed_dir, target['fname'])))

        self.distractors = self._get_distractors(mentions)
        return self._get_reference()