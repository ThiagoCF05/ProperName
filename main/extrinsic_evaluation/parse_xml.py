__author__ = 'thiagocastroferreira'

import json
import os
import xml.etree.ElementTree as ET

entities_dir = '/roaming/tcastrof/names/eacl/entities.json'

abstract_dir = '/roaming/tcastrof/names/eacl/evaluation/extrinsic/abstracts'
parsed_dir = '/roaming/tcastrof/names/eacl/evaluation/extrinsic/parsed'
mentions_dir = '/roaming/tcastrof/names/eacl/evaluation/extrinsic/mentions'

if __name__ == '__main__':
    entities = json.load(open(entities_dir))

    root = ET.fromstring("<?xml version=\"1.0\" encoding=\"utf-8\"?>")

    for entity_id in os.listdir(mentions_dir):
        entity = filter(lambda x: x['id'] == entity_id, entities)[0]

        parsed = json.load(open(os.path.join(parsed_dir, entity_id)))
        mentions = json.load(os.path.join(mentions_dir, entity_id))[entity['url']]

        text = ET.SubElement(root, 'TEXT')
        text.attrib['ID'] = entity_id

        paragraph = ET.SubElement(text, 'PARAGRAPH')
        paragraph['ID'] = str(1)

        reference_id = 1
        for i, s in enumerate(parsed['sentences']):
            fmentions = filter(lambda x: x['sentNum'] == i+1, mentions)

            indexes = map(lambda x: (x['startIndex']))

            sentence = ET.SubElement(paragraph, 'SENTENCE')
            sentence.attrib['ID'] = str(i+1)

            elem = None
            for itoken, token in enumerate(s['tokens']):
                pass