__author__ = 'thiagocastroferreira'

import copy
import operator
from .. import training, settings

class Bayes(object):
    def __init__(self, train_set, bigram):
        self.train_set = train_set
        self.bigram = bigram
        self.train()

    def train(self):
        self.clf, self.laplace = training.run(self.train_set, self.bigram, 'std')

    def select_content(self, features, entity):
        def calc_prob(s):
            # PRIORI
            f = filter(lambda x: x[1] == entity, self.clf['content']['s_e'])
            dem = sum(map(lambda x: self.clf['content']['s_e'][x], f))

            f = filter(lambda x: x[0] == s, f)
            num = sum(map(lambda x: self.clf['content']['s_e'][x], f))

            prob = (float(num+1) / (dem+self.laplace['content']['s_e']))

            # POSTERIORI
            for feature in features:
                f = filter(lambda x: x[1] == s and x[2] == entity, self.clf['content'][feature])
                dem = sum(map(lambda x: self.clf['content'][feature][x], f))

                f = filter(lambda x: x[0] == features[feature], f)
                num = sum(map(lambda x: self.clf['content'][feature][x], f))

                prob = prob * (float(num+1) / (dem+self.laplace['content'][feature]))
            return prob

        probabilities = dict(map(lambda s: (s, 0), settings.labels))

        for s in probabilities:
            probabilities[s] = calc_prob(s)

        return probabilities

    def _beam_search(self, names, words, s, entity, word_freq, n=5):
        def calc_prob(gram):
            # PRIORI
            f = filter(lambda x: x[1] == gram[1] and x[2] == entity, self.clf['realization']['w_e'])
            dem = sum(map(lambda x: self.clf['realization']['w_e'][x], f))

            f = filter(lambda x: x[0] == gram[0], f)
            num = sum(map(lambda x: self.clf['realization']['w_e'][x], f))

            # compute the penalty by the frequency of the word in the sentence
            if gram[0] in word_freq:
                penalty = float(1) / (word_freq[gram[0]] + 1)
            else:
                penalty = 1
            priori = ((float(num+1) / (dem+self.laplace['realization']['w_e']))) * penalty

            # POSTERIORI
            f = filter(lambda x: x[1] == gram[0] and x[2] == gram[1] and x[3] == entity, self.clf['realization']['s_we'])
            dem = sum(map(lambda x: self.clf['realization']['s_we'][x], f))

            f = filter(lambda x: x[0] == s, f)
            num = sum(map(lambda x: self.clf['realization']['s_we'][x], f))

            posteriori = (float(num+1) / (dem+self.laplace['realization']['s_we']))
            return priori * posteriori

        # prunning the tree
        def prune(candidates):
            names = sorted(candidates.items(), key=operator.itemgetter(1))
            names.reverse()
            return dict(names[:n])

        candidates = {}

        for name, prob in names.iteritems():
            w_tm1 = name[-1]
            if w_tm1 == 'END':
                candidates[name] = prob
            else:
                # just consider words that are not in the proper name yet
                for w_t in filter(lambda x: x not in name, words):
                    _name = copy.copy(list(name))
                    _name.append(w_t)
                    _name = tuple(_name)

                    _prob = calc_prob((w_t, w_tm1))

                    if w_tm1 == '*' and prob == 0:
                        candidates[_name] = _prob
                    else:
                        candidates[_name] = prob * _prob

        _names = prune(candidates)

        f = set(_names.values())
        # Stop criteria: prediction of END symbol or the beam search still the same from the last recursion or a proper name bigger than 5 is predicted
        if ('END' in f and len(f) == 1) or (names.keys() == _names.keys()) or len(filter(lambda name: len(name) > 5, _names.keys())) > 0:
            return _names
        else:
            return self._beam_search(_names, words, s, entity, word_freq, n)

    def realize(self, s, entity, word_freq):
        words = map(lambda x: x[1], filter(lambda x: x[0] == entity, self.clf['e_w']))

        names = {('*', ):0}
        return self._beam_search(names, words, s, entity, word_freq, 1)