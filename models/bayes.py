__author__ = 'thiagocastroferreira'

import json
import operator
import copy

import ML.extractors.count as count


def unigram(n_t, n_tm1, counts, features, laplace, entity):
    f = filter(lambda x: x[0] == n_tm1 and x[2] == entity, counts['wt_wtm1'])
    dem = sum(map(lambda x: counts['wt_wtm1'][x], f))

    f = filter(lambda x: x[1] == n_t, f)
    num = sum(map(lambda x: counts['wt_wtm1'][x], f))

    posteriori = float(num+1) / (dem+laplace['wt_wtm1'])

    for feature in filter(lambda x: x != 'wt_wtm1', features.keys()):
        f = filter(lambda x: x[1] == n_t and x[2] == entity, counts[feature])
        dem = sum(map(lambda x: counts[feature][x], f))

        f = filter(lambda x: x[0] == features[feature], f)
        num = sum(map(lambda x: counts[feature][x], f))

        posteriori = posteriori * (float(num+1) / (dem+laplace[feature]))
    return posteriori

def bigram(g_t, counts, features, laplace, entity):
    f = filter(lambda x: x[0] == g_t[1] and x[2] == entity, counts['wt_wtm1'])
    dem = sum(map(lambda x: counts['wt_wtm1'][x], f))

    f = filter(lambda x: x[1] == g_t[0], f)
    num = sum(map(lambda x: counts['wt_wtm1'][x], f))

    posteriori = float(num+1) / (dem+laplace['wt_wtm1'])

    for feature in filter(lambda x: x != 'wt_wtm1', features.keys()):
        f = filter(lambda x: x[1] == g_t and x[2] == entity, counts[feature])
        dem = sum(map(lambda x: counts[feature][x], f))

        f = filter(lambda x: x[0] == features[feature], f)
        num = sum(map(lambda x: counts[feature][x], f))

        posteriori = posteriori * (float(num+1) / (dem+laplace[feature]))
    return posteriori

def beam(names, counts, features, laplace, words, entity):
    candidates = {}
    for name, prob in names.iteritems():
        w_tm1 = name[-1]
        if w_tm1 == 'END':
            candidates[name] = prob
        else:
            for w_t in filter(lambda x: x not in name, words):
                _name = copy.copy(list(name))
                _name.append(w_t)
                _name = tuple(_name)

                posteriori = bigram((w_t, w_tm1), counts, features, laplace, entity)

                if w_tm1 == '*' and prob == 0:
                    candidates[_name] = posteriori
                else:
                    candidates[_name] = prob * posteriori

    # prunning the tree
    result = sorted(candidates.items(), key=operator.itemgetter(1))
    result.reverse()
    result = dict(result[:1])

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
    vocabulary = json.load(open('stats/word2voc.json'))
    entities = set(map(lambda x: x['entity'], vocabulary))

    test = ['http://en.wikipedia.org/wiki/Arthur_Conan_Doyle', 'http://en.wikipedia.org/wiki/Napoleon']

    vocabulary = filter(lambda x: x['entity'] in test, vocabulary)

    counts = count.run(vocabulary, entities, True)
    # words = set(map(lambda x: x['word'], vocabulary))

    for entity in test:
        print entity
        # print '\n'
        # for k in filter(lambda x: x[2] == entity, counts['dg_w'].keys()):
        #     print k, counts['dg_w'][k]
        # print '\n'
        # for k in filter(lambda x: x[2] == entity, counts['sg_w'].keys()):
        #     print k, counts['sg_w'][k]
        # print '\n'
        # for k in filter(lambda x: x[2] == entity, counts['s_w'].keys()):
        #     print k, counts['s_w'][k]
        # print '\n'
        # for k in filter(lambda x: x[2] == entity, counts['wt_wtm1'].keys()):
        #     print k, counts['wt_wtm1'][k]
        # print 10 * '-'
        for givenness in ['new', 'old']:
            for sgivenness in ['new', 'old']:
                for syntax in ['np-subj', 'np-obj', 'subj-det']:
                    # select as vocabulary words if frequency higher than 10 for the entity references
                    fwords = [k[1] for k, v in counts['e_w'].iteritems() if k[0] == entity and v > 2]

                    features = {
                        'wt_wtm1': '*',
                        'dg_w': givenness,
                        'sg_w': sgivenness,
                        # 'e_w': entity,
                        's_w': syntax
                    }

                    laplace = {
                        'wt_wtm1': len(fwords),
                        'dg_w': 2,
                        'sg_w': 2,
                        's_w': 3
                    }

                    names = {('*', ):0}
                    try:
                        results = beam(names, counts, features, laplace, fwords, entity)
                        results = sorted(results.items(), key=operator.itemgetter(1))
                        results.reverse()
                        if givenness == 'new' and sgivenness == 'old':
                            pass
                        else:
                            print givenness, sgivenness, syntax
                            for k, v in results:
                                print k, v
                            print 10 * '-'
                    except:
                        pass
        print '\n'

if __name__ == '__main__':
    run()