__author__ = 'thiagocastroferreira'

import unittest

from main.eacl.models.siddharthan import Siddharthan

class SiddharthanTest(unittest.TestCase):
    dbpedia_dir = '/roaming/tcastrof/names/eacl/fdbpedia.json'

    def test_foaf_new(self):
        model = Siddharthan(dbpedia_dir=self.dbpedia_dir)

        entity = 'http://en.wikipedia.org/wiki/Charles_Bukowski'
        self.assertTupleEqual(tuple(model.run(entity, 'new', 'np-subj')), ('+f+l', 'Charles Bukowski'))

    def test_foaf_old(self):
        model = Siddharthan(dbpedia_dir=self.dbpedia_dir)

        entity = 'http://en.wikipedia.org/wiki/Charles_Bukowski'
        self.assertTupleEqual(tuple(model.run(entity, 'old', 'np-subj')), ('+l', 'Bukowski'))

    def test_birth_new(self):
        model = Siddharthan(dbpedia_dir=self.dbpedia_dir)
        entity = "http://en.wikipedia.org/wiki/Adam_Sandler"
        self.assertTupleEqual(tuple(model.run(entity, 'new', 'np-subj')), ('+f+m+l', 'Adam Richard Sandler'))

    def test_birth_old(self):
        model = Siddharthan(dbpedia_dir=self.dbpedia_dir)
        entity = "http://en.wikipedia.org/wiki/Adam_Sandler"
        self.assertTupleEqual(tuple(model.run(entity, 'old', 'np-subj')), ('+l', 'Sandler'))

    def test_birth_new_det(self):
        model = Siddharthan(dbpedia_dir=self.dbpedia_dir)
        entity = "http://en.wikipedia.org/wiki/Adam_Sandler"
        self.assertTupleEqual(tuple(model.run(entity, 'new', 'subj-det')), ('+f+m+l', 'Adam Richard Sandler\'s'))

    def test_birth_old_det(self):
        model = Siddharthan(dbpedia_dir=self.dbpedia_dir)
        entity = "http://en.wikipedia.org/wiki/Adam_Sandler"
        self.assertTupleEqual(tuple(model.run(entity, 'old', 'subj-det')), ('+l', 'Sandler\'s'))