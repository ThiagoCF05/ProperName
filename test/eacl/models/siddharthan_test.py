__author__ = 'thiagocastroferreira'

import unittest

from main.eacl.models.siddharthan import Siddharthan

class SiddharthanTest(unittest.TestCase):
    dbpedia_dir = '/roaming/tcastrof/names/eacl/fdbpedia.json'

    def test_foaf_new(self):
        model = Siddharthan(dbpedia_dir=self.dbpedia_dir)

        entity = 'http://en.wikipedia.org/wiki/Charles_Bukowski'
        self.assertTupleEqual(tuple(model.run(entity, 'new')), ('+f+l', 'Charles Bukowski'))

    def test_foaf_old(self):
        model = Siddharthan(dbpedia_dir=self.dbpedia_dir)

        entity = 'http://en.wikipedia.org/wiki/Charles_Bukowski'
        self.assertTupleEqual(tuple(model.run(entity, 'old')), ('+l', 'Bukowski'))

    def test_birth_new(self):
        model = Siddharthan(dbpedia_dir=self.dbpedia_dir)
        entity = "http://en.wikipedia.org/wiki/Adam_Sandler"
        self.assertTupleEqual(tuple(model.run(entity, 'new')), ('+f+m+l', 'Adam Richard Sandler'))

    def test_birth_old(self):
        model = Siddharthan(dbpedia_dir=self.dbpedia_dir)
        entity = "http://en.wikipedia.org/wiki/Adam_Sandler"
        self.assertTupleEqual(tuple(model.run(entity, 'old')), ('+l', 'Sandler'))