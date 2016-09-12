from main import utils as vutils

__author__ = 'thiagocastroferreira'

import os


def update(dbpedia):
    if 'aliases' in dbpedia.keys():
        del dbpedia['aliases']

    dbpedia['first_names'] = []
    dbpedia['middle_names'] = []
    dbpedia['last_names'] = []

    for givenName in dbpedia['givenNames']:
        names = givenName.split()

        if len(names[0]) > 2:
            dbpedia['first_names'].append(names[0])
        for middle in names[1:]:
            if len(middle) > 2:
                dbpedia['middle_names'].append(middle)

    for birthName in dbpedia['birthNames']:
        names = birthName.split()

        if len(names[0]) > 2:
            dbpedia['first_names'].append(names[0])
        if len(names[-1]) > 2:
            dbpedia['last_names'].append(names[-1])
        names.remove(names[-1])
        for middle in names[1:]:
            if len(middle) > 2:
                dbpedia['middle_names'].append(middle)
    dbpedia['last_names'].extend(dbpedia['surnames'])

    dbpedia['first_names'] = list(set(dbpedia['first_names']))
    dbpedia['middle_names'] = list(set(dbpedia['middle_names']))
    dbpedia['last_names'] = list(set(dbpedia['last_names']))
    return dbpedia

if __name__ == '__main__':
    parsed_dir = "data/vareg/parsed"
    mentions_dir = "data/vareg/mentions"
    files = os.listdir(parsed_dir)
    files.remove('.DS_Store')


    nfiles = 0
    for file in files:
        f = filter(lambda x: x in file, vutils.file_vs_names.keys())

        if len(f) > 0:
            dbpedia = update(vutils.file_vs_names[f[0]])
            nfiles += 1
            if nfiles % 10 == 0:
                print nfiles, "processed", '\r',

            mentions = get_mentions.run(os.path.join(parsed_dir, file), dbpedia)

            # for mention in mentions:
            #     print mention
            # p.dump(mentions, open(os.path.join(mentions_dir, file.split('.')[0]), 'w'))


            sentences = list(set(map(lambda x: int(x['sentNum']), mentions)))
            sentences.sort()
            print file.split('.')[0]
            for sentence in sentences:
                f = filter(lambda x: int(x['sentNum']) == sentence, mentions)
                for mention in f:
                    print mention
                print '\n'
            print 20 * '-'
            print '\n'