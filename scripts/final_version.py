__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 07/07/2016
Description:
    This script aims to build the final version of the corpus introduced at INLG 2016
"""

import os
import json
from shutil import copyfile

if __name__ == '__main__':
    fdir = '/roaming/tcastrof/names/mentions'
    furls = '/roaming/tcastrof/names/urls-top50-new.txt'

    with open(furls) as f:
        urls = f.read()
        urls = map(lambda x: x.split('\n'), urls.split('\n\n'))
        urls = dict(map(lambda x: (x[0], map(lambda y: y.split('\t'),x[1:])), urls))

    notfound = 0
    for e in urls.keys():
        for url in urls[e]:
            try:
                mentions = json.load(open(os.path.join(fdir, url[0])))
                nmentions = 0
                for entity in mentions:
                    nmentions = nmentions + len(mentions[entity])

                if nmentions > 0:
                    copyfile(os.path.join('/roaming/tcastrof/names/webpages', url[0]), \
                             os.path.join('/roaming/tcastrof/names/regnames/webpages', url[0]))

                    copyfile(os.path.join('/roaming/tcastrof/names/parsed', url[0]), \
                             os.path.join('/roaming/tcastrof/names/regnames/parsed', url[0]))

                    copyfile(os.path.join(fdir, url[0]), \
                             os.path.join('/roaming/tcastrof/names/regnames/mentions', url[0]))
            except Exception,e:
                notfound = notfound + 1
                print 'Files not found: ', notfound