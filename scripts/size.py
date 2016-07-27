__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 09/05/2016
Description:
    This script aims to average the size of the references as a function of syntax and referential status
"""

from tabulate import tabulate

import json
import numpy as np
import scikits.bootstrap as boot

def display(header, data):
    print '\n'
    print tabulate(data, headers=header)
    print '\n'

def parse():
    result = {'subj':[], 'obj':[], 'dnew':[], 'dold':[], 'snew':[], 'sold':[]}
    r = json.load(open('../data/report.json'))

    result['subj'] = r['freq_syntax']['np-subj']['name_size']
    result['obj'] = r['freq_syntax']['np-obj']['name_size']

    result['dnew'] = r['freq_status']['new']['name_size']
    result['dold'] = r['freq_status']['old']['name_size']

    result['snew'] = r['freq_sent_status']['new']['name_size']
    result['sold'] = r['freq_sent_status']['old']['name_size']
    return result

if __name__ == '__main__':
    j = parse()

    # syntax
    header = ['SYNCAT', 'AVG.', 'STD', 'CONFIDENCE INTERVALS', '']
    data = []

    for syncat in ['subj', 'obj']:
        sizes = j[syncat]
        mean, sigma = np.mean(sizes), np.std(sizes)
        conf_int = map(lambda x: round(x, 6), boot.ci(sizes))
        interval = (conf_int[1] - conf_int[0]) / 2

        data.append([syncat, mean, sigma, conf_int, interval])
    display(header, data)

    # discourse status
    header = ['D-Status', 'AVG.', 'STD', 'CONFIDENCE INTERVALS', '']
    data = []

    for status in ['dnew', 'dold']:
        sizes = j[status]
        mean, sigma = np.mean(sizes), np.std(sizes)
        conf_int = map(lambda x: round(x, 6), boot.ci(sizes))
        interval = (conf_int[1] - conf_int[0]) / 2

        data.append([syncat, mean, sigma, conf_int, interval])
    display(header, data)

    # sentence status
    header = ['S-Status', 'AVG.', 'STD', 'CONFIDENCE INTERVALS', '']
    data = []

    for status in ['snew', 'sold']:
        sizes = j[status]
        mean, sigma = np.mean(sizes), np.std(sizes)
        conf_int = map(lambda x: round(x, 6), boot.ci(sizes))
        interval = (conf_int[1] - conf_int[0]) / 2

        data.append([syncat, mean, sigma, conf_int, interval])
    display(header, data)