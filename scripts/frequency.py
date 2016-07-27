__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 19/04/2016
Description:
    This script aims to compute the corrupted files and the general frequencies of the different proper name labels,
    as well their frequencies by sentence and syntactic position.

    This script should be executed once you collected your results
"""

import os
import json

if __name__ == '__main__':
    fname = '/roaming/tcastrof/names/regnames/report.json'
    d = "/roaming/tcastrof/names/regnames/mentions"

    freq_files = 0
    # corrupted files
    freq_corrupted, corrupted = 0, []
    # no class mentions
    freq_no_class = 0
    # frequency indicators
    freq_mentions, freq_title, freq_first, freq_middle, freq_last, freq_appos = 0, 0, 0, 0, 0, 0

    # combinations => t = title / first = first / m = middle / l = last / a = appositive
    t, first, m, l, a = 0, 0, 0, 0, 0
    t_f, t_m, t_l, t_a, f_m, f_l, f_a, m_l, m_a, l_a = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    t_f_m, t_f_l, t_f_a, t_m_l, t_m_a, t_l_a, f_m_l, f_m_a, f_l_a, m_l_a = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    t_f_m_l, t_f_m_a, t_f_l_a, t_m_l_a, f_m_l_a = 0, 0, 0, 0, 0
    t_f_m_l_a = 0

    # frequency indicators by sentence
    freq_sent = {}
    # frequency indicators by syntax
    freq_syntax = {}
    # frequency indicators by status
    freq_status = {}
    # frequency indicators by sentence status
    freq_sent_status = {}
    # frequency indicators by dbpedia ontology
    freq_given, freq_surnames, freq_birthname = 0, 0, 0
    # size of the reference
    name_size = []

    files = os.listdir(d)

    for f in files:
        print f, '\r',
        freq_files += 1
        try:
            entities = json.load(open(os.path.join(d, f)))
            for e in entities:
                pickle = entities[e]
                names = filter(lambda x: x['type'] == 'PROPER', pickle)

                if len(names) == 0:
                    freq_corrupted += 1
                    corrupted.append(f)
                for name in names:
                    if name['sentNum'] not in freq_sent:
                        freq_sent[name['sentNum']] = {'freq_mentions': 0, 'freq_title': 0, 'freq_first': 0, 'freq_middle': 0, 'freq_last': 0, 'freq_appos': 0, \
                                                      'freq_given': 0, 'freq_surnames': 0, 'freq_birthname': 0, 'freq_no_class': 0, 'name_size':[], \
                                                      't': 0, 'f': 0, 'm': 0, 'l': 0, 'a': 0, \
                                                      't_f': 0, 't_m': 0, 't_l': 0, 't_a': 0, 'f_m': 0, 'f_l': 0, 'f_a': 0, 'm_l': 0, 'm_a': 0, 'l_a': 0, \
                                                      't_f_m': 0, 't_f_l': 0, 't_f_a': 0, 't_m_l': 0, 't_m_a': 0, 't_l_a': 0, 'f_m_l': 0, 'f_m_a': 0, 'f_l_a': 0, 'm_l_a': 0, \
                                                      't_f_m_l': 0, 't_f_m_a': 0, 't_f_l_a': 0, 't_m_l_a': 0, 'f_m_l_a': 0, 't_f_m_l_a': 0}
                    if name['syntax'] not in freq_syntax:
                        freq_syntax[name['syntax']] = {'freq_mentions': 0, 'freq_title': 0, 'freq_first': 0, 'freq_middle': 0, 'freq_last': 0, 'freq_appos': 0, \
                                                       'freq_given': 0, 'freq_surnames': 0, 'freq_birthname': 0, 'freq_no_class': 0, 'name_size':[], \
                                                       't': 0, 'f': 0, 'm': 0, 'l': 0, 'a': 0, \
                                                       't_f': 0, 't_m': 0, 't_l': 0, 't_a': 0, 'f_m': 0, 'f_l': 0, 'f_a': 0, 'm_l': 0, 'm_a': 0, 'l_a': 0, \
                                                       't_f_m': 0, 't_f_l': 0, 't_f_a': 0, 't_m_l': 0, 't_m_a': 0, 't_l_a': 0, 'f_m_l': 0, 'f_m_a': 0, 'f_l_a': 0, 'm_l_a': 0, \
                                                       't_f_m_l': 0, 't_f_m_a': 0, 't_f_l_a': 0, 't_m_l_a': 0, 'f_m_l_a': 0, 't_f_m_l_a': 0}
                    if name['givenness'] not in freq_status:
                        freq_status[name['givenness']] = {'freq_mentions': 0, 'freq_title': 0, 'freq_first': 0, 'freq_middle': 0, 'freq_last': 0, 'freq_appos': 0, \
                                                          'freq_given': 0, 'freq_surnames': 0, 'freq_birthname': 0, 'freq_no_class': 0, 'name_size':[], \
                                                          't': 0, 'f': 0, 'm': 0, 'l': 0, 'a': 0, \
                                                       't_f': 0, 't_m': 0, 't_l': 0, 't_a': 0, 'f_m': 0, 'f_l': 0, 'f_a': 0, 'm_l': 0, 'm_a': 0, 'l_a': 0, \
                                                       't_f_m': 0, 't_f_l': 0, 't_f_a': 0, 't_m_l': 0, 't_m_a': 0, 't_l_a': 0, 'f_m_l': 0, 'f_m_a': 0, 'f_l_a': 0, 'm_l_a': 0, \
                                                       't_f_m_l': 0, 't_f_m_a': 0, 't_f_l_a': 0, 't_m_l_a': 0, 'f_m_l_a': 0, 't_f_m_l_a': 0}
                    if name['sentence-givenness'] not in freq_sent_status:
                        freq_sent_status[name['sentence-givenness']] = {'freq_mentions': 0, 'freq_title': 0, 'freq_first': 0, 'freq_middle': 0, 'freq_last': 0, 'freq_appos': 0, \
                                                                        'freq_given': 0, 'freq_surnames': 0, 'freq_birthname': 0, 'freq_no_class': 0, 'name_size':[], \
                                                                        't': 0, 'f': 0, 'm': 0, 'l': 0, 'a': 0, \
                                                          't_f': 0, 't_m': 0, 't_l': 0, 't_a': 0, 'f_m': 0, 'f_l': 0, 'f_a': 0, 'm_l': 0, 'm_a': 0, 'l_a': 0, \
                                                          't_f_m': 0, 't_f_l': 0, 't_f_a': 0, 't_m_l': 0, 't_m_a': 0, 't_l_a': 0, 'f_m_l': 0, 'f_m_a': 0, 'f_l_a': 0, 'm_l_a': 0, \
                                                          't_f_m_l': 0, 't_f_m_a': 0, 't_f_l_a': 0, 't_m_l_a': 0, 'f_m_l_a': 0, 't_f_m_l_a': 0}

                    freq_mentions += 1
                    freq_syntax[name['syntax']]['freq_mentions'] += 1
                    freq_sent[name['sentNum']]['freq_mentions'] += 1
                    freq_status[name['givenness']]['freq_mentions'] += 1
                    freq_sent_status[name['sentence-givenness']]['freq_mentions'] += 1

                    aux = len(name['text'].split())
                    name_size.append(aux)
                    freq_syntax[name['syntax']]['name_size'].append(aux)
                    freq_sent[name['sentNum']]['name_size'].append(aux)
                    freq_status[name['givenness']]['name_size'].append(aux)
                    freq_sent_status[name['sentence-givenness']]['name_size'].append(aux)

                    if name['has_title']:
                        freq_title += 1
                        freq_sent[name['sentNum']]['freq_title'] += 1
                        freq_syntax[name['syntax']]['freq_title'] += 1
                        freq_status[name['givenness']]['freq_title'] += 1
                        freq_sent_status[name['sentence-givenness']]['freq_title'] += 1
                    if name['has_firstName']:
                        freq_first += 1
                        freq_sent[name['sentNum']]['freq_first'] += 1
                        freq_syntax[name['syntax']]['freq_first'] += 1
                        freq_status[name['givenness']]['freq_first'] += 1
                        freq_sent_status[name['sentence-givenness']]['freq_first'] += 1
                    if name['has_middleName']:
                        freq_middle += 1
                        freq_sent[name['sentNum']]['freq_middle'] += 1
                        freq_syntax[name['syntax']]['freq_middle'] += 1
                        freq_status[name['givenness']]['freq_middle'] += 1
                        freq_sent_status[name['sentence-givenness']]['freq_middle'] += 1
                    if name['has_lastName']:
                        freq_last += 1
                        freq_sent[name['sentNum']]['freq_last'] += 1
                        freq_syntax[name['syntax']]['freq_last'] += 1
                        freq_status[name['givenness']]['freq_last'] += 1
                        freq_sent_status[name['sentence-givenness']]['freq_last'] += 1
                    if name['has_appositive']:
                        freq_appos += 1
                        freq_sent[name['sentNum']]['freq_appos'] += 1
                        freq_syntax[name['syntax']]['freq_appos'] += 1
                        freq_status[name['givenness']]['freq_appos'] += 1
                        freq_sent_status[name['sentence-givenness']]['freq_appos'] += 1

                    if not name['has_title'] and not name['has_firstName'] and not name['has_middleName'] and not name['has_lastName'] and not name['has_appositive']:
                        freq_no_class += 1
                        freq_sent[name['sentNum']]['freq_no_class'] += 1
                        freq_syntax[name['syntax']]['freq_no_class'] += 1
                        freq_status[name['givenness']]['freq_no_class'] += 1
                        freq_sent_status[name['sentence-givenness']]['freq_no_class'] += 1

                    elif name['has_title'] and not name['has_firstName'] and not name['has_middleName'] and not name['has_lastName'] and not name['has_appositive']:
                        t += 1
                        freq_sent[name['sentNum']]['t'] += 1
                        freq_syntax[name['syntax']]['t'] += 1
                        freq_status[name['givenness']]['t'] += 1
                        freq_sent_status[name['sentence-givenness']]['t'] += 1
                    elif not name['has_title'] and name['has_firstName'] and not name['has_middleName'] and not name['has_lastName'] and not name['has_appositive']:
                        first += 1
                        freq_sent[name['sentNum']]['f'] += 1
                        freq_syntax[name['syntax']]['f'] += 1
                        freq_status[name['givenness']]['f'] += 1
                        freq_sent_status[name['sentence-givenness']]['f'] += 1
                    elif not name['has_title'] and not name['has_firstName'] and name['has_middleName'] and not name['has_lastName'] and not name['has_appositive']:
                        m += 1
                        freq_sent[name['sentNum']]['m'] += 1
                        freq_syntax[name['syntax']]['m'] += 1
                        freq_status[name['givenness']]['m'] += 1
                        freq_sent_status[name['sentence-givenness']]['m'] += 1
                    elif not name['has_title'] and not name['has_firstName'] and not name['has_middleName'] and name['has_lastName'] and not name['has_appositive']:
                        l += 1
                        freq_sent[name['sentNum']]['l'] += 1
                        freq_syntax[name['syntax']]['l'] += 1
                        freq_status[name['givenness']]['l'] += 1
                        freq_sent_status[name['sentence-givenness']]['l'] += 1
                    elif not name['has_title'] and not name['has_firstName'] and not name['has_middleName'] and not name['has_lastName'] and name['has_appositive']:
                        a += 1
                        freq_sent[name['sentNum']]['a'] += 1
                        freq_syntax[name['syntax']]['a'] += 1
                        freq_status[name['givenness']]['a'] += 1
                        freq_sent_status[name['sentence-givenness']]['a'] += 1

                    elif name['has_title'] and name['has_firstName'] and not name['has_middleName'] and not name['has_lastName'] and not name['has_appositive']:
                        t_f += 1
                        freq_sent[name['sentNum']]['t_f'] += 1
                        freq_syntax[name['syntax']]['t_f'] += 1
                        freq_status[name['givenness']]['t_f'] += 1
                        freq_sent_status[name['sentence-givenness']]['t_f'] += 1
                    elif name['has_title'] and not name['has_firstName'] and name['has_middleName'] and not name['has_lastName'] and not name['has_appositive']:
                        t_m += 1
                        freq_sent[name['sentNum']]['t_m'] += 1
                        freq_syntax[name['syntax']]['t_m'] += 1
                        freq_status[name['givenness']]['t_m'] += 1
                        freq_sent_status[name['sentence-givenness']]['t_m'] += 1
                    elif name['has_title'] and not name['has_firstName'] and not name['has_middleName'] and name['has_lastName'] and not name['has_appositive']:
                        t_l += 1
                        freq_sent[name['sentNum']]['t_l'] += 1
                        freq_syntax[name['syntax']]['t_l'] += 1
                        freq_status[name['givenness']]['t_l'] += 1
                        freq_sent_status[name['sentence-givenness']]['t_l'] += 1
                    elif name['has_title'] and not name['has_firstName'] and not name['has_middleName'] and not name['has_lastName'] and name['has_appositive']:
                        t_a += 1
                        freq_sent[name['sentNum']]['t_a'] += 1
                        freq_syntax[name['syntax']]['t_a'] += 1
                        freq_status[name['givenness']]['t_a'] += 1
                        freq_sent_status[name['sentence-givenness']]['t_a'] += 1
                    elif not name['has_title'] and name['has_firstName'] and name['has_middleName'] and not name['has_lastName'] and not name['has_appositive']:
                        f_m += 1
                        freq_sent[name['sentNum']]['f_m'] += 1
                        freq_syntax[name['syntax']]['f_m'] += 1
                        freq_status[name['givenness']]['f_m'] += 1
                        freq_sent_status[name['sentence-givenness']]['f_m'] += 1
                    elif not name['has_title'] and name['has_firstName'] and not name['has_middleName'] and name['has_lastName'] and not name['has_appositive']:
                        f_l += 1
                        freq_sent[name['sentNum']]['f_l'] += 1
                        freq_syntax[name['syntax']]['f_l'] += 1
                        freq_status[name['givenness']]['f_l'] += 1
                        freq_sent_status[name['sentence-givenness']]['f_l'] += 1
                    elif not name['has_title'] and name['has_firstName'] and not name['has_middleName'] and not name['has_lastName'] and name['has_appositive']:
                        f_a += 1
                        freq_sent[name['sentNum']]['f_a'] += 1
                        freq_syntax[name['syntax']]['f_a'] += 1
                        freq_status[name['givenness']]['f_a'] += 1
                        freq_sent_status[name['sentence-givenness']]['f_a'] += 1
                    elif not name['has_title'] and not name['has_firstName'] and name['has_middleName'] and name['has_lastName'] and not name['has_appositive']:
                        m_l += 1
                        freq_sent[name['sentNum']]['m_l'] += 1
                        freq_syntax[name['syntax']]['m_l'] += 1
                        freq_status[name['givenness']]['m_l'] += 1
                        freq_sent_status[name['sentence-givenness']]['m_l'] += 1
                    elif not name['has_title'] and not name['has_firstName'] and name['has_middleName'] and not name['has_lastName'] and name['has_appositive']:
                        m_a += 1
                        freq_sent[name['sentNum']]['m_a'] += 1
                        freq_syntax[name['syntax']]['m_a'] += 1
                        freq_status[name['givenness']]['m_a'] += 1
                        freq_sent_status[name['sentence-givenness']]['m_a'] += 1
                    elif not name['has_title'] and not name['has_firstName'] and not name['has_middleName'] and name['has_lastName'] and name['has_appositive']:
                        l_a += 1
                        freq_sent[name['sentNum']]['l_a'] += 1
                        freq_syntax[name['syntax']]['l_a'] += 1
                        freq_status[name['givenness']]['l_a'] += 1
                        freq_sent_status[name['sentence-givenness']]['l_a'] += 1

                    elif name['has_title'] and name['has_firstName'] and name['has_middleName'] and not name['has_lastName'] and not name['has_appositive']:
                        t_f_m += 1
                        freq_sent[name['sentNum']]['t_f_m'] += 1
                        freq_syntax[name['syntax']]['t_f_m'] += 1
                        freq_status[name['givenness']]['t_f_m'] += 1
                        freq_sent_status[name['sentence-givenness']]['t_f_m'] += 1
                    elif name['has_title'] and name['has_firstName'] and not name['has_middleName'] and name['has_lastName'] and not name['has_appositive']:
                        t_f_l += 1
                        freq_sent[name['sentNum']]['t_f_l'] += 1
                        freq_syntax[name['syntax']]['t_f_l'] += 1
                        freq_status[name['givenness']]['t_f_l'] += 1
                        freq_sent_status[name['sentence-givenness']]['t_f_l'] += 1
                    elif name['has_title'] and name['has_firstName'] and not name['has_middleName'] and not name['has_lastName'] and name['has_appositive']:
                        t_f_a += 1
                        freq_sent[name['sentNum']]['t_f_a'] += 1
                        freq_syntax[name['syntax']]['t_f_a'] += 1
                        freq_status[name['givenness']]['t_f_a'] += 1
                        freq_sent_status[name['sentence-givenness']]['t_f_a'] += 1
                    elif name['has_title'] and not name['has_firstName'] and name['has_middleName'] and name['has_lastName'] and not name['has_appositive']:
                        t_m_l += 1
                        freq_sent[name['sentNum']]['t_m_l'] += 1
                        freq_syntax[name['syntax']]['t_m_l'] += 1
                        freq_status[name['givenness']]['t_m_l'] += 1
                        freq_sent_status[name['sentence-givenness']]['t_m_l'] += 1
                    elif name['has_title'] and not name['has_firstName'] and name['has_middleName'] and not name['has_lastName'] and name['has_appositive']:
                        t_m_a += 1
                        freq_sent[name['sentNum']]['t_m_a'] += 1
                        freq_syntax[name['syntax']]['t_m_a'] += 1
                        freq_status[name['givenness']]['t_m_a'] += 1
                        freq_sent_status[name['sentence-givenness']]['t_m_a'] += 1
                    elif name['has_title'] and not name['has_firstName'] and not name['has_middleName'] and name['has_lastName'] and name['has_appositive']:
                        t_l_a += 1
                        freq_sent[name['sentNum']]['t_l_a'] += 1
                        freq_syntax[name['syntax']]['t_l_a'] += 1
                        freq_status[name['givenness']]['t_l_a'] += 1
                        freq_sent_status[name['sentence-givenness']]['t_l_a'] += 1
                    elif not name['has_title'] and name['has_firstName'] and name['has_middleName'] and name['has_lastName'] and not name['has_appositive']:
                        f_m_l += 1
                        freq_sent[name['sentNum']]['f_m_l'] += 1
                        freq_syntax[name['syntax']]['f_m_l'] += 1
                        freq_status[name['givenness']]['f_m_l'] += 1
                        freq_sent_status[name['sentence-givenness']]['f_m_l'] += 1
                    elif not name['has_title'] and name['has_firstName'] and name['has_middleName'] and not name['has_lastName'] and name['has_appositive']:
                        f_m_a += 1
                        freq_sent[name['sentNum']]['f_m_a'] += 1
                        freq_syntax[name['syntax']]['f_m_a'] += 1
                        freq_status[name['givenness']]['f_m_a'] += 1
                        freq_sent_status[name['sentence-givenness']]['f_m_a'] += 1
                    elif not name['has_title'] and name['has_firstName'] and not name['has_middleName'] and name['has_lastName'] and name['has_appositive']:
                        f_l_a += 1
                        freq_sent[name['sentNum']]['f_l_a'] += 1
                        freq_syntax[name['syntax']]['f_l_a'] += 1
                        freq_status[name['givenness']]['f_l_a'] += 1
                        freq_sent_status[name['sentence-givenness']]['f_l_a'] += 1
                    elif not name['has_title'] and not name['has_firstName'] and name['has_middleName'] and name['has_lastName'] and name['has_appositive']:
                        m_l_a += 1
                        freq_sent[name['sentNum']]['m_l_a'] += 1
                        freq_syntax[name['syntax']]['m_l_a'] += 1
                        freq_status[name['givenness']]['m_l_a'] += 1
                        freq_sent_status[name['sentence-givenness']]['m_l_a'] += 1

                    elif name['has_title'] and name['has_firstName'] and name['has_middleName'] and name['has_lastName'] and not name['has_appositive']:
                        t_f_m_l += 1
                        freq_sent[name['sentNum']]['t_f_m_l'] += 1
                        freq_syntax[name['syntax']]['t_f_m_l'] += 1
                        freq_status[name['givenness']]['t_f_m_l'] += 1
                        freq_sent_status[name['sentence-givenness']]['t_f_m_l'] += 1
                    elif name['has_title'] and name['has_firstName'] and name['has_middleName'] and not name['has_lastName'] and name['has_appositive']:
                        t_f_m_a += 1
                        freq_sent[name['sentNum']]['t_f_m_a'] += 1
                        freq_syntax[name['syntax']]['t_f_m_a'] += 1
                        freq_status[name['givenness']]['t_f_m_a'] += 1
                        freq_sent_status[name['sentence-givenness']]['t_f_m_a'] += 1
                    elif name['has_title'] and name['has_firstName'] and not name['has_middleName'] and name['has_lastName'] and name['has_appositive']:
                        t_f_l_a += 1
                        freq_sent[name['sentNum']]['t_f_l_a'] += 1
                        freq_syntax[name['syntax']]['t_f_l_a'] += 1
                        freq_status[name['givenness']]['t_f_l_a'] += 1
                        freq_sent_status[name['sentence-givenness']]['t_f_l_a'] += 1
                    elif name['has_title'] and not name['has_firstName'] and name['has_middleName'] and name['has_lastName'] and name['has_appositive']:
                        t_m_l_a += 1
                        freq_sent[name['sentNum']]['t_m_l_a'] += 1
                        freq_syntax[name['syntax']]['t_m_l_a'] += 1
                        freq_status[name['givenness']]['t_m_l_a'] += 1
                        freq_sent_status[name['sentence-givenness']]['t_m_l_a'] += 1
                    elif not name['has_title'] and name['has_firstName'] and name['has_middleName'] and name['has_lastName'] and name['has_appositive']:
                        f_m_l_a += 1
                        freq_sent[name['sentNum']]['f_m_l_a'] += 1
                        freq_syntax[name['syntax']]['f_m_l_a'] += 1
                        freq_status[name['givenness']]['f_m_l_a'] += 1
                        freq_sent_status[name['sentence-givenness']]['f_m_l_a'] += 1

                    elif name['has_title'] and name['has_firstName'] and name['has_middleName'] and name['has_lastName'] and name['has_appositive']:
                        t_f_m_l_a += 1
                        freq_sent[name['sentNum']]['t_f_m_l_a'] += 1
                        freq_syntax[name['syntax']]['t_f_m_l_a'] += 1
                        freq_status[name['givenness']]['t_f_m_l_a'] += 1
                        freq_sent_status[name['sentence-givenness']]['t_f_m_l_a'] += 1

                    if 'givenNames' in name['name_type']:
                        freq_given += 1
                        freq_sent[name['sentNum']]['freq_given'] += 1
                        freq_syntax[name['syntax']]['freq_given'] += 1
                        freq_status[name['givenness']]['freq_given'] += 1
                        freq_sent_status[name['sentence-givenness']]['freq_given'] += 1
                    if 'surnames' in name['name_type']:
                        freq_surnames += 1
                        freq_sent[name['sentNum']]['freq_surnames'] += 1
                        freq_syntax[name['syntax']]['freq_surnames'] += 1
                        freq_status[name['givenness']]['freq_surnames'] += 1
                        freq_sent_status[name['sentence-givenness']]['freq_surnames'] += 1
                    if 'birthNames' in name['name_type']:
                        freq_birthname += 1
                        freq_sent[name['sentNum']]['freq_birthname'] += 1
                        freq_syntax[name['syntax']]['freq_birthname'] += 1
                        freq_status[name['givenness']]['freq_birthname'] += 1
                        freq_sent_status[name['sentence-givenness']]['freq_birthname'] += 1
        except:
            freq_corrupted += 1
            corrupted.append(f)

    result = {'freq_corrupted':freq_corrupted, 'corrupted':corrupted, 'freq_mentions': freq_mentions, 'freq_no_class': freq_no_class, \
              'freq_sentence':freq_sent, 'freq_syntax': freq_syntax, 'freq_status': freq_status, 'freq_sent_status': freq_sent_status, \
              'freq_title': freq_title, 'freq_first': freq_first, 'freq_middle': freq_middle, 'freq_last': freq_last, \
              'freq_appos': freq_appos, 'freq_given': freq_given, 'freq_surnames': freq_surnames, 'freq_birthname': freq_birthname, 'name_size':name_size, \
              't': t, 'f': first, 'm': m, 'l': l, 'a': a, \
              't_f': t_f, 't_m': t_m, 't_l': t_l, 't_a': t_a, 'f_m': f_m, 'f_l': f_l, 'f_a': f_a, 'm_l': m_l, 'm_a': m_a, 'l_a': l_a, \
              't_f_m': t_f_m, 't_f_l': t_f_l, 't_f_a': t_f_a, 't_m_l': t_m_l, 't_m_a': t_m_a, \
              't_l_a': t_l_a, 'f_m_l': f_m_l, 'f_m_a': f_m_a, 'f_l_a': f_l_a, 'm_l_a': m_l_a, \
              't_f_m_l': t_f_m_l, 't_f_m_a': t_f_m_a, 't_f_l_a': t_f_l_a, 't_m_l_a': t_m_l_a, 'f_m_l_a': f_m_l_a, 't_f_m_l_a': t_f_m_l_a}
    json.dump(result, open(fname, 'w'), indent=4, separators=(',', ': '))