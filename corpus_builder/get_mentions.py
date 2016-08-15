__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 12/04/2016
Description:
    Main script from the code. It aims to find mentions in the texts from the corpus.
    It only selects the mentions described in the Wikilinks corpus. In case you want all the references in the text,
    check get_all_mentions.py
"""

import json
import re

import corpus_builder.name_variation as nv

from nltk.metrics.distance import edit_distance

def find_mentions(corefs={}, variations=[], sentences=[]):
    candidates = []
    for coref in corefs:
        isFound = False
        for mention in corefs[coref]:
            tokens = sentences[mention['sentNum']-1]['tokens'][mention['startIndex']-1:mention['endIndex']-1]

            # find the number of proper nouns in the mention
            proper = filter(lambda x: x['pos'] == 'NNP', tokens)
            num = 0
            for token in proper:
                if token['word'].lower() in variations:
                    num += 1
                if num == len(proper):
                    isFound = True
                    break
            if isFound:
                candidates.extend(corefs[coref])
                break

    return candidates

def clean(mentions=[], sentences=[]):
    results = []

    # remove references that overlap
    for mention in mentions:
        f = filter(lambda x: x != mention \
                             and x['sentNum'] == mention['sentNum'] \
                             and x['startIndex'] >= mention['startIndex'] \
                             and x['endIndex'] <= mention['endIndex'], mentions)
        if len(f) == 0:
            # Include a proper name as mention only if there is a PERSON named entity
            if mention['type'] != 'PROPER':
                results.append(mention)
            else:
                ner = map(lambda x: x['ner'], sentences[mention['sentNum']-1]['tokens'][mention['startIndex']-1:mention['endIndex']-1])
                if 'PERSON' in ner:
                    results.append(mention)

    return results

def classify(mentions = [], dbpedia = {}, sentences = []):
    def _classify_nominals(name):
        tokens = sentences[name['sentNum']-1]['tokens'][name['startIndex']-1:name['endIndex']-1]

        # get previous tokens to check for titles
        title_check = []
        if name['startIndex'] > 1:
            prev_token = sentences[name['sentNum']-1]['tokens'][name['startIndex']-2]
            title_check.insert(0, prev_token)

            if name['startIndex'] > 2:
                prev_token = sentences[name['sentNum']-1]['tokens'][name['startIndex']-3]
                title_check.insert(0, prev_token)
        title_check.extend(tokens)
        name['text_prevTokens'] = ' '.join(map(lambda x: x['originalText'], title_check))

        # Check title
        m = re.match("M(r.*|s.*|rs.*)\s", name['text'])
        if m != None:
            name['has_title'] = True
            name['titles'] = [m.group(0)]
            aux = re.sub("M(r.*|s.*|rs.*)\s", "", name['text'])
        else:
            name['titles'] = filter(lambda x: x['ner'] == 'TITLE', title_check)
            name['has_title'] = len(name['titles']) > 0

            aux = name['text']
            for title in name['titles']:
                aux = aux.replace(title['originalText'], '')

        # Check first name
        for first in dbpedia['first_names']:
            if str(first).lower() in str(aux).lower():
                name['has_firstName'] = True
                break

        # Check middle name
        for middle in dbpedia['middle_names']:
            if str(middle).lower() in str(aux).lower():
                name['has_middleName'] = True
                break

        # Check last name
        for last in dbpedia['last_names']:
            if str(last).lower() in str(aux).lower():
                name['has_lastName'] = True
                break

        # Check adjective
        if 'JJ' in map(lambda x: x['pos'], tokens):
            name['has_adjective'] = True

        # Check classes extracted from dbpedia
        for name_type in ['surnames', 'givenNames', 'birthNames', 'foaf_names', 'dbp_names']:
            for candidate in dbpedia[name_type]:
                # Threshold of 3 for the string distance
                if edit_distance(str(aux).lower(), str(candidate).lower()) < 3:
                    name['name_type'].append(name_type)

        # Label the reference according to the attribute set (Attributes: title, first, middle, last, appositive)
        attribute_set = ''
        if name['has_title']:
            attribute_set = attribute_set + '+t'

        if name['has_firstName']:
            attribute_set = attribute_set + '+f'

        if name['has_middleName']:
            attribute_set = attribute_set + '+m'

        if name['has_lastName']:
            attribute_set = attribute_set + '+l'

        if name['has_appositive']:
            attribute_set = attribute_set + '+a'
        name['label'] = attribute_set
        return name

    # initialize variables
    for mention in mentions:
        mention['has_title'] = False
        mention['has_firstName'] = False
        mention['has_middleName'] = False
        mention['has_lastName'] = False
        mention['has_appositive'] = False
        mention['has_adjective'] = False

        mention['appositive'] = None
        mention['name_type'] = []

    results = []
    # treat pronominal references
    pronominal = filter(lambda x: x['type'] == 'PRONOMINAL', mentions)
    pronominal = filter(lambda x: str(x['text']).lower() \
                     not in ['they', 'their', 'theirs', 'themselves', \
                             'we', 'our', 'ours', 'ourselves', \
                             'it', 'its', 'itself', \
                             'this', 'these', 'that', 'those'], pronominal)

    # TO DO: remove wrong pronouns
    results.extend(pronominal)

    # treat proper names
    names = filter(lambda x: x['type'] == 'PROPER', mentions)
    for name in names:
        # TO DO: remove wrong names
        results.append(_classify_nominals(name))

    nominals = filter(lambda x: x['type'] == 'NOMINAL', mentions)
    for nominal in nominals:
        deps = filter(lambda x: nominal['startIndex'] <= x['dependent'] <= nominal['endIndex'] \
                                and x['dep'] == 'appos', sentences[nominal['sentNum']-1]['basic-dependencies'])
        for dep in deps:
            governors = filter(lambda x: nominal != x and x['sentNum'] == nominal['sentNum'] \
                                         and x['startIndex'] <= dep['governor'] <= x['endIndex'], results)
            for governor in governors:
                results[results.index(governor)]['has_appositive'] = True
                results[results.index(governor)]['appositive'] = nominal
            if len(governors) == 0:
                results.append(nominal)
    return results

def extract_status(mentions, num_sent):
    results = []

    first = 1
    for i in range(1, num_sent+1):
        fmentions = filter(lambda x: str(x['sentNum']) == str(i), mentions)

        indexes = map(lambda x: int(x['startIndex']), fmentions)
        indexes.sort()

        pos = 1
        for idx in indexes:
            fmention = filter(lambda x: x['startIndex'] == idx, fmentions)[0]

            if first == 1:
                fmention['givenness'] = 'new'
            else:
                fmention['givenness'] = 'old'

            if pos == 1:
                fmention['sentence-givenness'] = 'new'
            else:
                fmention['sentence-givenness'] = 'old'
            first += 1
            pos += 1

            results.append(fmention)

    return results

def extract_syntax(mentions, sentences):
    for mention in mentions:
        deps = filter(lambda x: mention['startIndex'] <= x['dependent'] < mention['endIndex'] \
                                or mention['startIndex'] <= x['governor'] < mention['endIndex'], sentences[mention['sentNum']-1]['basic-dependencies'])

        type = map(lambda x: x['dep'], deps)
        if 'nsubj' in type or 'nsubjpass' in type:
            mention['syntax'] = 'np-subj'

            dep = filter(lambda x: x['dep'] in ['nsubj', 'nsubjpass'], deps)[0]
            mention['syntax-governor'] = [dep['governor'], dep['governorGloss']]
        elif 'dobj' in type or 'iobj' in type:
            mention['syntax'] = 'np-obj'

            dep = filter(lambda x: x['dep'] in ['dobj', 'iobj'], deps)[0]
            mention['syntax-governor'] = [dep['governor'], dep['governorGloss']]
        elif 'nmod:poss' in type or 'compound' in type:
            mention['syntax'] = 'subj-det'

            dep = filter(lambda x: x['dep'] in ['nmod:poss', 'compound'], deps)[0]
            mention['syntax-governor'] = [dep['governor'], dep['governorGloss']]
        else:
            mention['syntax'] = ''
            mention['syntax-governor'] = []

    # only return the mentions with defined syntax
    return filter(lambda x: x['syntax'] != '', mentions)


def run(fname, dbpedia):
    r = json.load(open(fname))

    variations = nv.get_variations_db(dbpedia_names=dbpedia)
    mentions = find_mentions(r['corefs'], variations, r['sentences'])
    mentions = classify(mentions, dbpedia, r['sentences'])
    mentions = clean(mentions, r['sentences'])
    mentions = extract_syntax(mentions, r['sentences'])
    mentions = extract_status(mentions, len(r['sentences']))

    return mentions