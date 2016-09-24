__author__ = 'thiagocastroferreira'

import json
import os

mention_dir = '/roaming/tcastrof/names/eacl/mentions'
entities_dir = '/roaming/tcastrof/names/eacl/entities.json'

entities = ['http://en.wikipedia.org/wiki/Diana_Ross',
            'http://en.wikipedia.org/wiki/Muammar_Gaddafi',
            'http://en.wikipedia.org/wiki/Jack_Nicholson',
            'http://en.wikipedia.org/wiki/Paris_Hilton',
            'http://en.wikipedia.org/wiki/Anna_Wintour',
            'http://en.wikipedia.org/wiki/Charles_Manson',
            'http://en.wikipedia.org/wiki/Lindsay_Lohan',
            'http://en.wikipedia.org/wiki/Dick_Cheney',
            'http://en.wikipedia.org/wiki/George_Lucas',
            'http://en.wikipedia.org/wiki/Clint_Eastwood',
            'http://en.wikipedia.org/wiki/Britney_Spears',
            'http://en.wikipedia.org/wiki/Mark_Zuckerberg',
            'http://en.wikipedia.org/wiki/Anne_Boleyn',
            'http://en.wikipedia.org/wiki/Kurt_Vonnegut',
            'http://en.wikipedia.org/wiki/Neville_Chamberlain',
            'http://en.wikipedia.org/wiki/Kylie_Minogue',
            'http://en.wikipedia.org/wiki/Elton_John',
            'http://en.wikipedia.org/wiki/Charles,_Prince_of_Wales',
            'http://en.wikipedia.org/wiki/Donald_Rumsfeld',
            'http://en.wikipedia.org/wiki/Magic_Johnson',
            'http://en.wikipedia.org/wiki/Kobe_Bryant',
            'http://en.wikipedia.org/wiki/Rick_Santorum',
            'http://en.wikipedia.org/wiki/Michael_Schumacher',
            'http://en.wikipedia.org/wiki/Raila_Odinga',
            'http://en.wikipedia.org/wiki/Mark_Antony']

if __name__ == '__main__':
    for entity in entities:
        print entity
        for fname in os.listdir(mention_dir):
            mentions = json.load(open(os.path.join(mention_dir, fname)))

            if entity in mentions.keys():
                f = filter(lambda x: x['type'] == 'PROPER', mentions[entity])

                if len(f) >= 10:
                    print fname
        print 10 * '*'