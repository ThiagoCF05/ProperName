__author__ = 'thiagocastroferreira'

from Bayes import Bayes

training_set = ['Barack Obama', 'Barack Obama', 'President Barack Obama', 'President Obama', 'Obama', 'Obama', 'Barack Obama, the 44th president of United States'] # just for illustration

train_set_content = [{'entity': 'Barack_Obama', 'givenness': 'old', 'sentence-givenness': 'new', 'syntax': 'np-subj', 'label': '+f+l', 'label_elems': ['+f', '+l']},
                     {'entity': 'Barack_Obama', 'givenness': 'new', 'sentence-givenness': 'new', 'syntax': 'np-subj', 'label': '+f+l', 'label_elems': ['+f', '+l']},
                     {'entity': 'Barack_Obama', 'givenness': 'new', 'sentence-givenness': 'new', 'syntax': 'np-obj', 'label': '+t+f+l', 'label_elems': ['+t', '+f', '+l']},
                     {'entity': 'Barack_Obama', 'givenness': 'old', 'sentence-givenness': 'new', 'syntax': 'np-subj', 'label': '+t+l', 'label_elems': ['+t', '+l']},
                     {'entity': 'Barack_Obama', 'givenness': 'old', 'sentence-givenness': 'new', 'syntax': 'np-subj', 'label': '+l', 'label_elems': ['+l']},
                     {'entity': 'Barack_Obama', 'givenness': 'old', 'sentence-givenness': 'old', 'syntax': 'np-subj', 'label': '+l', 'label_elems': ['+l']},
                     {'entity': 'Barack_Obama', 'givenness': 'new', 'sentence-givenness': 'new', 'syntax': 'np-subj', 'label': '+f+l+a', 'label_elems': ['+f', '+l', '+a']}]

train_set_realization = [{'word': 'Barack', 'bigram': ('Barack', '*'), 'entity': 'Barack_Obama', 'givenness': 'old', 'sentence-givenness': 'new', 'syntax': 'np-subj', 'label': '+f+l'},
                         {'word': 'Obama', 'bigram': ('Obama', 'Barack'), 'entity': 'Barack_Obama', 'givenness': 'old', 'sentence-givenness': 'new', 'syntax': 'np-subj', 'label': '+f+l'},
                         {'word': 'END', 'bigram': ('END', 'Obama'), 'entity': 'Barack_Obama', 'givenness': 'old', 'sentence-givenness': 'new', 'syntax': 'np-subj', 'label': '+f+l'},
                         # Second Example
                         {'word': 'Barack', 'bigram': ('Barack', '*'), 'entity': 'Barack_Obama', 'givenness': 'new', 'sentence-givenness': 'new', 'syntax': 'np-subj', 'label': '+f+l'},
                         {'word': 'Obama', 'bigram': ('Obama', 'Barack'), 'entity': 'Barack_Obama', 'givenness': 'new', 'sentence-givenness': 'new', 'syntax': 'np-subj', 'label': '+f+l'},
                         {'word': 'END', 'bigram': ('END', 'Obama'), 'entity': 'Barack_Obama', 'givenness': 'new', 'sentence-givenness': 'new', 'syntax': 'np-subj', 'label': '+f+l'},
                         # Third Example
                         {'word': 'President', 'bigram': ('President', '*'), 'entity': 'Barack_Obama', 'givenness': 'new', 'sentence-givenness': 'new', 'syntax': 'np-obj', 'label': '+t+f+l'},
                         {'word': 'Barack', 'bigram': ('Barack', 'President'), 'entity': 'Barack_Obama', 'givenness': 'new', 'sentence-givenness': 'new', 'syntax': 'np-obj', 'label': '+t+f+l'},
                         {'word': 'Obama', 'bigram': ('Obama', 'Barack'), 'entity': 'Barack_Obama', 'givenness': 'new', 'sentence-givenness': 'new', 'syntax': 'np-obj', 'label': '+t+f+l'},
                         {'word': 'END', 'bigram': ('END', 'Obama'), 'entity': 'Barack_Obama', 'givenness': 'new', 'sentence-givenness': 'new', 'syntax': 'np-obj', 'label': '+t+f+l'},
                         # Fourth Example
                         {'word': 'President', 'bigram': ('President', '*'), 'entity': 'Barack_Obama', 'givenness': 'old', 'sentence-givenness': 'new', 'syntax': 'np-subj', 'label': '+t+l'},
                         {'word': 'Obama', 'bigram': ('Obama', 'President'), 'entity': 'Barack_Obama', 'givenness': 'old', 'sentence-givenness': 'new', 'syntax': 'np-subj', 'label': '+t+l'},
                         {'word': 'END', 'bigram': ('END', 'Obama'), 'entity': 'Barack_Obama', 'givenness': 'old', 'sentence-givenness': 'new', 'syntax': 'np-subj', 'label': '+t+l'},
                         # Fifth Example
                         {'word': 'Obama', 'bigram': ('Obama', '*'), 'entity': 'Barack_Obama', 'givenness': 'old', 'sentence-givenness': 'new', 'syntax': 'np-subj', 'label': '+l'},
                         {'word': 'END', 'bigram': ('END', 'Obama'), 'entity': 'Barack_Obama', 'givenness': 'old', 'sentence-givenness': 'new', 'syntax': 'np-subj', 'label': '+l'},
                         # Sixth Example
                         {'word': 'Obama', 'bigram': ('Obama', '*'), 'entity': 'Barack_Obama', 'givenness': 'old', 'sentence-givenness': 'old', 'syntax': 'np-subj', 'label': '+l'},
                         {'word': 'END', 'bigram': ('END', 'Obama'), 'entity': 'Barack_Obama', 'givenness': 'old', 'sentence-givenness': 'old', 'syntax': 'np-subj', 'label': '+l'},
                         # Seventh Example
                         {'word': 'Barack', 'bigram': ('Barack', '*'), 'entity': 'Barack_Obama', 'givenness': 'new', 'sentence-givenness': 'new', 'syntax': 'np-subj', 'label': '+f+l+a'},
                         {'word': 'Obama', 'bigram': ('Obama', 'Barack'), 'entity': 'Barack_Obama', 'givenness': 'new', 'sentence-givenness': 'new', 'syntax': 'np-subj', 'label': '+f+l+a'},
                         {'word': 'END', 'bigram': ('END', 'Obama'), 'entity': 'Barack_Obama', 'givenness': 'new', 'sentence-givenness': 'new', 'syntax': 'np-subj', 'label': '+f+l+a'}]

clf = Bayes(train_set_content=train_set_content, train_set_realization=train_set_realization, bigram=True)

features = {
    'discourse_se': 'new',
    'sentence_se': 'new',
    'syntax_se': 'np-subj'
}
entity = 'Barack_Obama'

print clf.select_content(D=features, p=entity)

print clf.realize(form='+f+l+a', p=entity, syntax='np-subj', appositive='the 44th president of USA')