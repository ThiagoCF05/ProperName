__author__ = 'thiagocastroferreira'

import json
import os
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
        self.assertEqual(model._get_names(), ['Sandler', 'Adam', 'Adam Richard Sandler'])

    def test_distractors(self):
        dbpedia_dir = '/roaming/tcastrof/names/eacl/dbpedia.json'
        parsed_dir = '/roaming/tcastrof/names/parsed'
        mentions_dir = '/roaming/tcastrof/names/eacl/mentions'

        model = Deemter(dbpedia_dir, parsed_dir)

        model.target = {'has_appositive': False, 'text': 'Charles Bukowski', 'syntax-governor': [9, 'collection'],\
                  'text_prevTokens': 'of the Charles Bukowski', 'has_lastName': True, 'endIndex': 9, \
                  'position': [3, 4], 'number': 'SINGULAR', 'has_adjective': False, 'has_middleName': False, \
                  'appositive': None, 'syntax': 'subj-det', 'id': 17, 'titles': [], 'sentence-givenness': 'new', \
                  'type': 'PROPER', 'isRepresentativeMention': True, 'fname': '7298454', \
                  'name_type': ['foaf_names', 'dbp_names'], 'animacy': 'ANIMATE', 'givenness': 'new', \
                  'has_title': False, 'gender': 'MALE', 'has_firstName': True, 'startIndex': 7, \
                  'label': '+f+l', 'sentNum': 3}
        model.win = 3
        mentions = json.load(open(os.path.join(mentions_dir, model.target['fname'])))['http://en.wikipedia.org/wiki/Charles_Bukowski']

        result = model._get_distractors(mentions)
        result.sort()

        expected = ['07/11/12 13:16:04', '1987', 'Barfly', 'Dutch company Scotch & Soda', \
                    'Dutch company Scotch & Soda, acquired last year by Kellwood', 'Elena Vosnaki', \
                    'Elena Vosnaki', 'Kellwood', 'Scotch & Soda', \
                    'The textile producing Dutch company Scotch & Soda, acquired last year by Kellwood', 'Their', \
                    'Their offering', 'a follow-up', 'a fragrance', 'autobiographical stories of the same name', \
                    'first', 'last year', 'the eponymous film', 'the first time', \
                    'the perfume arena for the first time', 'the same name', 'their', \
                    'their Spring-Summer 2013 collection']

        self.assertListEqual(result, expected)

