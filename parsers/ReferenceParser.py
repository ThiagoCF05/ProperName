__author__ = 'thiagocastroferreira'

import xml.etree.ElementTree as ET
import copy
from Parser import Parser
import corpus_builder

class ReferenceParser(Parser):
    def __init__(self, append_other = False, append_refex = True, root = 'data/xmls'):
        super(Parser)
        self.append_other = append_other
        self.append_refex = append_refex
        self.root = root

    def run(self):
        lists = self.list_files(self.root)

        references = []

        keys = lists.keys()
        keys.sort()
        for l in keys:
            for f in lists[l]:
                references.extend(self.parse_text(f, l))

        return references

    def parse_text(self, xml, list_id):
        references = []
        root = ET.parse(xml)
        root = root.getroot()

        paragraphs = root.findall('PARAGRAPH')

        for p in paragraphs:
            sentences = p.findall('SENTENCE')
            for s in sentences:
                for i, child in enumerate(s):
                    if child.tag == 'REFERENCE':
                        ref = child
                        reference = {}
                        reference['list-id'] = list_id
                        reference['paragraph-id'] = int(p.attrib['ID'])
                        reference['sentence-id'] = int(s.attrib['ID'].split('.')[1])
                        reference['text-id'] = root.attrib['ID']
                        reference['file'] = xml.split('/')[-1].split('.')[0]

                        reference['syncat'] = ref.attrib['SYNCAT']

                        reference['entropy'] = float(ref.attrib['ENTROPY'])
                        reference['paragraph-recency'] = int(ref.attrib['PARAGRAPH-RECENCY'])
                        reference['categorical-recency'] = corpus_builder.recency(int(ref.attrib['PARAGRAPH-RECENCY']))
                        reference['paragraph-position'] = int(ref.attrib['PARAGRAPH-POSITION'])
                        reference['sentence-recency'] = int(ref.attrib['SENTENCE-RECENCY'])
                        reference['sentence-position'] = int(ref.attrib['SENTENCE-POSITION'])
                        reference['reference-id'] = int(ref.attrib['ID'])
                        reference['original-type'] = ref.find('ORIGINAL-REFEX').find('REFEX').attrib['TYPE']
                        reference['animacy'] = root.attrib['TOPIC-ANIMACY']

                        reference['genre'] = root.attrib['GENRE']

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

                        if self.append_refex:
                            for refex in ref.find('PARTICIPANTS-REFEX').findall('REFEX'):
                                row = copy.copy(reference)
                                row['participant-id'] = refex.attrib['PARTICIPANT-ID']
                                row['type'] = refex.attrib['TYPE']
                                row['refex'] = refex.text
                                if row['type'] == 'other':
                                    if self.append_other == True:
                                        references.append(row)
                                else:
                                    references.append(row)
                        else:
                            references.append(reference)
        return references