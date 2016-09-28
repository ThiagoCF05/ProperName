__author__ = 'thiagocastroferreira'

import json
import nltk
import os

mentions_dir = '/roaming/tcastrof/names/eacl/mentions'
webpages_dir = '/roaming/tcastrof/names/webpages'

def main():
    fnames = os.listdir(mentions_dir)
    words = []

    for fname in fnames:
        print fname
        f = open(os.path.join(webpages_dir, fname))
        webpage = f.read()
        f.close()

        url = webpage.split('\n')[0].split('\t')[1]

        url = str(url).replace('http://', '').replace('.com', '')
        for i in url.split('/'):
            for j in i.split('.'):
                for word in j.split('-'):
                    words.append(word)

    freq = nltk.FreqDist(words)
    json.dump(freq, open('freq_url.json', 'w'), separators=(',',':'))

if __name__ == '__main__':
    main()