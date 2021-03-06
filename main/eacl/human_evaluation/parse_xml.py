__author__ = 'thiagocastroferreira'

import copy
import json
import os

import main.eacl.preprocessing as prep
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

from main.eacl.models.Bayes import Bayes
from main.eacl.models.random_baseline import Random
from main.eacl.models.siddharthan import Siddharthan

from random import randint, shuffle

class HumanEvaluation(object):
    def __init__(self, train_set_content, train_set_realization, dbpedia, words, appositive, xml, write_dir):
        # models
        self.bayes = Bayes(train_set_content, train_set_realization, True)
        self.random_baseline = Random(dbpedia)
        self.siddharthan = Siddharthan(dbpedia)

        self.words = words
        self.appositive = appositive
        self.xml = xml
        self.write_dir = write_dir

        self.references = []
        self.results = {}

        self.run()

    def run(self):
        print 'Get references...'
        root = ET.parse(self.xml)
        root = root.getroot()
        reference_tags = map(lambda paragraph: paragraph.findall('REFERENCE'), root.findall('PARAGRAPH'))

        self.entity = root.attrib['ENTITY']
        self.references = map(lambda x: x.attrib, reduce(lambda x, y: x+y, reference_tags))

        print 'Generating...'
        self._generate()

        print 'Parsing...'
        new_xml = self._parse(root)

        print 'Writing...'
        title = root.find('TITLE').text
        with open(os.path.join(self.write_dir, title+'.xml'), 'w') as f:
            f.write(new_xml.encode('utf-8'))

    def _generate(self):
        def bayes_selection(_features, k):
            if k != None:
                prob = self.bayes.select_content_backoff(_features, self.entity, k)
            else:
                prob = self.bayes.select_content(_features, self.entity)
            return prob

        def bayes_variation(references, form_distribution, mentions, name):
            distribution = {}
            for form in form_distribution:
                distribution[form[0]] = len(references) * form[1]

            shuffle(references)
            for i, reference in enumerate(references):
                form = filter(lambda x: distribution[x] == max(distribution.values()), distribution.keys())[0]

                realizer = self.bayes.realizeWithWords(form, self.entity, mentions[i]['SYNCAT'], self.words, self.appositive)
                label = filter(lambda x: x[0] == form, form_distribution)[0]
                references[i][name] = { 'label': form, 'prob': label[1], 'reference': realizer[0][0] }

                distribution[form] -= 1
            return references

        for _givenness in ['new', 'old']:
            for _sgivenness in ['new', 'old']:
                for _syntax in ['np-subj', 'np-obj', 'subj-det']:
                    # Group proper name references from the test fold by feature values
                    same_features = filter(lambda x: x['GIVENNESS'] == _givenness \
                                                              and x['SENTENCE-GIVENNESS'] == _sgivenness \
                                                              and x['SYNCAT'] == _syntax, self.references)
                    if len(same_features) > 0:
                        print _givenness, _sgivenness, _syntax

                    _features = {
                        # 's_e': mention['label'],
                        'discourse_se': _givenness,
                        'sentence_se': _sgivenness,
                        'syntax_se': _syntax
                    }

                    # Bayes model selection
                    form_distribution = bayes_selection(_features, None)
                    # form_distribution_k0 = bayes_selection(_features, 0)
                    # form_distribution_k2 = bayes_selection(_features, 2)

                    # Siddharthan model
                    siddharthan_result = self.siddharthan.run(self.entity, _givenness, _syntax)

                    # Bayes model with no variation (Realization with the most likely referential form)
                    bayes_result = self.bayes.realizeWithWords(form_distribution[0][0], self.entity, _syntax, self.words, self.appositive)

                    # Generate proper names for each group of features
                    group_result = []
                    for filtered_mention in same_features:
                        result = {'ID': filtered_mention['ID']}

                        # Random model
                        r = self.random_baseline.run(self.entity, filtered_mention['SYNCAT'])
                        result['random'] = { 'label': r[0], 'reference': r[1] }

                        result['siddharthan'] = { 'label': siddharthan_result[0], 'reference': siddharthan_result[1] }

                        result['bayes_no_variation'] = { 'label': form_distribution[0][0], 'prob': form_distribution[0][1], 'reference': bayes_result[0][0] }

                        group_result.append(result)

                    # Generate proper names with individual variation in the for choice
                    group_result = bayes_variation(group_result, form_distribution, same_features, 'bayes_variation')

                    for result in group_result:
                        self.results[int(result['ID'])]= result

    def _parse(self, text_tag):
        new_tag = ET.fromstring("<?xml version=\"1.0\" encoding=\"utf-8\"?><TEXT></TEXT>")

        new_tag.attrib['ID'] = text_tag.attrib['ID']
        new_tag.attrib['ENTITY'] = text_tag.attrib['ENTITY']

        title = text_tag.find('TITLE')

        new_title = ET.SubElement(new_tag, 'TITLE')
        new_title.text = title.text

        paragraphs = text_tag.findall('PARAGRAPH')

        for p in paragraphs:
            new_paragraph_tag = ET.SubElement(new_tag, 'PARAGRAPH')
            new_paragraph_tag.attrib['ID'] = p.attrib['ID']

            for elem in p:
                if elem.tag == 'STRING':
                    new_elem = ET.SubElement(new_paragraph_tag, 'STRING')
                    new_elem.text = elem.text
                else:
                    new_paragraph_tag.append(self._parse_reference(elem))

        rough_string = ET.tostring(new_tag, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        xml = reparsed.toprettyxml(indent="\t")
        return xml

    def _parse_reference(self, reference):
        new_reference_tag = ET.Element('REFERENCE')
        new_reference_tag.attrib = copy.copy(reference.attrib)

        models = ['random', 'siddharthan', \
                  'bayes_no_variation', 'bayes_variation']

        reference_id = int(new_reference_tag.attrib['ID'])

        for model in models:
            refex = ET.SubElement(new_reference_tag, 'REFEX')
            refex.attrib['MODEL']= model
            refex.attrib['FORM'] = self.results[reference_id][model]['label']
            refex.text = self.results[reference_id][model]['reference']

        refex = ET.SubElement(new_reference_tag, 'REFEX')
        refex.attrib['MODEL']= 'original'
        refex.attrib['FORM'] = ''
        refex.text = copy.copy(reference.text)

        return new_reference_tag

fdbpedia = '/roaming/tcastrof/names/eacl/name_base.json'
fentities = '/roaming/tcastrof/names/eacl/entities.json'
titles_dir = '/roaming/tcastrof/names/eacl/all_titles.json'
appositives_dir = '/roaming/tcastrof/names/eacl/appositives.json'
vocabulary_dir = '/roaming/tcastrof/names/eacl/stats/voc.json'
mention_dir = '/roaming/tcastrof/names/eacl/mentions'
parsed_dir = '/roaming/tcastrof/names/regnames/parsed'
xmls_dir = '/home/tcastrof/names/ProperName/main/eacl/human_evaluation/data/xmls/'
write_dir = '/home/tcastrof/names/ProperName/main/eacl/human_evaluation/data/processed'

def init():
    print 'Initializing appositives...'
    appositives = json.load(open(appositives_dir))
    print 'Initializing entities_info...'
    entities_info = json.load(open(fentities))

    print 'Initializing titles...'
    titles = json.load(open(titles_dir))
    dbpedia = json.load(open(fdbpedia))
    print 'Initializing vocabulary...'
    # vocabulary = json.load(open(vocabulary_dir))

    print 'Initializing dbpedia...'
    base = {}
    for entity in dbpedia:
        base[entity] = []
        base[entity].extend(dbpedia[entity]['first_names'])
        base[entity].extend(dbpedia[entity]['middle_names'])
        base[entity].extend(dbpedia[entity]['last_names'])

        # insert END token
        base[entity].append('END')

        base[entity].extend(titles)
        base[entity] = list(set(base[entity]))

    return entities_info, base, appositives, dbpedia, []

# filter 1 toke per discourse feature value for the vocabulary. Overcome lack of resourses
def filter_voc(entity, vocabulary):
    result = []

    count = {'np-subj':0, 'np-obj':0, 'subj-det':0, 'givenness_new':0, 'givenness_old':0, 'sentence-givenness_new':0, 'sentence-givenness_old':0}
    for e in vocabulary:
        if e != entity:
            _max = max(count.values())

            f = filter(lambda x: x['syntax'] == 'np-subj', vocabulary[e])[:(_max+1)-count['np-subj']]
            count['np-subj'] += len(f)
            result.extend(f)

            f = filter(lambda x: x['syntax'] == 'np-obj', vocabulary[e])[:(_max+1)-count['np-obj']]
            count['np-obj'] += len(f)
            result.extend(f)

            f = filter(lambda x: x['syntax'] == 'subj-det', vocabulary[e])[:(_max+1)-count['subj-det']]
            count['subj-det'] += len(f)
            result.extend(f)

            f = filter(lambda x: x['givenness'] == 'new', vocabulary[e])[:(_max+1)-count['givenness_new']]
            count['givenness_new'] += len(f)
            result.extend(f)

            f = filter(lambda x: x['givenness'] == 'old', vocabulary[e])[:(_max+1)-count['givenness_old']]
            count['givenness_old'] += len(f)
            result.extend(f)

            f = filter(lambda x: x['sentence-givenness'] == 'new', vocabulary[e])[:(_max+1)-count['sentence-givenness_new']]
            count['sentence-givenness_new'] += len(f)
            result.extend(f)

            f = filter(lambda x: x['sentence-givenness'] == 'old', vocabulary[e])[:(_max+1)-count['sentence-givenness_old']]
            count['sentence-givenness_old'] += len(f)
            result.extend(f)

    return result

if __name__ == '__main__':
    # voc contains only the proper names / titles from DBpedia for each entity
    entities_info, tested_words, appositives, dbpedia, vocabulary = init()

    # filter entities and their references (more than X references and less than Y)
    print 'Filter entities and their references (more than X references and less than Y)'
    references = prep.filter_entities(50, 0, mention_dir)

    xmls = os.listdir(xmls_dir)
    xmls = filter(lambda x: x != '.DS_Store', xmls)

    if not os.path.exists(write_dir):
        os.mkdir(write_dir)

    for xml in xmls:
        print xml
        root = ET.parse(os.path.join(xmls_dir, xml))
        root = root.getroot()
        entity = root.attrib['ENTITY']

        print 'Get appositive...'
        if entity in appositives:
            appositive = appositives[entity]
        else:
            appositive = ''

        print 'Get proper nouns...'
        # Get proper nouns to be tested whether should be included in the reference
        words = tested_words[entity]

        print 'Get training and test vocs...'
        # general_voc = filter_voc(entity, vocabulary)
        # # compute the set of features (vocabulary) for the bayes model
        # content_vocabulary, realization_vocabulary = vocabulary[entity], vocabulary[entity]
        # content_vocabulary.extend(general_voc)

        # compute the set of features (vocabulary) for the bayes model
        content_vocabulary, realization_vocabulary = [], []
        for mention in references[entity]:
            parsed = json.load(open(os.path.join(parsed_dir, mention['fname'])))

            content_data, realization_data = prep.process_tokens(mention, parsed, entity, False)
            content_vocabulary.append(content_data)
            realization_vocabulary.extend(realization_data)

        HumanEvaluation(content_vocabulary, realization_vocabulary, dbpedia, words, appositive, os.path.join(xmls_dir, xml), write_dir)
        print 10 * '-'