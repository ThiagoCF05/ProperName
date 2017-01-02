__author__ = 'thiagocastroferreira'

import copy
import operator
import nltk

settings_labels = [
    '+f',
    '+m',
    '+l',
    '+t+f',
    '+t+m',
    '+t+l',
    '+f+m',
    '+f+l',
    '+f+a',
    '+m+l',
    '+m+a',
    '+l+a',
    '+t+f+m',
    '+t+f+l',
    '+t+f+a',
    '+t+m+l',
    '+t+m+a',
    '+t+l+a',
    '+f+m+l',
    '+f+m+a',
    '+f+l+a',
    '+m+l+a',
    '+t+f+m+l',
    '+t+f+m+a',
    '+t+f+l+a',
    '+t+m+l+a',
    '+f+m+l+a',
    '+t+f+m+l+a',
    ]

settings_features = {
    'syntax':['np-subj', 'np-obj', 'subj-det'],
    'givenness':['new', 'old'],
    'sentence-givenness':['new', 'old']
}

class BayesTraining(object):
    # calculate count(f)
    def f(self, voc):
        grams = map(lambda x: x['label'], voc)
        return dict(nltk.FreqDist(grams))

    # calculate count(f | p)
    def f_given_p(self, voc):
        grams = map(lambda x: (x['label'], x['entity']), voc)
        return dict(nltk.FreqDist(grams))

    # calculate givenness count(dg | f)
    def discourse_given_f(self, voc):
        grams = map(lambda x: (x['givenness'], x['label']), voc)
        return dict(nltk.FreqDist(grams))

    # calculate givenness count(dg | f, p)
    def discourse_given_fp(self, voc):
        grams = map(lambda x: (x['givenness'], x['label'], x['entity']), voc)
        return dict(nltk.FreqDist(grams))

    # calculate sentence givenness count(sg | f)
    def sentence_given_f(self, voc):
        grams = map(lambda x: (x['sentence-givenness'], x['label']), voc)
        return dict(nltk.FreqDist(grams))

    # calculate sentence givenness count(sg | f, p)
    def sentence_given_fp(self, voc):
        grams = map(lambda x: (x['sentence-givenness'], x['label'], x['entity']), voc)
        return dict(nltk.FreqDist(grams))

    # calculate count(syntax | f)
    def syntax_given_f(self, voc):
        grams = map(lambda x: (x['syntax'], x['label']), voc)
        return dict(nltk.FreqDist(grams))

    # calculate count(syntax | f, p)
    def syntax_given_fp(self, voc):
        grams = map(lambda x: (x['syntax'], x['label'], x['entity']), voc)
        return dict(nltk.FreqDist(grams))

    # REALIZATION
    # calculate count(w | w_m1, f, p)
    def w_given_wm1fp(self, voc, bigram=True):
        if bigram:
            grams = map(lambda x: (x['bigram'][0], x['bigram'][1], x['label'], x['entity']), voc)
        else:
            grams = map(lambda x: (x['word'], x['label'], x['entity']), voc)
        return dict(nltk.FreqDist(grams))

    # form attribute by person
    def elem_given_p(self, voc):
        elem_p = []
        for v in voc:
            for elem in v['label_elems']:
                elem_p.append((elem, v['entity']))
        return dict(nltk.FreqDist(elem_p))

    # calculate entity given w count(p | w)
    def entity_given_w(self, voc):
        grams = map(lambda x: (x['entity'], x['word']), voc)
        return dict(nltk.FreqDist(grams))

    # calculate count(s | w, p)
    def s_given_wp(self, voc, bigram=True):
        if bigram:
            grams = map(lambda x: (x['label'], x['bigram'][0], x['bigram'][1], x['entity']), voc)
        else:
            grams = map(lambda x: (x['label'], x['word'], x['entity']), voc)
        return dict(nltk.FreqDist(grams))

    # calculate entity given w count(w | p)
    def w_given_p(self, voc, bigram=True):
        if bigram:
            grams = map(lambda x: (x['bigram'][0], x['bigram'][1], x['entity']), voc)
        else:
            grams = map(lambda x: (x['word'], x['entity']), voc)
        return dict(nltk.FreqDist(grams))

    def run_content(self, voc):
        # CONTENT SELECTION
        s = self.f(voc)
        s_e = self.f_given_p(voc)
        discourse_se = self.discourse_given_fp(voc)
        sentence_se = self.sentence_given_fp(voc)
        syntax_se = self.syntax_given_fp(voc)
        elem_p = self.elem_given_p(voc)

        discourse_s = self.discourse_given_f(voc)
        sentence_s = self.sentence_given_f(voc)
        syntax_s = self.syntax_given_f(voc)

        train_set = {
            's_e': s_e,
            'discourse_se': discourse_se,
            'sentence_se': sentence_se,
            'syntax_se': syntax_se,
            's': s,
            'discourse_s': discourse_s,
            'sentence_s': sentence_s,
            'syntax_s': syntax_s,
            'elem_p': elem_p
        }

        laplace = {
            's_e': len(settings_labels),
            'discourse_se': len(settings_features['givenness']),
            'sentence_se': len(settings_features['sentence-givenness']),
            'syntax_se': len(settings_features['syntax']),
            }
        return train_set, laplace

    def run_realization(self, voc, bigram=True):
        # REALIZATION
        e_w = self.entity_given_w(voc)
        w_wm1fe = self.w_given_wm1fp(voc, bigram)

        train_set = {
            'e_w': e_w,
            'w_wm1fe': w_wm1fe
        }
        return train_set

class Bayes(object):
    def __init__(self, train_set_content, train_set_realization, bigram):
        training = BayesTraining()
        self.clf_content, self.laplace_content = training.run_content(train_set_content)
        self.clf_realization = training.run_realization(train_set_realization, bigram)

    def select_content(self, D, p):
        def calc_prob(s):
            # PRIORI
            f = filter(lambda x: x[1] == p, self.clf_content['s_e'])
            dem = sum(map(lambda x: self.clf_content['s_e'][x], f))

            f = filter(lambda x: x[0] == s, f)
            num = sum(map(lambda x: self.clf_content['s_e'][x], f))

            prob = (float(num+1) / (dem+self.laplace_content['s_e']))

            # POSTERIORI
            for d in D:
                f = filter(lambda x: x[1] == s and x[2] == p, self.clf_content[d])
                dem = sum(map(lambda x: self.clf_content[d][x], f))

                f = filter(lambda x: x[0] == D[d], f)
                num = sum(map(lambda x: self.clf_content[d][x], f))

                prob = prob * (float(num+1) / (dem+self.laplace_content[d]))
            return prob

        P = dict(map(lambda s: (s, 0), settings_labels))

        for form in P:
            P[form] = calc_prob(form)

        # Frequency distribution
        total = sum(P.values())
        for form in P:
            P[form] = float(P[form]) / total

        P = sorted(P.items(), key=operator.itemgetter(1))
        P.reverse()

        return P

    def select_content_backoff(self, D, p, K):
        def calc_prob(s):
            # PRIORI
            f = filter(lambda x: x[1] == p, self.clf_content['s_e'])
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
            for d in D:
                f = filter(lambda x: x[1] == s and x[2] == p, self.clf_content[d])
                dem = sum(map(lambda x: self.clf_content[d][x], f))

                f = filter(lambda x: x[0] == D[d], f)
                num = sum(map(lambda x: self.clf_content[d][x], f))

                if num <= K:
                    feat = d[:-1]

                    f = filter(lambda x: x[1] == s, self.clf_content[feat])
                    dem = sum(map(lambda x: self.clf_content[feat][x], f))

                    f = filter(lambda x: x[0] == D[d], f)
                    num = sum(map(lambda x: self.clf_content[feat][x], f))

                    prob = prob * (float(num+1) / (dem+self.laplace_content[d]))
                else:
                    prob = prob * (float(num)/dem)
            return prob

        P = dict(map(lambda s: (s, 0), settings_labels))

        for form in P:
            P[form] = calc_prob(form)

        # Frequency distribution
        total = sum(P.values())
        for form in P:
            P[form] = float(P[form]) / total

        P = sorted(P.items(), key=operator.itemgetter(1))
        P.reverse()

        return P

    def _beam_search(self, names, words, form, entity, n=5):
        def calc_prob(gram):
            prob = 0
            if form == '':
                f = filter(lambda x: x[1] == gram[1] and x[3] == entity, self.clf_realization['w_wm1fe'])
            elif form == '-':
                f = filter(lambda x: x[3] == entity, self.clf_realization['w_wm1fe'])
            else:
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
            return self._beam_search(_names, words, form, entity, n)

    def realize(self, form, p, syntax, appositive):
        words = map(lambda x: x[1], filter(lambda x: x[0] == p, self.clf_realization['e_w']))

        # Backoff the less frequent attribute until find a realization or the realization has only one form
        names = {('*', ):0}
        result = self._beam_search(names, words, form, p, 1)
        while result[result.keys()[0]] == 0 and form != '':
            form = self._backoff(form, p)
            result = self._beam_search(names, words, form, p, 1)
        if result[result.keys()[0]] == 0:
            result = self._beam_search(names, words, '-', p, 1)

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

        # Select frequency of the attributes in the form
        keys = filter(lambda x: x[0] in elems and x[1] == entity, self.clf_content['elem_p'])
        aux = dict(map(lambda x: (x[0], self.clf_content['elem_p'][x]), keys))
        for e in elems:
            if e not in aux:
                aux[e] = 0

        # drop the less frequent attribute in the form
        elem = sorted(aux.items(), key=operator.itemgetter(1))
        form = str(form).replace(elem[0][0], '')
        return form

    # Realization with only the words present in the proper name knowledge base
    def realizeWithWords(self, form, p, syntax, words, appositive):
        original_form = copy.copy(form)

        # Backoff the less frequent attribute until find a realization or the realization has only one form
        names = {('*', ):0}
        result = self._beam_search(names, words, form, p, 1)
        while result[result.keys()[0]] == 0 and form != '':
            form = self._backoff(form, p)
            result = self._beam_search(names, words, form, p, 1)
        if result[result.keys()[0]] == 0:
            result = self._beam_search(names, words, '-', p, 1)

        names = []
        for name in result:
            surface = ' '.join(name[1:-1])

            if len(surface) > 0:
                if syntax == 'subj-det' and (surface[-2:] != '\'s' or surface[-1] != '\''):
                    if surface[-1] == 's':
                        surface = surface + '\''
                    else:
                        surface = surface + '\'s'
            if '+a' in original_form:
                surface = surface + ', ' + appositive
            names.append((surface, result[name]))
        return names