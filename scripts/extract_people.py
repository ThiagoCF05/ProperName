__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 20/04/2016
Description:
    This script aims to extract information about the top 1000 people from Wikilinks corpus at dbpedia.
"""

from rdflib import Graph, URIRef
import json
import os

def get_names():
    people, temp_people = {}, {}
    l = os.listdir('entities')

    for _f in l:
        people[_f], temp_people[_f] = {}, {}
        with open(os.path.join('entities', _f)) as _f1:
            doc = _f1.read()
            doc = doc.split('\n\n\n')[:-1]

            for person in doc:
                person = person.split('\n')
                people[_f][person[0]] = {}

                birthPlaces = person[1].split('\t')
                people[_f][person[0]][birthPlaces[0]] = filter(lambda x: x != '', birthPlaces[1:])

                surnames = person[2].split('\t')
                people[_f][person[0]][surnames[0]] = filter(lambda x: x != '', surnames[1:])

                birthNames = person[3].split('\t')
                people[_f][person[0]][birthNames[0]] = filter(lambda x: x != '', birthNames[1:])

                givenNames = person[4].split('\t')
                people[_f][person[0]][givenNames[0]] = filter(lambda x: x != '', givenNames[1:])

                foaf_names = person[5].split('\t')
                people[_f][person[0]][foaf_names[0]] = filter(lambda x: x != '', foaf_names[1:])

                birthDates = person[6].split('\t')
                people[_f][person[0]][birthDates[0]] = filter(lambda x: x != '', birthDates[1:])

                dbp_names = person[7].split('\t')
                people[_f][person[0]][dbp_names[0]] = filter(lambda x: x != '', dbp_names[1:])

                aliases = person[8].split('\t')
                people[_f][person[0]][aliases[0]] = filter(lambda x: x != '', aliases[1:])
    return people, temp_people

def is_person(uri):
    try:
        uri = URIRef(uri)
        person = URIRef('http://dbpedia.org/ontology/Person')
        g = Graph()
        g.parse(uri)
        resp = g.query(
            "ASK {?uri a ?person}",
            initBindings={'uri': uri, 'person': person}
        )
        return resp.askAnswer
    #     print uri, "is a person?", resp.askAnswer
    except:
        print 'ERROR: ', uri
        return False

def get_entity(uri):
    foaf_names, foaf_givenNames, foaf_surnames = [], [], []
    dbp_names, dbo_birthPlaces, dbo_birthNames, dbo_birthDates, dbo_deathDates, dbo_aliases = [], [], [], [], [], []

    try:
        g = Graph()
        g.parse(URIRef(uri))

        # SELECTING THE NAME, FIRST NAME AND SURNAME OF THE PERSON
        query = """SELECT DISTINCT ?foaf_name ?foaf_givenName ?foaf_surname
            WHERE { ?x foaf:name ?foaf_name .
                    ?x foaf:givenName ?foaf_givenName .
                    ?x foaf:surname ?foaf_surname . }"""
        resp = g.query(query)
        for result in resp.result:
            foaf_names.append(result[0])
            foaf_givenNames.append(result[1])
            foaf_surnames.append(result[2])

        # SELECTING THE NAME OF THE PERSON BORN
        query = """SELECT ?dbp_name
            WHERE { ?x dbp:name ?dbp_name . }"""
        resp = g.query(query)
        for result in resp.result:
            dbp_names.append(result[0])

        # SELECTING THE PLACE WHERE THE PERSON BORN
        query = """SELECT ?dbo_birthPlace
            WHERE { ?x dbo:birthPlace ?dbo_birthPlace . }"""
        resp = g.query(query)
        for result in resp.result:
            dbo_birthPlaces.append(result[0])

        # SELECTING THE DATE WHEN THE PERSON BORN
        query = """SELECT ?dbo_birthDate
            WHERE { ?x dbo:birthDate ?dbo_birthDate . }"""
        resp = g.query(query)
        for result in resp.result:
            dbo_birthDates.append(result[0])

        # SELECTING THE DATE WHEN THE PERSON DIED
        query = """SELECT ?dbo_deathDate
            WHERE { ?x dbo:deathDate ?dbo_deathDate . }"""
        resp = g.query(query)
        for result in resp.result:
            dbo_deathDates.append(result[0])

        # SELECTING THE BIRTH NAME OF THE PERSON
        query = """SELECT ?dbo_birthName
            WHERE { ?x dbo:birthName ?dbo_birthName . }"""
        resp = g.query(query)
        for result in resp.result:
            dbo_birthNames.append(result[0])

        # SELECTING THE ALIAS OF THE PERSON
        query = """SELECT ?dbo_alias
            WHERE { ?x dbo:alias ?dbo_alias . }"""
        resp = g.query(query)
        for result in resp.result:
            dbo_aliases.append(result[0])
    except:
        print 'ERROR: ', uri

    return set(dbo_aliases), set(foaf_names), set(foaf_givenNames), set(foaf_surnames), set(dbp_names), \
           set(dbo_birthPlaces), set(dbo_birthNames), set(dbo_birthDates), set(dbo_deathDates)

def save_names(people, file_name):
    f = open(os.path.join('entities', file_name), 'a')
    for uri in people:
        f.write(uri.encode('utf-8'))
        f.write('\n')
        for prop in people[uri]:
            f.write(prop)
            f.write('\t')
            for values in people[uri][prop]:
                f.write(values.encode('utf-8'))
                f.write('\t')
            f.write('\n')
        f.write('\n\n')
    f.close()

def save(people, fwrite):
    json.dump(people, open(fwrite, 'w'), sort_keys=True, indent=4, separators=(',', ': '))

def run():
    entities_dir = "/roaming/thiago/wikilinks/wikilinks/entities.txt"
    write_dir = "/roaming/thiago/wikilinks/wikilinks/dbpedia.txt"

    people = {}

    entities = []
    with open(entities_dir) as f:
        entities = f.readlines()
    entities = map(lambda x: x.split('\t')[0], entities)

    for entity in entities:
        name = entity.split('/')[-1]
        uri = os.path.join('http://dbpedia.org/resource/', name)
        aliases, foaf_names, givenNames, surnames, dbp_names, birthPlaces, birthNames, birthDates, deathDates = get_entity(uri)

        people[entity] = {'aliases':aliases, 'foaf_names':foaf_names, 'givenNames':givenNames, 'surnames':surnames, \
                          'dbp_names':dbp_names, 'birthPlaces':birthPlaces, 'birthNames':birthNames, 'birthDates':birthDates, 'deathDates': deathDates}
    save_names(people, write_dir)
    save(people, write_dir)

if __name__ == '__main__':
    run()