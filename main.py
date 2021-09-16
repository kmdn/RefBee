# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
import orcid
from SPARQLWrapper import SPARQLWrapper, JSON
import viaf
import acm
import dimensions
import dblp


def query_id_from_wikidata(person_id="Q57231890", platform_predicate="wdt:P496"):
    endpoint_url = "https://query.wikidata.org/sparql"

    query = """SELECT DISTINCT ?o WHERE {
      wd:""" + person_id + """ """ + platform_predicate + """ ?o .
      wd:""" + person_id + """ wdt:P31 wd:Q5.
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

    ids_set = set()
    for result in results["results"]["bindings"]:
        ids_set.add(result['o']['value'])
        # print(result['o']['value'])
        # print(result.keys())
        # print(type(result))

    return ids_set


def query_orcid(orcid_id="0000-0001-5458-8645", institution_key="APP-ZON9G76T8090XGSI",
                institution_secret="fe8d3704-73ce-4b77-a4fa-c45df8ce454c", sandbox=False, authorization_code="PzS8tv",
                redirect_uri="https://aifb.kit.edu&code=PzS8tv"):
    # KN:
    # 0000-0002-4916-9443
    # code=PzS8tv
    # curl -i -L -k -H 'Accept: application/json'
    # --data 'client_id=APP-ZON9G76T8090XGSI
    # client_secret=fe8d3704-73ce-4b77-a4fa-c45df8ce454c
    # grant_type=authorization_code
    # redirect_uri=https://aifb.kit.edu&code=PzS8tv' https://orcid.org/oauth/token
    api = orcid.MemberAPI(institution_key, institution_secret, sandbox=False)
    token = api.get_token(user_id=institution_key, password=institution_secret, redirect_uri=redirect_uri)
    # get_token_from_authorization_code(authorization_code,
    #                                           redirect_uri)
    search_results = api.search_public('text:English')
    # Get the summary
    summary = api.read_record_public(orcid_id, 'activities',
                                     token)
    summary = api.read_record_public(orcid_id, 'record',
                                     token)
    print(summary)


def get_titles(persons_dict):
    fetching_functions = {
        "VIAF": viaf.paper_titles_for_id,
        "ACM Digital Library": acm.paper_titles_for_id,
        "Dimensions": dimensions.paper_titles_for_id,
        "DBLP": dblp.paper_titles_for_id,

    }
    titles = {}
    for person in persons_dict.keys():
        titles[person] = {}
        for database in persons_dict[person].keys():
            if database not in fetching_functions.keys():
                continue
            titles_for_database = []
            for database_id in persons_dict[person][database]:
                titles_for_database.append(fetching_functions[database](database_id))
            titles[person][database] = titles_for_database
    return titles


if __name__ == '__main__':
    """
    Idea: Query Wikidata with a person's identifier (e.g. "Q57231890") and find their publications from other related 
                                                                    platforms via getting their IDs for said platforms
    """

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
    print(get_titles(persons_dict=persons_dict))

    # Now we've got our IDs - time to query the other endpoints
    query_orcid()
