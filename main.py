# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON


# This is a sample Python script.

def query_id_from_wikidata(person_id="Q57231890", platform_predicate="wdt:P496"):
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

    orcid_ids_set = set()
    for result in results["results"]["bindings"]:
        orcid_ids_set.add(result['o']['value'])
        #print(result['o']['value'])
        #print(result.keys())
        #print(type(result))

    return orcid_ids_set

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    platform_properties_dict = {
                                "ORCID": "wdt:P496",
                                "Google Scholar": "wdt:P1960",
                                "VIAF": "wdt:P214",
                                "DBLP": "wdt:P2456",
                                "Dimensions": "wdt:P6178",
                                "Github": "wdt:P2037",
                                "Microsoft Academic ": "wdt:P6366",
                                "Semantic Scholar": "wdt:P4012",
                                "DNB/GNB": "wdt:P227",
                                "ACM Digital Library": "wdt:P864"
                                }

    wd_person_id = "Q57231890"
    persons_dict = {}
    for platform in platform_properties_dict.keys():
        platform_property = platform_properties_dict[platform]
        platform_id = query_id_from_wikidata(person_id=wd_person_id, platform_predicate=platform_property)
        if len(platform_id) == 0:
            continue
        print("ID (%s): %s" % (platform, platform_id))
        person_dict = persons_dict.get(wd_person_id, {})
        # only relevant if it's defaulting to {}
        persons_dict[wd_person_id] = person_dict
        # add values for the specific platform
        person_dict[platform] = platform_id
    print(persons_dict)
