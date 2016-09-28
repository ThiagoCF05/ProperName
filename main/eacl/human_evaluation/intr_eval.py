__author__ = 'thiagocastroferreira'

import numpy as np
import os
import scipy as sp
import scipy.stats

import xml.etree.ElementTree as ET

from nltk.metrics.distance import edit_distance, jaccard_distance

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return round(m, 6), round(h, 6), round(m-h, 6), round(m+h, 6)

def process(xml):
    results = []

    root = ET.parse(xml)
    root = root.getroot()

    paragraphs = root.findall('PARAGRAPH')

    for p in paragraphs:
        references = p.findall('REFERENCE')
        for reference in references:
            refexes = reference.findall('REFEX')

            expression = {}
            for refex in refexes:
                if refex.attrib['MODEL'] == 'siddharthan':
                    expression['siddharthan'] = str(refex.text).strip()
                elif refex.attrib['MODEL'] == 'bayes_no_variation':
                    expression['bayes_no_variation'] = str(refex.text).strip()
                elif refex.attrib['MODEL'] == 'bayes_variation':
                    expression['bayes_variation'] = str(refex.text).strip()
                elif refex.attrib['MODEL'] == 'original':
                    expression['original'] = str(refex.text).strip()
            results.append(expression)
    return results

def eval(references):
    string_distances = {'siddharthan':[], 'bayes_no_variation':[], 'bayes_variation':[]}
    jaccard_distances = {'siddharthan':[], 'bayes_no_variation':[], 'bayes_variation':[]}

    for reference in references:
        print reference
        string_distances['siddharthan'].append(edit_distance(reference['original'], reference['siddharthan']))
        string_distances['bayes_no_variation'].append(edit_distance(reference['original'], reference['bayes_no_variation']))
        string_distances['bayes_variation'].append(edit_distance(reference['original'], reference['bayes_variation']))

        # jaccard_distances['siddharthan'].append(jaccard_distance(reference['original'], reference['siddharthan']))
        # jaccard_distances['bayes_no_variation'].append(jaccard_distance(reference['original'], reference['bayes_no_variation']))
        # jaccard_distances['bayes_variation'].append(jaccard_distance(reference['original'], reference['bayes_variation']))

    print 'String distances: '
    print 'siddharthan: ', mean_confidence_interval(string_distances['siddharthan'])
    print 'bayes_no_variation: ', mean_confidence_interval(string_distances['bayes_no_variation'])
    print 'bayes_variation: ', mean_confidence_interval(string_distances['bayes_variation'])
    print 10 * '-'
    # print 'Jaccard distance:'
    # print 'siddharthan: ', mean_confidence_interval(jaccard_distances['siddharthan'])
    # print 'bayes_no_variation: ', mean_confidence_interval(jaccard_distances['bayes_no_variation'])
    # print 'bayes_variation: ', mean_confidence_interval(jaccard_distances['bayes_variation'])
    # print 10 * '-'

if __name__ == '__main__':
    xmls = ['Anne Boleyn.xml', 'Britney Spears.xml', 'Diana Ross.xml', 'Donald Rumsfeld.xml', 'Elton John.xml', \
            'Kobe Bryant.xml', 'Kylie Minogue.xml', 'Lindsay Lohan.xml', 'Magic Johnson.xml', 'Neville Chamberlain.xml']

    results = []
    for xml in xmls:
        result = process(os.path.join('data/processed', xml))
        results.extend(result)

    eval(results)

