__author__ = 'thiagocastroferreira'

import os

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def run(fname):
    root = ET.parse(fname)
    root = root.getroot()
    title = root.find('TITLE').text

    soup = BeautifulSoup(open('data/htmls/layout.html'))

    soup.title.append(title)

    soup.body.header.h1.append(title)

    paragraphs = root.findall('PARAGRAPH')
    reference_id = 1

    original_div = soup.find('div', {'id':'original'})
    variation_div = soup.find('div', {'id':'variation'})
    novariation_div = soup.find('div', {'id':'no-variation'})

    for p_i, p in enumerate(paragraphs):
        original_p = BeautifulSoup("<p class=\"lead\"></p>").p
        variation_p = BeautifulSoup("<p class=\"lead\"></p>").p
        novariation_p = BeautifulSoup("<p class=\"lead\"></p>").p

        for e_i, child in enumerate(p):
            if child.tag == 'STRING':
                original_p.append(child.text)
                variation_p.append(child.text)
                novariation_p.append(child.text)
            elif child.tag == 'REFERENCE':
                original = child.text
                variation = ''
                novariation = ''

                refexes = child.findall('REFEX')

                for refex in refexes:
                    if refex.attrib['MODEL'] == 'bayes_variation':
                        variation = refex.text
                    elif refex.attrib['MODEL'] == 'bayes_no_variation':
                        novariation = refex.text
                    elif refex.attrib['MODEL'] == 'original':
                        original = refex.text

                tag_span = BeautifulSoup("<span style=\"background-color: #FFFF00\">"+ original.strip()+"</span>").span
                original_p.append(tag_span)

                tag_span = BeautifulSoup("<span style=\"background-color: #FFFF00\">"+ variation.strip()+"</span>").span
                variation_p.append(tag_span)

                tag_span = BeautifulSoup("<span style=\"background-color: #FFFF00\">"+ novariation.strip()+"</span>").span
                novariation_p.append(tag_span)
        original_div.append(original_p)
        variation_div.append(variation_p)
        novariation_div.append(novariation_p)

    f = open(os.path.join('data/htmls', title + ".html"), 'w')
    f.write(soup.prettify(formatter="html").encode("utf-8"))
    f.close()

if __name__ == '__main__':
    xmls = os.listdir('data/processed')
    xmls = filter(lambda x: x != '.DS_Store', xmls)

    for xml in xmls:
        run(os.path.join('data/processed', xml))

