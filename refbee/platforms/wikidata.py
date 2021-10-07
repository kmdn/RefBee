from refbee.util import get_sparql_query_results

platform_properties_dict = {
    "ORCID": "wdt:P496",
    "Google Scholar": "wdt:P1960",
    "VIAF": "wdt:P214",
    "DBLP": "wdt:P2456",
    "Dimensions": "wdt:P6178",
    "Github": "wdt:P2037",
    "Microsoft Academic": "wdt:P6366",
    "Semantic Scholar": "wdt:P4012",
    "DNB/GNB": "wdt:P227",
    #"ACM Digital Library": "wdt:P864"
}

def query_id_from_wikidata(person_id="Q57231890", platform_predicate="wdt:P496"):
    endpoint_url = "https://query.wikidata.org/sparql"

    query = """SELECT DISTINCT ?o WHERE {
      wd:""" + person_id + """ """ + platform_predicate + """ ?o .
      wd:""" + person_id + """ wdt:P31 wd:Q5.
    }
    LIMIT 100"""

    results = get_sparql_query_results(endpoint_url, query)

    ids_set = set()
    for result in results["results"]["bindings"]:
        ids_set.add(result['o']['value'])
    return ids_set

def paper_titles_for_id(person_id):
    """ Get all entities the person is the author of.

        Could additionally be filtered by entity type:
            https://www.wikidata.org/wiki/Q23927052  conference paper
            https://www.wikidata.org/wiki/Q13442814  scholarly article
            https://www.wikidata.org/wiki/Q18918145  academic journal article
            https://www.wikidata.org/wiki/Q591041    scientific publication
            https://www.wikidata.org/wiki/Q55915575  scholarly work
    """
    endpoint_url = "https://query.wikidata.org/sparql"
    query = ('SELECT ?pub ?title WHERE { ?pub wdt:P50 wd:' + person_id + ' .'
                                                                         '?pub wdt:P1476 ?title . }')
    results = get_sparql_query_results(endpoint_url, query)
    paper_titles = [r['title']['value'] for r in results['results']['bindings']]
    return paper_titles

def platform_ids_for_person(person_id):

    persons_dict = {
        person_id: {"Wikidata": set([person_id])}
    }
    for platform in platform_properties_dict.keys():
        platform_property = platform_properties_dict[platform]
        platform_id = query_id_from_wikidata(person_id=person_id, platform_predicate=platform_property)
        if len(platform_id) == 0:
            continue
        print("ID (%s): %s" % (platform, platform_id))
        person_dict = persons_dict.get(person_id, {})
        # only relevant if it's defaulting to {}
        persons_dict[person_id] = person_dict
        # add values for the specific platform
        person_dict[platform] = platform_id
    print(persons_dict)
    return persons_dict