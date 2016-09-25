__author__ = 'thiagocastroferreira'

import copy
import operator
from main.eacl import training, settings

class Bayes(object):
    def __init__(self, train_set_content, train_set_realization, bigram):
        self.train_set_content = train_set_content
        self.train_set_realization = train_set_realization
        self.bigram = bigram
        self.train_content()
        self.train_realization()

    def train_content(self):
        self.clf_content, self.laplace_content = training.run_content(self.train_set_content)

    def train_realization(self):
        self.clf_realization = training.run_realization(self.train_set_realization, self.bigram)

    def select_content(self, features, entity):
        def calc_prob(s):
            # PRIORI
            f = filter(lambda x: x[1] == entity, self.clf_content['s_e'])
            dem = sum(map(lambda x: self.clf_content['s_e'][x], f))

            f = filter(lambda x: x[0] == s, f)
            num = sum(map(lambda x: self.clf_content['s_e'][x], f))

            prob = (float(num+1) / (dem+self.laplace_content['s_e']))

            # POSTERIORI
            for feature in features:
                f = filter(lambda x: x[1] == s and x[2] == entity, self.clf_content[feature])
                dem = sum(map(lambda x: self.clf_content[feature][x], f))

                f = filter(lambda x: x[0] == features[feature], f)
                num = sum(map(lambda x: self.clf_content[feature][x], f))

                prob = prob * (float(num+1) / (dem+self.laplace_content[feature]))
            return prob

        probabilities = dict(map(lambda s: (s, 0), settings.labels))

        for form in probabilities:
            probabilities[form] = calc_prob(form)

        # Frequency distribution
        total = sum(probabilities.values())
        for form in probabilities:
            probabilities[form] = float(probabilities[form]) / total

        probabilities = sorted(probabilities.items(), key=operator.itemgetter(1))
        probabilities.reverse()

        return probabilities

    def select_content_backoff(self, features, entity, K):
        def calc_prob(s):
            # PRIORI
            f = filter(lambda x: x[1] == entity, self.clf_content['s_e'])
            dem = sum(map(lambda x: self.clf_content['s_e'][x], f))

            f = filter(lambda x: x[0] == s, f)
            num = sum(map(lambda x: self.clf_content['s_e'][x], f))

            if num <= K:
                f = self.clf_content['s'].keys()
                dem = sum(map(lambda x: self.clf_content['s'][x], f))

                f = filter(lambda x: x == s, f)
                num = sum(map(lambda x: self.clf_content['s'][x], f))

                prob = (float(num+1) / (dem+self.laplace_content['s_e']))
            else:
                prob = float(num) / dem

            # POSTERIORI
            for feature in features:
                f = filter(lambda x: x[1] == s and x[2] == entity, self.clf_content[feature])
                dem = sum(map(lambda x: self.clf_content[feature][x], f))

                f = filter(lambda x: x[0] == features[feature], f)
                num = sum(map(lambda x: self.clf_content[feature][x], f))

                if num <= K:
                    feat = feature[:-1]

                    f = filter(lambda x: x[1] == s, self.clf_content[feat])
                    dem = sum(map(lambda x: self.clf_content[feat][x], f))

                    f = filter(lambda x: x[0] == features[feature], f)
                    num = sum(map(lambda x: self.clf_content[feat][x], f))

                    prob = prob * (float(num+1) / (dem+self.laplace_content[feature]))
                else:
                    prob = prob * (float(num)/dem)
            return prob

        probabilities = dict(map(lambda s: (s, 0), settings.labels))

        for form in probabilities:
            probabilities[form] = calc_prob(form)

        # Frequency distribution
        total = sum(probabilities.values())
        for form in probabilities:
            probabilities[form] = float(probabilities[form]) / total

        probabilities = sorted(probabilities.items(), key=operator.itemgetter(1))
        probabilities.reverse()

        return probabilities

    def _beam_search(self, names, words, form, entity, word_freq, n=5):
        def calc_prob(gram):
            prob = 0
            f = filter(lambda x: x[1] == gram[1] and x[2] == form and x[3] == entity, self.clf_realization['w_wm1fe'])
            dem = sum(map(lambda x: self.clf_realization['w_wm1fe'][x], f))

            if dem != 0:
                f = filter(lambda x: x[0] == gram[0], f)
                num = sum(map(lambda x: self.clf_realization['w_wm1fe'][x], f))
                prob = float(num) / dem

            return prob

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

        # Stop criteria: prediction of END symbol
        # or the beam search still the same from the last recursion
        # or a proper name bigger than 5 is predicted or 0 probabilities
        if (names.keys() == _names.keys()) \
                or len(filter(lambda name: len(name) > 5, _names.keys())) > 0 \
                or set(_names.values()) == set([0]):
            return _names
        else:
            return self._beam_search(_names, words, form, entity, word_freq, n)

    def realize(self, form, entity, syntax, word_freq, appositive):
        words = map(lambda x: x[1], filter(lambda x: x[0] == entity, self.clf_realization['e_w']))

        names = {('*', ):0}
        result = self._beam_search(names, words, form, entity, word_freq, 1)

        names = []
        for name in result:
            surface = ' '.join(name[1:-1])

            if syntax == 'subj-det' and (surface[-2:] != '\'s' or surface[-1] != '\''):
                if surface[-1] == 's':
                    surface = surface + '\''
                else:
                    surface = surface + '\'s'
            if '+a' in form:
                surface = surface + ', ' + appositive
            names.append((surface, result[name]))
        return names

    # Drop the less frequent attribute of the form
    def _backoff(self, form, entity):
        elems = []
        if '+f' in form:
            elems.append('+f')
        if '+m' in form:
            elems.append('+m')
        if '+l' in form:
            elems.append('+l')
        if '+t' in form:
            elems.append('+t')
        if '+a' in form:
            elems.append('+a')

        keys = filter(lambda x: x[0] in elems and x[1] == entity, self.clf_content['elem_p'])
        aux = dict(map(lambda x: (x[0], self.clf_content['elem_p'][x]), keys))

        for e in elems:
            if e not in aux:
                aux[e] = 0

        elem = sorted(aux.items(), key=operator.itemgetter(1))
        form = str(form).replace(elem[0][0], '')
        return form

    # Realization with only the words present in the proper name knowledge base
    def realizeWithWords(self, form, entity, syntax, words, appositive):
        word_freq = {}

        # Backoff the less frequent attribute until find a realization or the realization has only one form
        names = {('*', ):0}
        result = self._beam_search(names, words, form, entity, word_freq, 1)
        print 'FIRST', form, result
        while result[result.keys()[0]] == 0 and len(form) > 2:
            form = self._backoff(form, entity)
            result = self._beam_search(names, words, form, entity, word_freq, 1)
            print 'NEW', form, result

        names = []
        for name in result:
            surface = ' '.join(name[1:-1])

            if syntax == 'subj-det' and (surface[-2:] != '\'s' or surface[-1] != '\''):
                if surface[-1] == 's':
                    surface = surface + '\''
                else:
                    surface = surface + '\'s'
            if '+a' in form:
                surface = surface + ', ' + appositive
            names.append((surface, result[name]))
        return names