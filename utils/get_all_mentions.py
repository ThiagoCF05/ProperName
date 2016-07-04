__author__ = 'thiagocastroferreira'

import json
import loader
import name_variation as nv

def find_core_mentions(corefs={}, variations=[], sentences=[]):
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
                candidates.extend(coref)
                break

    return candidates

def get_variations():
    entities = loader.get_entities_indir('/roaming/tcastrof/names/entities')

    variations = {}
    for first in entities:
        variations[first] = {}
        for e in entities[first]:
            variations[first][e] = nv.get_variations_db(e)
    return variations

def run(fname, dbpedia, url):
    variations = get_variations()

    r = json.load(open(fname))
    variations = nv.get_variations_db(dbpedia_names=dbpedia)

    candidates = find_core_mentions(r['corefs'], variations, r['sentences'])

    entities = { url:candidates }
    