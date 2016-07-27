__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 19/05/2016
Description:
    This script aims to extract the size of the proper names in the first 100 sentences in the texts.
    A linear regression is also computed.
"""

import json
import numpy as np

from sklearn import linear_model

if __name__ == '__main__':
    r = json.load(open('../data/report.json'))

    sizes = []

    sentences = map(lambda x: int(x), r['freq_sentence'].keys())
    sentences.sort()

    for s in sentences[:100]:
        sizes.append(np.mean(r['freq_sentence'][str(s)]['name_size']))

    regr = linear_model.LinearRegression()

    X = map(lambda x: [float(x)], sentences[:100])
    y = sizes
    regr.fit(X, sizes)

    predictions = regr.predict(X)

    data = zip(sentences[:100], sizes)
    regression = zip(sentences[:100], predictions)

    plot1 = map(lambda x: str(x[0]) + ' ' + str(x[1]), data)
    plot2 = map(lambda x: str(x[0]) + ' ' + str(x[1]), regression)

    print 'Data'
    print '\\\\'.join(plot1)
    print '\n\n'
    print 'Regression'
    print '\\\\'.join(plot2)