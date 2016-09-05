__author__ = 'thiagocastroferreira'

import json
import os

class Deemter(object):
    def __init__(self, dbpedia_dir, parsed_dir, target, mentions, win):
        self.dbpedia = json.load(open(dbpedia_dir))
        self.target = target
        self.mentions = mentions
        self.win = win

        self.parsed = json.load(open(os.path.join(parsed_dir, target['fname'])))

        # select all the mentions to the target entity in the context window size win
        self.mentions = filter(lambda x: x['fname'] == target['fname'] \
                                         and self.target['sentNum']-win <= x['sentNum'] <= self.target['sentNum'], mentions)
        self.distractors = self.get_distractors()

    def get_distractors(self):
        def isDistractor(mention, intervals):
            for i in range(mention['startIndex']-1,mention['endIndex']):
                if len(filter(lambda x: x[2] == mention['sentNum'] and i in range(x[0], x[1]+1), intervals)) != 0:
                    return False
            return True

        intervals = map(lambda x: (x['startIndex']-1, x['endIndex']-1, x['sentNum']), self.mentions)

        distractors = []
        for e in self.parsed['corefs']:
            # select all the mentions in the context window size win
            f = filter(lambda x: self.target['sentNum']-self.win <= x['sentNum'] <= self.target['sentNum'])
            for mention in f:
                if isDistractor(mention, intervals):
                    distractor = self.parsed['sentences'][mention['sentNum']-1]['tokens'][mention['startIndex']-1:mention['endIndex']-1]
                    distractors.append(distractor)

        return distractors

    def run(self):
        pass