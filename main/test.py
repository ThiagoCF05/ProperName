__author__ = 'thiagocastroferreira'

import json
import os

mention_dir = '/roaming/tcastrof/names/eacl/mentions'
write_dir = '/roaming/tcastrof/names/eacl/entities_50.json'

# filter entities with more than N mentions and process the mentions
def filter_entities(N_min, N_max, mention_dir):
    '''
    :param N: only entities with more than N mentions should be considered
    :param mention_dir: directory where the mention files are present
    :return:
    '''
    result = {}

    files = os.listdir(mention_dir)
    for i, fname in enumerate(files):
        print i, fname, '\r',
        mentions = json.load(open(os.path.join(mention_dir, fname)))

        # Exclude this entity from the set
        entities = filter(lambda x: x != 'http://en.wikipedia.org/wiki/Whoopi_Goldberg', mentions)
        for entity in entities:
            if entity not in result:
                result[entity] = []
            for mention in filter(lambda mention: mention['type'] == 'PROPER', mentions[entity]):
                mention['fname'] = fname
                result[entity].append(mention)
    if N_max == 0:
        return dict(map(lambda x: (x, result[x]), filter(lambda e: len(result[e]) >= N_min, result.keys())))
    else:
        return dict(map(lambda x: (x, result[x]), filter(lambda e: N_min <= len(result[e]) <= N_max, result.keys())))

if __name__ == '__main__':
    references = filter_entities(50, 0, mention_dir)

    json.dump(references.keys(), open(write_dir, 'w'), indent=4, separators=(',', ': '))

