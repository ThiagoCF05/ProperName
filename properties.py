__author__ = 'thiagocastroferreira'

import os

root_dir = '/roaming/tcastrof/names/eacl'
parsed_dir = '/roaming/tcastrof/names/regnames/parsed'
mentions_dir = '/roaming/tcastrof/names/eacl/mentions'
webpages_dir = '/roaming/tcastrof/names/regnames/webpages'

file_dbpedia = os.path.join(root_dir, 'name_base.json')
file_urls = os.path.join(root_dir, 'furls.json')
file_entities = os.path.join(root_dir, 'entities.json')
file_titles = os.path.join(root_dir, 'all_titles.json')
file_appositives = os.path.join(root_dir, 'appositives.json')

file_vocabulary = os.path.join(root_dir, 'stats/voc.json')
evaluation_dir = os.path.join(root_dir, 'evaluation/intrinsic_domain')