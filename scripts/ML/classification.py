__author__ = 'thiagocastroferreira'

import json
import numpy as np

from sklearn import cross_validation, svm, tree
# from sklearn.metrics import classification_report

if __name__ == '__main__':
    fname = '/roaming/tcastrof/names/ML.json'

    j = json.load(open(fname))

    # X = map(lambda features: [features[1], features[2], features[3]], j['features'])
    X = j['features']
    y = np.array(j['classes'])

    print 20 * '*'
    print 'AD'
    clf_title = tree.DecisionTreeClassifier()
    scores = cross_validation.cross_val_score(clf_title, X, y[:, 0], cv=10)
    print("TITLE \t Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    # predicted = cross_validation.cross_val_predict(clf_title, X, y[:, 0], cv=10)
    # print(classification_report(y[:, 0], predicted))
    # print 20 * '-'

    clf_first = tree.DecisionTreeClassifier()
    scores = cross_validation.cross_val_score(clf_first, X, y[:, 1], cv=10)
    print("FIRST \t Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    # predicted = cross_validation.cross_val_predict(clf_first, X, y[:, 1], cv=10)
    # print(classification_report(y[:, 1], predicted))
    # print 20 * '-'

    clf_middle = tree.DecisionTreeClassifier()
    scores = cross_validation.cross_val_score(clf_middle, X, y[:, 2], cv=10)
    print("MIDDLE \t Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    # predicted = cross_validation.cross_val_predict(clf_middle, X, y[:, 2], cv=10)
    # print(classification_report(y[:, 2], predicted))
    # print 20 * '-'

    clf_last = tree.DecisionTreeClassifier()
    scores = cross_validation.cross_val_score(clf_last, X, y[:, 3], cv=10)
    print("LAST \t Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    # predicted = cross_validation.cross_val_predict(clf_last, X, y[:, 3], cv=10)
    # print(classification_report(y[:, 3], predicted))
    # print 20 * '-'

    clf_appositive = tree.DecisionTreeClassifier()
    scores = cross_validation.cross_val_score(clf_appositive, X, y[:, 4], cv=10)
    print("APPOSITIVE \t Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    # predicted = cross_validation.cross_val_predict(clf_appositive, X, y[:, 4], cv=10)
    # print(classification_report(y[:, 4], predicted))
    # print '\n'

    print 20 * '*'
    for c in [0.001, 0.01, 0.1, 1, 10, 100, 1000]:
        print 'SVM / C -> ', c
        clf_title = svm.SVC(kernel='linear', C=c)
        scores = cross_validation.cross_val_score(clf_title, X, y[:, 0], cv=10)
        print("TITLE \t Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        # predicted = cross_validation.cross_val_predict(clf_title, X, y[:, 0], cv=10)
        # print(classification_report(y[:, 0], predicted))
        # print 20 * '-'

        clf_first = svm.SVC(kernel='linear', C=c)
        scores = cross_validation.cross_val_score(clf_first, X, y[:, 1], cv=10)
        print("FIRST \t Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        # predicted = cross_validation.cross_val_predict(clf_first, X, y[:, 1], cv=10)
        # print(classification_report(y[:, 1], predicted))
        # print 20 * '-'

        clf_middle = svm.SVC(kernel='linear', C=c)
        scores = cross_validation.cross_val_score(clf_middle, X, y[:, 2], cv=10)
        print("MIDDLE \t Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        # predicted = cross_validation.cross_val_predict(clf_middle, X, y[:, 2], cv=10)
        # print(classification_report(y[:, 2], predicted))
        # print 20 * '-'

        clf_last = svm.SVC(kernel='linear', C=c)
        scores = cross_validation.cross_val_score(clf_last, X, y[:, 3], cv=10)
        print("LAST \t Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        # predicted = cross_validation.cross_val_predict(clf_last, X, y[:, 3], cv=10)
        # print(classification_report(y[:, 3], predicted))
        # print 20 * '-'

        clf_appositive = svm.SVC(kernel='linear', C=c)
        scores = cross_validation.cross_val_score(clf_appositive, X, y[:, 4], cv=10)
        print("APPOSITIVE \t Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        # predicted = cross_validation.cross_val_predict(clf_appositive, X, y[:, 4], cv=10)
        # print(classification_report(y[:, 4], predicted))
        # print 20 * '-'
    print 20 * '-'