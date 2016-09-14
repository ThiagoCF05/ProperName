__author__ = 'thiagocastroferreira'

labels = [
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

features = {
    'syntax':['np-subj', 'np-obj', 'subj-det'],
    'givenness':['new', 'old'],
    'sentence-givenness':['new', 'old']
}