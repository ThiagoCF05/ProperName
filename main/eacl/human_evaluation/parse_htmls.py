__author__ = 'thiagocastroferreira'

import os

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from random import randint

def run(fname, combinations):
    root = ET.parse(fname)
    root = root.getroot()
    title = root.find('TITLE').text

    soup = BeautifulSoup(open('data/htmls/layout.html'))

    paragraphs = root.findall('PARAGRAPH')

    article_div = soup.find('div', {'id':'article'}).div
    index = randint(0, len(combinations)-1)
    for i, idx in enumerate(combinations[index]):
        if idx == 1:
            original_div = BeautifulSoup("<div id=\"original\" class=\"col-md-4\"></div>").div
            article_div.append(original_div)

            _id = 'inlineRadio'+str(i+1)
            label = soup.find('input', {'id':_id})
            label['value'] = 'original'
        elif idx == 2:
            variation_div = BeautifulSoup("<div id=\"variation\" class=\"col-md-4\"></div>").div
            article_div.append(variation_div)

            _id = 'inlineRadio'+str(i+1)
            label = soup.find('input', {'id':_id})
            label['value'] = 'variation'
        else:
            novariation_div = BeautifulSoup("<div id=\"novariation\" class=\"col-md-4\"></div>").div
            article_div.append(novariation_div)

            _id = 'inlineRadio'+str(i+1)
            label = soup.find('input', {'id':_id})
            label['value'] = 'novariation'

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

    combinations = [(1,2,3), (1,3,2), (2,1,3), (2,3,1), (3,1,2), (3,2,1)]
    for xml in xmls:
        run(os.path.join('data/processed', xml), combinations)

