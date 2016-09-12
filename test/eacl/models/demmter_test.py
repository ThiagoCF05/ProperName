__author__ = 'thiagocastroferreira'

import unittest

from main.eacl.models.deemter import Deemter

class DemmterTest(unittest.TestCase):

    # given and surnames
    def test_get_names_1(self):
        dbpedia_dir = '/roaming/tcastrof/names/eacl/dbpedia.json'
        parsed_dir = '/roaming/tcastrof/names/parsed'

        model = Deemter(dbpedia_dir, parsed_dir)

        model.entity = 'http://en.wikipedia.org/wiki/Charles_Bukowski'
        self.assertEqual(model._get_names(), ['Bukowski', 'Charles', 'Charles Bukowski'])

    # birth names
    def test_get_names_1(self):
        dbpedia_dir = '/roaming/tcastrof/names/eacl/dbpedia.json'
        parsed_dir = '/roaming/tcastrof/names/parsed'

        model = Deemter(dbpedia_dir, parsed_dir)

        model.entity = "http://en.wikipedia.org/wiki/Adam_Sandler"
        self.assertEqual(model._get_names(), ['Sandler', 'Adam', 'Adam Sandler'])