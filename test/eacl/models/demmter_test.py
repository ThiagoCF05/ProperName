__author__ = 'thiagocastroferreira'

import json
import os
import unittest

from main.eacl.models.deemter import Deemter

class DemmterTest(unittest.TestCase):
    dbpedia_dir = '/roaming/tcastrof/names/eacl/fdbpedia.json'
    parsed_dir = '/roaming/tcastrof/names/parsed'
    mentions_dir = '/roaming/tcastrof/names/eacl/mentions'

    model = Deemter(dbpedia_dir, parsed_dir)

    # given and surnames
    def test_get_names_1(self):
        self.model.entity = 'http://en.wikipedia.org/wiki/Charles_Bukowski'
        self.assertEqual(self.model._get_names(), ['Bukowski', 'Charles', 'Charles Bukowski'])

    # birth names
    def test_get_names_2(self):
        self.model.entity = "http://en.wikipedia.org/wiki/Adam_Sandler"
        self.assertEqual(self.model._get_names(), ['Sandler', 'Adam', 'Adam Richard Sandler'])

    def test_distractors_1(self):
        self.model.target = {'has_appositive': False, 'text': 'Charles Bukowski', 'syntax-governor': [9, 'collection'],\
                  'text_prevTokens': 'of the Charles Bukowski', 'has_lastName': True, 'endIndex': 9, \
                  'position': [3, 4], 'number': 'SINGULAR', 'has_adjective': False, 'has_middleName': False, \
                  'appositive': None, 'syntax': 'subj-det', 'id': 17, 'titles': [], 'sentence-givenness': 'new', \
                  'type': 'PROPER', 'isRepresentativeMention': True, 'fname': '7298454', \
                  'name_type': ['foaf_names', 'dbp_names'], 'animacy': 'ANIMATE', 'givenness': 'new', \
                  'has_title': False, 'gender': 'MALE', 'has_firstName': True, 'startIndex': 7, \
                  'label': '+f+l', 'sentNum': 3}
        self.model.win = 3
        mentions = json.load(open(os.path.join(self.mentions_dir, self.model.target['fname'])))['http://en.wikipedia.org/wiki/Charles_Bukowski']

        result = self.model._get_distractors(mentions)
        result.sort()

        expected = ['07/11/12 13:16:04', '1987', 'Barfly', 'Dutch company Scotch & Soda', \
                    'Dutch company Scotch & Soda, acquired last year by Kellwood', 'Elena Vosnaki', \
                    'Elena Vosnaki\nThe textile producing Dutch company Scotch & Soda, acquired last year by Kellwood', \
                    'Kellwood', 'Scotch & Soda', 'Their', 'Their offering', 'a follow-up', 'a fragrance', \
                    'autobiographical stories of the same name', 'first', 'last year', 'the eponymous film', \
                    'the first time', 'the perfume arena for the first time', 'the same name', 'their', \
                    'their Spring-Summer 2013 collection']

        self.assertListEqual(result, expected)

    def test_get_reference(self):
        self.model.entity = 'http://en.wikipedia.org/wiki/Charles_Bukowski'
        self.model.target = {'has_appositive': False, 'text': 'Charles Bukowski', 'syntax-governor': [9, 'collection'], \
                             'text_prevTokens': 'of the Charles Bukowski', 'has_lastName': True, 'endIndex': 9, \
                             'position': [3, 4], 'number': 'SINGULAR', 'has_adjective': False, 'has_middleName': False, \
                             'appositive': None, 'syntax': 'subj-det', 'id': 17, 'titles': [], 'sentence-givenness': 'new', \
                             'type': 'PROPER', 'isRepresentativeMention': True, 'fname': '7298454', \
                             'name_type': ['foaf_names', 'dbp_names'], 'animacy': 'ANIMATE', 'givenness': 'new', \
                             'has_title': False, 'gender': 'MALE', 'has_firstName': True, 'startIndex': 7, \
                             'label': '+f+l', 'sentNum': 3}

        self.model.distractors = ['07/11/12 13:16:04', '1987', 'Barfly', 'Dutch company Scotch & Soda', \
                    'Dutch company Scotch & Soda, acquired last year by Kellwood', 'Elena Vosnaki', \
                    'Elena Vosnaki\nThe textile producing Dutch company Scotch & Soda, acquired last year by Kellwood', \
                    'Kellwood', 'Scotch & Soda', 'Their', 'Their offering', 'a follow-up', 'a fragrance', \
                    'autobiographical stories of the same name', 'first', 'last year', 'the eponymous film', \
                    'the first time', 'the perfume arena for the first time', 'the same name', 'their', \
                    'their Spring-Summer 2013 collection', 'Bukowski', 'Charles']

        result = tuple(self.model._get_reference(syntax='np-subj'))
        self.assertTupleEqual(('+f+l', 'Charles Bukowski'), result)

    def test_run_1(self):
        entity = 'http://en.wikipedia.org/wiki/Charles_Bukowski'
        target = {'has_appositive': False, 'text': 'Charles Bukowski', 'syntax-governor': [9, 'collection'], \
                        'text_prevTokens': 'of the Charles Bukowski', 'has_lastName': True, 'endIndex': 9, \
                        'position': [3, 4], 'number': 'SINGULAR', 'has_adjective': False, 'has_middleName': False, \
                        'appositive': None, 'syntax': 'subj-det', 'id': 17, 'titles': [], 'sentence-givenness': 'new', \
                        'type': 'PROPER', 'isRepresentativeMention': True, 'fname': '7298454', \
                        'name_type': ['foaf_names', 'dbp_names'], 'animacy': 'ANIMATE', 'givenness': 'new', \
                        'has_title': False, 'gender': 'MALE', 'has_firstName': True, 'startIndex': 7, \
                        'label': '+f+l', 'sentNum': 3}
        win = 3
        mentions = json.load(open(os.path.join(self.mentions_dir, target['fname'])))[entity]
        result = tuple(self.model.run(entity=entity, target=target, mentions=mentions, win=win, syntax=target['syntax']))
        self.assertTupleEqual(('+l', 'Bukowski\'s'), result)

    def test_run_2(self):
        entity = 'http://en.wikipedia.org/wiki/Charles_Bukowski'
        target = {'has_appositive': False, 'text': 'Charles Bukowski', 'syntax-governor': [9, 'collection'], \
                  'text_prevTokens': 'of the Charles Bukowski', 'has_lastName': True, 'endIndex': 9, \
                  'position': [3, 4], 'number': 'SINGULAR', 'has_adjective': False, 'has_middleName': False, \
                  'appositive': None, 'syntax': 'subj-det', 'id': 17, 'titles': [], 'sentence-givenness': 'new', \
                  'type': 'PROPER', 'isRepresentativeMention': True, 'fname': '7298454', \
                  'name_type': ['foaf_names', 'dbp_names'], 'animacy': 'ANIMATE', 'givenness': 'new', \
                  'has_title': False, 'gender': 'MALE', 'has_firstName': True, 'startIndex': 7, \
                  'label': '+f+l', 'sentNum': 3}
        win = 3
        mentions = json.load(open(os.path.join(self.mentions_dir, target['fname'])))[entity]

        result = tuple(self.model.run(entity=entity, target=target, mentions=mentions, win=win, syntax='np-subj'))
        self.assertTupleEqual(('+l', 'Bukowski'), result)


