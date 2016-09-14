__author__ = 'thiagocastroferreira'

import json
import unittest

from main.eacl.models.siddharthan import Siddharthan

class SiddharthanTest(unittest.TestCase):
    dbpedia_dir = '/roaming/tcastrof/names/eacl/name_base.json'

    dbpedia = json.load(open(dbpedia_dir))

    model = Siddharthan(dbpedia)

    def test_foaf_new(self):
        entity = 'http://en.wikipedia.org/wiki/Charles_Bukowski'
        self.assertTupleEqual(tuple(self.model.run(entity, 'new', 'np-subj')), ('+f+l', 'Charles Bukowski'))

    def test_foaf_old(self):
        entity = 'http://en.wikipedia.org/wiki/Charles_Bukowski'
        self.assertTupleEqual(tuple(self.model.run(entity, 'old', 'np-subj')), ('+l', 'Bukowski'))

    def test_birth_new(self):
        entity = "http://en.wikipedia.org/wiki/Adam_Sandler"
        self.assertTupleEqual(tuple(self.model.run(entity, 'new', 'np-subj')), ('+f+m+l', 'Adam Richard Sandler'))

    def test_birth_old(self):
        entity = "http://en.wikipedia.org/wiki/Adam_Sandler"
        self.assertTupleEqual(tuple(self.model.run(entity, 'old', 'np-subj')), ('+l', 'Sandler'))

    def test_birth_new_det(self):
        entity = "http://en.wikipedia.org/wiki/Adam_Sandler"
        self.assertTupleEqual(tuple(self.model.run(entity, 'new', 'subj-det')), ('+f+m+l', 'Adam Richard Sandler\'s'))

    def test_birth_old_det(self):
        entity = "http://en.wikipedia.org/wiki/Adam_Sandler"
        self.assertTupleEqual(tuple(self.model.run(entity, 'old', 'subj-det')), ('+l', 'Sandler\'s'))