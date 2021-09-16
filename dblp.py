import urllib.request
from rdflib import Graph
from rdflib import Dataset
from rdflib.namespace import RDF
import pprint


def retrieve_titles(input_nt=""):
    g = Graph()
    g.parse(input_nt)

    print(len(g))
    # prints: 2
    for stmt in g:
        pprint.pprint(stmt)
    for s, p, o, g in g.quads((None, RDF.type, None, None)):
        print(s, g)


def paper_titles_for_id(person_id):
    url = f'https://dblp.org/pid/{person_id}.nt'
    titles = retrieve_titles(input_nt=urllib.request.urlopen(url))
    print("DBLP: ", titles)
    return titles

