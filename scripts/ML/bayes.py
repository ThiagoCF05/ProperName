__author__ = 'thiagocastroferreira'

import json
import extractors.count_words as count
import operator
import copy

def beam(names, counts, features, laplace, words, entity):
    candidates = {}
    for name, prob in names.iteritems():
        prev = name[-1]
        if prev == 'END':
            candidates[name] = prob
        else:
            for word in filter(lambda x: x not in name, words):
                _name = copy.copy(list(name))
                _name.append(word)
                _name = tuple(_name)

                dem = filter(lambda x: x[0] == prev and x[2] == entity, counts['wt_wtm1'])
                num = len(filter(lambda x: x[1] == word and x[2] == entity, dem))
                posteriori = float(num+1) / (len(dem)+laplace['wt_wtm1'])

                for feature in filter(lambda x: x != 'wt_wtm1', features.keys()):
                    dem = filter(lambda x: x[1] == word and x[2] == entity, counts[feature])
                    num = filter(lambda x: x[0] == features[feature] and x[2] == entity, dem)
                    posteriori = posteriori * (float(len(num)+1) / (len(dem)+laplace[feature]))

                if prev == '*' and prob == 0:
                    candidates[_name] = posteriori
                else:
                    candidates[_name] = prob * posteriori

    # prunning the tree
    result = sorted(candidates.items(), key=operator.itemgetter(1))
    result.reverse()
    result = dict(result[:10])
    # normalization
    norm = sum(result.values())
    for k in result:
        result[k] = float(result[k]) / norm

    f = set(result.values())
    if ('END' in f and len(f) == 1) or (names.keys() == result.keys()) or len(filter(lambda name: len(name) > 5, result.keys())) > 0:
        return result
    else:
        return beam(result, counts, features, laplace, words, entity)

def run():
    vocabulary = json.load(open('stats/vocabulary.json'))
    entities = set(map(lambda x: x['entity'], vocabulary))

    # list(entities)[:50]
    vocabulary = filter(lambda x: x['entity'] in list(entities)[50:70], vocabulary)

    counts = count.run(vocabulary, entities)
    words = set(map(lambda x: x['word'], vocabulary))

    for entity in list(entities)[50:70]:
        print entity
        for givenness in ['new', 'old']:
            for sgivenness in ['new', 'old']:
                # for syntax in ['np-subj', 'np-obj', 'subj-det']:
                features = {
                    'wt_wtm1': '*',
                    'dg_w': givenness,
                    'sg_w': sgivenness,
                    # 'e_w': entity,
                    # 's_w': syntax
                }

                laplace = {
                    'wt_wtm1': len(words),
                    'dg_w': 2,
                    'sg_w': 2,
                    # 's_w': 3
                }

                names = {('*', ):0}
                # select as vocabulary words if frequency higher than 10 for the entity references
                fwords = [k[1] for k, v in counts['e_w'].iteritems() if k[0] == entity and v > 5]
                try:
                    results = beam(names, counts, features, laplace, fwords, entity)
                    results = sorted(results.items(), key=operator.itemgetter(1))
                    results.reverse()
                    print givenness, sgivenness
                    for k, v in results:
                        print k, v
                    print 10 * '-'
                except:
                    pass
        print '\n'

if __name__ == '__main__':
    run()