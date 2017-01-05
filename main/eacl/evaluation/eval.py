__author__ = 'thiagocastroferreira'

import sys
sys.path.append('../../../')

import properties

import bootstrap
import cPickle as p
import nltk
import numpy as np
import os

from nltk.metrics.distance import edit_distance, jaccard_distance
from sklearn.metrics import accuracy_score
from scipy import stats
import scipy as sp
import scipy.stats

# fentities = '/roaming/tcastrof/names/eacl/entities.json'
# # entities_dir = '/roaming/tcastrof/names/eacl/evaluationV3'
# entities_dir = '/roaming/tcastrof/names/eacl/evaluation/intrinsic_domain'
# webpages_dir = '/roaming/tcastrof/names/webpages'

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return round(m, 6), round(h, 6), round(m-h, 6), round(m+h, 6)

def get_domain(fname):
    f = open(os.path.join(properties.webpages_dir, fname))
    webpage = f.read()
    f.close()

    url = webpage.split('\n')[0].split('\t')[1]

    if 'blog' in url or 'wordpress' in url or 'tumblr' in url:
        return 'blog'
    elif 'new' in url or 'article' in url:
        return 'news'
    elif 'wiki' in url:
        return 'wiki'
    else:
        return 'others'

def get_values(entities, domain):
    _random, bayes_random = {}, {}
    bayes_no_variation, bayes_variation = {}, {}
    siddharthan, deemter  = {}, {}

    for _id in entities:
        evaluation = p.load(open(os.path.join(properties.evaluation_dir, _id)))

        for fold in evaluation:
            if fold not in bayes_random:
                _random[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
                bayes_random[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
                bayes_no_variation[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
                bayes_variation[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
                siddharthan[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}
                deemter[fold] = {'y_real':[], 'y_pred':[], 'string':[], 'jaccard':[]}

            for item in evaluation[fold]:
                item_domain = get_domain(item['features']['fname'])

                if domain == item_domain or domain == '':
                    string_real = item['real']['reference']
                    string_random = item['random']['reference']
                    string_bayes_random = item['bayes_random']['reference'][0][0]
                    string_bayes_no_variation = item['bayes_no_variation']['reference'][0][0]
                    string_bayes_variation = item['bayes_variation']['reference'][0][0]
                    string_siddharthan = item['siddharthan']['reference']
                    string_deemter = item['deemter']['reference']

                    dist_random = edit_distance(string_random, string_real)
                    dist_bayes_random = edit_distance(string_bayes_random, string_real)
                    dist_bayes_no_variation = edit_distance(string_bayes_no_variation, string_real)
                    dist_bayes_variation = edit_distance(string_bayes_variation, string_real)
                    dist_siddharthan = edit_distance(string_siddharthan, string_real)
                    dist_deemter = edit_distance(string_deemter, string_real)

                    tokens_real = set(nltk.word_tokenize(string_real))
                    tokens_random = set(nltk.word_tokenize(string_random))
                    tokens_bayes_random = set(nltk.word_tokenize(string_bayes_random))
                    tokens_bayes_no_variation = set(nltk.word_tokenize(string_bayes_no_variation))
                    tokens_bayes_variation = set(nltk.word_tokenize(string_bayes_variation))
                    tokens_siddharthan = set(nltk.word_tokenize(string_siddharthan))
                    tokens_deemter = set(nltk.word_tokenize(string_deemter))

                    jaccard_random = jaccard_distance(tokens_random, tokens_real)
                    jaccard_bayes_random = jaccard_distance(tokens_bayes_random, tokens_real)
                    jaccard_bayes_no_variation = jaccard_distance(tokens_bayes_no_variation, tokens_real)
                    jaccard_bayes_variation = jaccard_distance(tokens_bayes_variation, tokens_real)
                    jaccard_siddharthan = jaccard_distance(tokens_siddharthan, tokens_real)
                    jaccard_deemter = jaccard_distance(tokens_deemter, tokens_real)

                    bayes_random[fold]['y_real'].append(item['real']['label'])
                    bayes_random[fold]['y_pred'].append(item['bayes_random']['label'][0])
                    bayes_random[fold]['string'].append(dist_bayes_random)
                    bayes_random[fold]['jaccard'].append(jaccard_bayes_random)

                    bayes_no_variation[fold]['y_real'].append(item['real']['label'])
                    bayes_no_variation[fold]['y_pred'].append(item['bayes_no_variation']['label'][0])
                    bayes_no_variation[fold]['string'].append(dist_bayes_no_variation)
                    bayes_no_variation[fold]['jaccard'].append(jaccard_bayes_no_variation)

                    bayes_variation[fold]['y_real'].append(item['real']['label'])
                    bayes_variation[fold]['y_pred'].append(item['bayes_variation']['label'][0])
                    bayes_variation[fold]['string'].append(dist_bayes_variation)
                    bayes_variation[fold]['jaccard'].append(jaccard_bayes_variation)

                    _random[fold]['y_real'].append(item['real']['label'])
                    _random[fold]['y_pred'].append(item['random']['label'])
                    _random[fold]['string'].append(dist_random)
                    _random[fold]['jaccard'].append(jaccard_random)

                    siddharthan[fold]['y_real'].append(item['real']['label'])
                    siddharthan[fold]['y_pred'].append(item['siddharthan']['label'])
                    siddharthan[fold]['string'].append(dist_siddharthan)
                    siddharthan[fold]['jaccard'].append(jaccard_siddharthan)

                    deemter[fold]['y_real'].append(item['real']['label'])
                    deemter[fold]['y_pred'].append(item['deemter']['label'])
                    deemter[fold]['string'].append(dist_deemter)
                    deemter[fold]['jaccard'].append(jaccard_deemter)
    return _random, bayes_random, bayes_no_variation, bayes_variation, siddharthan, deemter

def write_csv(general_random, general_siddharthan, general_deemter, general_bayes_no_variation, general_bayes_variation, write_dir):
    if not os.path.exists(write_dir):
        os.mkdir(write_dir)

    f_string = open(os.path.join(write_dir, 'string.csv'), 'w')
    f_jaccard = open(os.path.join(write_dir, 'jaccard.csv'), 'w')

    f_string.write('Subject,Random,Deemter,Siddharthan,PNmVariation,PNpVariation\n')
    f_jaccard.write('Subject,Random,Deemter,Siddharthan,PNmVariation,PNpVariation\n')

    for i in range(0, len(general_random['string'])):
        f_string.write(str(i+1)+','+str(general_random['string'][i])+','+str(general_deemter['string'][i])+','+ \
                       str(general_siddharthan['string'][i])+','+str(general_bayes_no_variation['string'][i])+ \
                       ','+str(general_bayes_variation['string'][i])+'\n')
        f_jaccard.write(str(i+1)+','+str(general_random['jaccard'][i])+','+str(general_deemter['jaccard'][i])+','+ \
                        str(general_siddharthan['jaccard'][i])+','+str(general_bayes_no_variation['jaccard'][i])+ \
                       ','+str(general_bayes_variation['jaccard'][i])+'\n')
    f_string.close()
    f_jaccard.close()

def run(std=True, domain=''):
    entities = os.listdir(properties.evaluation_dir)

    _random, bayes_random, bayes_no_variation, bayes_variation, siddharthan, deemter = get_values(entities, domain)

    general_random = {'accuracy':[], 'string':[], 'jaccard':[]}
    general_bayes_random = {'accuracy':[], 'string':[], 'jaccard':[]}
    general_bayes_no_variation = {'accuracy':[], 'string':[], 'jaccard':[]}
    general_bayes_variation = {'accuracy':[], 'string':[], 'jaccard':[]}
    general_siddharthan = {'accuracy':[], 'string':[], 'jaccard':[]}
    general_deemter = {'accuracy':[], 'string':[], 'jaccard':[]}
    number_samples, number_samples1 = 0, 0

    for fold in bayes_random:
        general_random['accuracy'].append(accuracy_score(_random[fold]['y_real'], _random[fold]['y_pred']))
        general_random['string'].append(np.mean(_random[fold]['string']))
        general_random['jaccard'].append(np.mean(_random[fold]['jaccard']))

        general_siddharthan['accuracy'].append(accuracy_score(siddharthan[fold]['y_real'], siddharthan[fold]['y_pred']))
        general_siddharthan['string'].append(np.mean(siddharthan[fold]['string']))
        general_siddharthan['jaccard'].append(np.mean(siddharthan[fold]['jaccard']))

        general_deemter['accuracy'].append(accuracy_score(deemter[fold]['y_real'], deemter[fold]['y_pred']))
        general_deemter['string'].append(np.mean(deemter[fold]['string']))
        general_deemter['jaccard'].append(np.mean(deemter[fold]['jaccard']))

        general_bayes_random['accuracy'].append(accuracy_score(bayes_random[fold]['y_real'], bayes_random[fold]['y_pred']))
        general_bayes_random['string'].append(np.mean(bayes_random[fold]['string']))
        general_bayes_random['jaccard'].append(np.mean(bayes_random[fold]['jaccard']))

        general_bayes_no_variation['accuracy'].append(accuracy_score(bayes_no_variation[fold]['y_real'], bayes_no_variation[fold]['y_pred']))
        general_bayes_no_variation['string'].append(np.mean(bayes_no_variation[fold]['string']))
        general_bayes_no_variation['jaccard'].append(np.mean(bayes_no_variation[fold]['jaccard']))

        general_bayes_variation['accuracy'].append(accuracy_score(bayes_variation[fold]['y_real'], bayes_variation[fold]['y_pred']))
        general_bayes_variation['string'].append(np.mean(bayes_variation[fold]['string']))
        general_bayes_variation['jaccard'].append(np.mean(bayes_variation[fold]['jaccard']))
        number_samples += len(bayes_no_variation[fold]['string'])
        number_samples1 += len(siddharthan[fold]['string'])

        if std and domain == '':
            print 'Fold', fold
            print 'Labels: '
            print 'Random: ', accuracy_score(_random[fold]['y_real'], _random[fold]['y_pred'])
            print 'Siddharthan: ', accuracy_score(siddharthan[fold]['y_real'], siddharthan[fold]['y_pred'])
            print 'Deemter: ', accuracy_score(deemter[fold]['y_real'], deemter[fold]['y_pred'])
            print 'Bayes Random: ', accuracy_score(bayes_random[fold]['y_real'], bayes_random[fold]['y_pred'])
            print 'Bayes No Variation: ', accuracy_score(bayes_no_variation[fold]['y_real'], bayes_no_variation[fold]['y_pred'])
            print 'Bayes Variation: ', accuracy_score(bayes_variation[fold]['y_real'], bayes_variation[fold]['y_pred'])
            print 20 * '-'
            print 'String Distance: '
            print 'Random: ', np.mean(_random[fold]['string'])
            print 'Siddharthan: ', np.mean(siddharthan[fold]['string'])
            print 'Deemter: ', np.mean(deemter[fold]['string'])
            print 'Bayes Random: ', np.mean(bayes_random[fold]['string'])
            print 'Bayes No Variation: ', np.mean(bayes_no_variation[fold]['string'])
            print 'Bayes Variation: ', np.mean(bayes_variation[fold]['string'])
            print 20 * '-'
            print 'Jaccard Distance: '
            print 'Random: ', np.mean(_random[fold]['jaccard'])
            print 'Siddharthan: ', np.mean(siddharthan[fold]['jaccard'])
            print 'Deemter: ', np.mean(deemter[fold]['jaccard'])
            print 'Bayes Random: ', np.mean(bayes_random[fold]['jaccard'])
            print 'Bayes No Variation: ', np.mean(bayes_no_variation[fold]['jaccard'])
            print 'Bayes Variation: ', np.mean(bayes_variation[fold]['jaccard'])
            print 20 * '-'
            print '\n'

    if std:
        print 'GENERAL', domain
        print 'Labels: '
        print 'Random: ', np.mean(general_random['accuracy'])
        print 'Siddharthan: ', np.mean(general_siddharthan['accuracy'])
        print 'Deemter: ', np.mean(general_deemter['accuracy'])
        print 'Bayes Random: ', np.mean(general_bayes_random['accuracy'])
        print 'Bayes No Variation: ', np.mean(general_bayes_no_variation['accuracy'])
        print 'Bayes Variation: ', np.mean(general_bayes_variation['accuracy'])
        print 20 * '-'
        print 'String Distance: '
        print 'Random: ', mean_confidence_interval(general_random['string']), bootstrap.ci(general_random['string'])
        print 'Siddharthan: ', mean_confidence_interval(general_siddharthan['string']), bootstrap.ci(general_siddharthan['string'])
        print 'Deemter: ', mean_confidence_interval(general_deemter['string']), bootstrap.ci(general_deemter['string'])
        print 'Bayes Random: ', mean_confidence_interval(general_bayes_random['string']), bootstrap.ci(general_bayes_random['string'])
        print 'Bayes No Variation: ', mean_confidence_interval(general_bayes_no_variation['string']), bootstrap.ci(general_bayes_no_variation['string'])
        print 'Bayes Variation: ', mean_confidence_interval(general_bayes_variation['string']), bootstrap.ci(general_bayes_variation['string'])
        print 20 * '-'
        print 'Jaccard Distance: '
        print 'Random: ', mean_confidence_interval(general_random['jaccard']), bootstrap.ci(general_random['jaccard'])
        print 'Siddharthan: ', mean_confidence_interval(general_siddharthan['jaccard']), bootstrap.ci(general_siddharthan['jaccard'])
        print 'Deemter: ', mean_confidence_interval(general_deemter['jaccard']), bootstrap.ci(general_deemter['jaccard'])
        print 'Bayes Random: ', mean_confidence_interval(general_bayes_random['jaccard']), bootstrap.ci(general_bayes_random['jaccard'])
        print 'Bayes No Variation: ', mean_confidence_interval(general_bayes_no_variation['jaccard']), bootstrap.ci(general_bayes_no_variation['jaccard'])
        print 'Bayes Variation: ', mean_confidence_interval(general_bayes_variation['jaccard']), bootstrap.ci(general_bayes_variation['jaccard'])
        print 20 * '-'
        print '\n'

        print 'String -> T-test: Random X PN-Variation'
        t, p = stats.ttest_ind(general_random['string'], general_bayes_no_variation['string'])
        print round(t, 6), p
        t, p = stats.ttest_rel(general_random['string'], general_bayes_no_variation['string'])
        print round(t, 6), p
        print 10 * '-'
        print 'String -> T-test: Random X PN+Variation'
        t, p = stats.ttest_ind(general_random['string'], general_bayes_variation['string'])
        print round(t, 6), p
        t, p = stats.ttest_rel(general_random['string'], general_bayes_variation['string'])
        print round(t, 6), p
        print 10 * '-'

        print 'String -> T-test: Siddarthan X PN-Variation'
        t, p = stats.ttest_ind(general_siddharthan['string'], general_bayes_no_variation['string'])
        print round(t, 6), p
        t, p = stats.ttest_rel(general_siddharthan['string'], general_bayes_no_variation['string'])
        print round(t, 6), p
        print 10 * '-'
        print 'String -> T-test: Siddarthan X PN+Variation'
        t, p = stats.ttest_ind(general_siddharthan['string'], general_bayes_variation['string'])
        print round(t, 6), p
        t, p = stats.ttest_rel(general_siddharthan['string'], general_bayes_variation['string'])
        print round(t, 6), p
        print 10 * '-'

        print 'String -> T-test: Deemter X PN-Variation'
        t, p = stats.ttest_ind(general_deemter['string'], general_bayes_no_variation['string'])
        print round(t, 6), p
        t, p = stats.ttest_rel(general_deemter['string'], general_bayes_no_variation['string'])
        print round(t, 6), p
        print 10 * '-'
        print 'String -> T-test: Deemter X PN+Variation'
        t, p = stats.ttest_ind(general_deemter['string'], general_bayes_variation['string'])
        print round(t, 6), p
        t, p = stats.ttest_rel(general_deemter['string'], general_bayes_variation['string'])
        print round(t, 6), p
        print 10 * '-'

        print 'String -> T-test: PN-Variation X PN+Variation'
        t, p = stats.ttest_ind(general_bayes_no_variation['string'], general_bayes_variation['string'])
        print round(t, 6), p
        t, p = stats.ttest_rel(general_bayes_no_variation['string'], general_bayes_variation['string'])
        print round(t, 6), p
        print 10 * '-'

        print 'String -> One way ANOVA'
        t, p = stats.f_oneway(general_random['string'], general_siddharthan['string'], general_deemter['string'], general_bayes_no_variation['string'], general_bayes_variation['string'])
        print round(t, 6), p
        print 10 * '-'

        print 'Number of samples: ', number_samples, number_samples1

    write_dir = '/roaming/tcastrof/names/eacl/evaluation'
    write_csv(general_random, general_siddharthan, general_deemter, general_bayes_no_variation, general_bayes_variation, write_dir)

if __name__ == '__main__':
    print 'BLOGS: '
    run(True, 'blog')
    print '\n\n'
    print 'NEWS:'
    run(True, 'news')
    print '\n\n'
    print 'WIKI:'
    run(True, 'wiki')
    print '\n\n'
    print 'OTHERS:'
    run(True, 'others')
    print '\n\n'
    print 'GENERAL:'
    run(True, '')