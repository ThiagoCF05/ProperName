__author__ = 'thiagocastroferreira'

import xml.etree.ElementTree as ET
import corpus_builder
import os

class GRECParser():
    def __init__(self, root = 'data/grec/oficial'):
        self.root = root

    def run(self):
        references = []

        for f in self.list_files():
            print f, '\r',
            references.extend(self.parse_text(f))

        return references

    def list_files(self):
        dirs = filter(lambda x: x != '.DS_Store', os.listdir(self.root))
        return dirs

    def run_plain_parse(self):
        texts = []

        for f in self.list_files():
            print f, '\r',
            texts.append(self.parse_plain_text(f))

        return texts

    def parse_plain_text(self, xml):
        root = ET.parse(os.path.join(self.root, xml))
        root = root.getroot()
        id = root.attrib['ID']

        paragraphs = root.findall('PARAGRAPH')

        text = {}
        originals = []
        nertype = 'LOCATION'

        for p_i, p in enumerate(paragraphs):
            sentences = p.findall('SENTENCE')
            paragraph = ''
            for s_i, s in enumerate(sentences):
                for i, child in enumerate(s):
                    if child.tag == 'REFERENCE':
                        if child.attrib['SEMCAT'] == 'person':
                            nertype = 'PERSON'

                        original = child.find('ORIGINAL-REFEX').find('REFEX').text
                        originals.append({'id': child.attrib['ID'], 'paragraph_id':p_i+1, 'sentence_id':s_i+1, \
                                          'reference': original, 'position':child.attrib['PARAGRAPH-POSITION']})
                        # if child.attrib['SYNCAT'] == 'subj-det':
                        #     paragraph = paragraph + 'Thiago Castro' + '\'s '
                        # else:
                        #     paragraph = paragraph + 'Thiago Castro' + ' '
                        paragraph = paragraph + original + ' '
                    elif child.tag == 'STRING':
                        paragraph = paragraph + child.text.strip() + ' '
            text[p_i+1] = paragraph
        return (id, text, originals, nertype)

    def parse_text(self, xml):
        references = []
        root = ET.parse(os.path.join(self.root, xml))
        root = root.getroot()
        paragraphs = root.findall('PARAGRAPH')

        for p in paragraphs:
            sentences = p.findall('SENTENCE')
            for s in sentences:
                for i, child in enumerate(s):
                    if child.tag == 'REFERENCE':
                        ref = child
                        reference = {}
                        reference['paragraph-id'] = int(p.attrib['ID'])
                        reference['text-id'] = root.attrib['ID']

                        reference['syncat'] = ref.attrib['SYNCAT']

                        reference['paragraph-recency'] = int(ref.attrib['PARAGRAPH-RECENCY'])
                        reference['categorical-recency'] = corpus_builder.recency(int(ref.attrib['PARAGRAPH-RECENCY']))
                        reference['paragraph-position'] = int(ref.attrib['PARAGRAPH-POSITION'])
                        reference['sentence-recency'] = int(ref.attrib['SENTENCE-RECENCY'])
                        reference['sentence-position'] = int(ref.attrib['SENTENCE-POSITION'])
                        reference['reference-id'] = int(ref.attrib['ID'])

                        original = ref.find('ORIGINAL-REFEX').find('REFEX')
                        reference['type'] = original.attrib['TYPE']
                        reference['head'] = original.attrib['HEAD']
                        reference['case'] = original.attrib['CASE']
                        reference['emphatic'] = original.attrib['EMPHATIC']
                        reference['refex'] = original.text

                        reference['name'] = xml

                        if ref.attrib['SEMCAT'] == 'person':
                            reference['animacy'] = 'animate'
                        else:
                            reference['animacy'] = 'inanimate'

                        if int(reference['reference-id']) == 1:
                            reference['givenness'] = 'new'
                        else:
                            reference['givenness'] = 'given'

                        if int(reference['paragraph-recency']) == 0:
                            reference['paragraph-givenness'] = 'new'
                        else:
                            reference['paragraph-givenness'] = 'given'

                        if int(reference['sentence-recency']) == 0:
                            reference['sentence-givenness'] = 'new'
                        else:
                            reference['sentence-givenness'] = 'given'

                        references.append(reference)

        return references