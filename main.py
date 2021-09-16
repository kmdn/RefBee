# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON


# This is a sample Python script.

def query_wikidata(person_id="Q57231890", platform_predicate="wdt:P496"):
    endpoint_url = "https://query.wikidata.org/sparql"

    query = """SELECT DISTINCT ?o WHERE {
      wd:"""+person_id+""" """+platform_predicate+""" ?o .
      wd:"""+person_id+""" wdt:P31 wd:Q5.
    }
    LIMIT 100"""

    def get_results(endpoint_url, query):
        user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        # TODO adjust user agent; see https://w.wiki/CX6
        sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()

    results = get_results(endpoint_url, query)

    for result in results["results"]["bindings"]:
        print(result['o']['value'])
        print(result.keys())
        print(type(result))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    query_wikidata()
