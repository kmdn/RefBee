import urllib.request
from rdflib import Graph
from rdflib import Dataset
from rdflib.namespace import RDF
import pprint


def retrieve_titles(input_nt=""):
    g = Graph()
    g.parse(input_nt)
    print("RDF File:", g)


    print(len(g))
    # prints: 2
    for stmt in g:
        print(stmt)
    #for s, p, o, g in g.quads((None, None, None, None)):
    #    print(s, p, o, g)
    return None


def paper_titles_for_id(person_id):
    url = f'https://dblp.org/pid/{person_id}.nt'
    titles = retrieve_titles(input_nt=urllib.request.urlopen(url))
    print("DBLP: ", titles)
    return titles

