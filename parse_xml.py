__author__ = 'thiagocastroferreira'

import copy
import json
import os

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
        self.run()

        self.references = []
        self.results = {}

        self.run()

    def run(self):
        root = ET.parse(self.xml)
        root = root.getroot()
        reference_tags = map(lambda paragraph: paragraph.findall('REFERENCE'), root.findall('PARAGRAPH'))

        self.entity = root.attrib['ENTITY']
        self.references = map(lambda x: x.attrib, reduce(lambda x, y: x+y, reference_tags))

        self._generate()
        new_xml = self._parse(root)

        with open(os.path.join(self.write_dir, root.attrib['ID']+'.xml')) as f:
            f.write(new_xml.encode('utf-8'))

    def _generate(self):
        # check the feature values already processed
        def get_features_visited(mention, features):
            result = copy.copy(features)

            if ('GIVENNESS', mention['GIVENNESS']) not in result:
                result.append(('GIVENNESS', mention['GIVENNESS']))

            if ('SENTENCE-GIVENNESS', mention['SENTENCE-GIVENNESS']) not in result:
                result.append(('SENTENCE-GIVENNESS', mention['SENTENCE-GIVENNESS']))

            if ('SYNCAT', mention['SYNCAT']) not in result:
                result.append(('SYNCAT', mention['SYNCAT']))
            return result

        def bayes_selection(mention, k):
            _features = {
                # 's_e': mention['label'],
                'discourse_se': mention['GIVENNESS'],
                'sentence_se': mention['SENTENCE-GIVENNESS'],
                'syntax_se': mention['SYNCAT']
            }

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
                references[i][name] = { 'label': form, 'reference': realizer[0][0] }

                distribution[form] -= 1
            return references

        features = []
        for mention in self.references:
            aux = get_features_visited(mention, features)
            if aux != features:
                features = copy.copy(aux)

                # Group proper name references from the test fold by feature values
                same_features = filter(lambda x: x['GIVENNESS'] == mention['GIVENNESS'] \
                                                          and x['SENTENCE-GIVENNESS'] == mention['SENTENCE-GIVENNESS'] \
                                                          and x['SYNCAT'] == mention['SYNCAT'], self.references)

                # Bayes model selection
                form_distribution = bayes_selection(mention, None)
                form_distribution_k0 = bayes_selection(mention, 0)
                form_distribution_k2 = bayes_selection(mention, 2)

                # Generate proper names for each group of features
                group_result = []
                for filtered_mention in same_features:
                    result = {'ID': filtered_mention['ID']}

                    # Random model
                    r = self.random_baseline.run(self.entity, filtered_mention['SYNCAT'])
                    result['random'] = { 'label': r[0], 'reference': r[1] }

                    # Siddharthan model
                    r = self.siddharthan.run(self.entity, filtered_mention['GIVENNESS'], filtered_mention['SYNCAT'])
                    result['siddharthan'] = { 'label': r[0], 'reference': r[1] }

                    # Bayes model with no variation (Realization with the most likely referential form)
                    realizer = self.bayes.realizeWithWords(form_distribution[0][0], self.entity, filtered_mention['SYNCAT'], self.words, self.appositive)
                    result['bayes_no_variation'] = { 'label': form_distribution[0][0], 'reference': realizer[0][0] }

                    # Bayes backoff model with no variation (Realization with the most likely referential form)
                    realizer = self.bayes.realizeWithWords(form_distribution_k0[0][0], self.entity, filtered_mention['SYNCAT'], self.words, self.appositive)
                    result['bayes_backoffk0_no_variation'] = { 'label': form_distribution_k0[0], 'reference': realizer[0][0] }

                    # Bayes backoff model with no variation (Realization with the most likely referential form)
                    realizer = self.bayes.realizeWithWords(form_distribution_k2[0][0], self.entity, filtered_mention['SYNCAT'], self.words, self.appositive)
                    result['bayes_backoffk2_no_variation'] = { 'label': form_distribution_k2[0], 'reference': realizer[0][0] }

                    group_result.append(result)

                # Generate proper names with individual variation in the for choice
                group_result = bayes_variation(group_result, form_distribution, same_features, 'bayes_variation')
                group_result = bayes_variation(group_result, form_distribution_k0, same_features, 'bayes_backoffk0_variation')
                group_result = bayes_variation(group_result, form_distribution_k2, same_features, 'bayes_backoffk2_variation')

                for result in group_result:
                    self.results[result['ID']]= result

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
                    new_paragraph_tag.append(self.process_reference(elem))

        rough_string = ET.tostring(new_tag, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        xml = reparsed.toprettyxml(indent="\t")
        return xml

    def _parse_reference(self, reference):
        new_reference_tag = ET.Element('REFERENCE')
        new_reference_tag.attrib = reference.attrib

        models = ['random', 'siddharthan', \
                  'bayes_no_variation', 'bayes_variation', \
                  'bayes_backoffk0_no_variation', 'bayes_backoffk0_variation', \
                  'bayes_backoffk2_no_variation', 'bayes_backoffk2_variation']

        reference_id = new_reference_tag.attrib['ID']

        for model in models:
            refex = ET.SubElement(new_reference_tag, 'REFEX')
            refex.attrib['MODEL']= model
            refex.attrib['FORM'] = self.results[reference_id][model]['label']
            refex.text = self.references[reference_id][model]['reference']

        refex = ET.SubElement(new_reference_tag, 'REFEX')
        refex.attrib['MODEL']= 'original'
        refex.attrib['FORM'] = ''
        refex.text = reference.text

        return new_reference_tag

fdbpedia = '/roaming/tcastrof/names/eacl/name_base.json'
fentities = '/roaming/tcastrof/names/eacl/entities.json'
titles_dir = '/roaming/tcastrof/names/eacl/titles.json'
appositives_dir = '/roaming/tcastrof/names/eacl/appositives.json'
vocabulary_dir = '/roaming/tcastrof/names/eacl/stats/voc.json'

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
    vocabulary = json.load(open(vocabulary_dir))

    print 'Initializing dbpedia...'
    base = {}
    for entity in dbpedia:
        base[entity] = []
        base[entity].extend(dbpedia[entity]['first_names'])
        base[entity].extend(dbpedia[entity]['middle_names'])
        base[entity].extend(dbpedia[entity]['last_names'])

        # insert END token
        base[entity].append('END')

        if entity in titles:
            base[entity].extend(titles[entity])
        base[entity] = list(set(base[entity]))

    return entities_info, base, appositives, dbpedia, vocabulary

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

    xmls = os.listdir(xmls_dir)

    if not os.path.exists(write_dir):
        os.mkdir(write_dir)

    for xml in xmls:
        root = ET.parse(os.path.join(xmls_dir, xml))
        entity = root.attrib['ENTITY']

        if entity in appositives:
            appositive = appositives[entity]
        else:
            appositive = ''

        # Get proper nouns to be tested whether should be included in the reference
        words = tested_words[entity]

        general_voc = filter_voc(entity, vocabulary)
        # compute the set of features (vocabulary) for the bayes model
        content_vocabulary, realization_vocabulary = vocabulary[entity], vocabulary[entity]
        content_vocabulary.extend(general_voc)

        HumanEvaluation(content_vocabulary, realization_vocabulary, dbpedia, words, appositive, xml, write_dir)
        print 10 * '-'