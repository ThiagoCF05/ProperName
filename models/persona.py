__author__ = 'thiagocastroferreira'

import json
import numpy as np
import os

from sklearn import tree
from sklearn.cross_validation import KFold
from sklearn.metrics import classification_report, accuracy_score

def run(X_train, y_train, X_test, y_test):
    clf_title = tree.DecisionTreeClassifier()
    clf_title.fit(X_train, y_train[:, 0])
    title = (clf_title.predict(X_test), y_test[:, 0])

    clf_first = tree.DecisionTreeClassifier()
    clf_first.fit(X_train, y_train[:, 1])
    first = (clf_title.predict(X_test), y_test[:, 1])

    clf_middle = tree.DecisionTreeClassifier()
    clf_middle.fit(X_train, y_train[:, 2])
    middle = (clf_title.predict(X_test), y_test[:, 2])

    clf_last = tree.DecisionTreeClassifier()
    clf_last.fit(X_train, y_train[:, 3])
    last = (clf_title.predict(X_test), y_test[:, 3])

    clf_appositive = tree.DecisionTreeClassifier()
    clf_appositive.fit(X_train, y_train[:, 4])
    appositive = (clf_title.predict(X_test), y_test[:, 4])

    return title, first, middle, last, appositive

if __name__ == '__main__':
    fdir = 'features/personal'
    files = os.listdir(fdir)
    folds = {}
    titles_true, titles_pred, firsts_true, firsts_pred, middles_true, middles_pred, lasts_true, lasts_pred, appositives_true, appositives_pred = \
        [], [], [], [], [], [], [], [], [], []
    for fname in files:
        print fname, '\r',
        folds[fname] = {}
        j = json.load(open(os.path.join(fdir, fname)))
        X = np.array(map(lambda features: [features[1], features[2], features[3]], j['features']))
        y = np.array(j['classes'])

        if y.shape[0] >= 10:
            _fold = 1
            kf = KFold(y.shape[0], n_folds=10)
            for train, test in kf:
                folds[fname][_fold] = {'title':[], 'first':[], 'middle':[], 'last':[], 'appositive':[]}
                X_train, y_train, X_test, y_test = X[train], y[train], X[test], y[test]
                title, first, middle, last, appositive = run(X_train, y_train, X_test, y_test)

                folds[fname][_fold] = {
                    'title':title,
                    'first':first,
                    'middle':middle,
                    'last':last,
                    'appositive':appositive
                }

                titles_true.extend(title[0])
                titles_pred.extend(title[1])

                firsts_true.extend(first[0])
                firsts_pred.extend(first[1])

                middles_true.extend(middle[0])
                middles_pred.extend(middle[1])

                lasts_true.extend(last[0])
                lasts_pred.extend(last[1])

                appositives_true.extend(appositive[0])
                appositives_pred.extend(appositive[1])

    print 'TITLE'
    print accuracy_score(titles_true, titles_pred)
    print '\n'
    print classification_report(titles_true, titles_pred)
    print 10 * '-'
    print 'FIRST'
    print accuracy_score(firsts_true, firsts_pred)
    print '\n'
    print classification_report(firsts_true, firsts_pred)
    print 10 * '-'
    print 'MIDDLE'
    print accuracy_score(middles_true, middles_pred)
    print '\n'
    print classification_report(middles_true, middles_pred)
    print 10 * '-'
    print 'LAST'
    print accuracy_score(lasts_true, lasts_pred)
    print '\n'
    print classification_report(lasts_true, lasts_pred)
    print 10 * '-'
    print 'APPOSITIVE'
    print accuracy_score(appositives_true, appositives_pred)
    print '\n'
    print classification_report(appositives_true, appositives_pred)
    print 10 * '-'

    # json.dump(folds, open('folds.json', 'w'))
