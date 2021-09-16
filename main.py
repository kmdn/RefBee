# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
import orcid_manual
from SPARQLWrapper import SPARQLWrapper, JSON
import viaf
import acm
import dimensions
import dblp
import google_scholar
import semantic_scholar
import microsoft_academic


def get_sparql_query_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


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


def wikidata_paper_titles_for_id(person_id="Q57231890"):
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


def get_titles(persons_dict):
    fetching_functions = {
        "VIAF": viaf.paper_titles_for_id,
        "ACM Digital Library": acm.paper_titles_for_id,
        "Dimensions": dimensions.paper_titles_for_id,
        "DBLP": dblp.paper_titles_for_id,
        "ORCID": orcid_manual.paper_titles_for_id,
        "Google Scholar": google_scholar.paper_titles_for_id,
        "Semantic Scholar": semantic_scholar.paper_titles_for_id,
        "Microsoft Academic": microsoft_academic.paper_titles_for_id,
        "Wikidata": wikidata_paper_titles_for_id,
    }
    titles = {}
    for person in persons_dict.keys():
        titles[person] = {}
        for database in persons_dict[person].keys():
            if database not in fetching_functions.keys():
                continue
            titles_for_database = []
            for database_id in persons_dict[person][database]:
                fetched_titles = fetching_functions[database](database_id)
                if fetched_titles is None:
                    continue
                titles_for_database.extend(fetching_functions[database](database_id))
            titles[person][database] = list(set(titles_for_database))
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
        "Microsoft Academic": "wdt:P6366",
        "Semantic Scholar": "wdt:P4012",
        "DNB/GNB": "wdt:P227",
        "ACM Digital Library": "wdt:P864"
    }

    wd_person_id = "Q57231890"
    persons_dict = {
        wd_person_id: {"Wikidata": wd_person_id}
    }
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

    # Now we've got our IDs - time to query the other endpoints
    grouped_titles_dict = get_titles(persons_dict=persons_dict)

    ret_json = {}
    for person in grouped_titles_dict:
        # new person - add it to our data structure <3
        papers_dict = ret_json.get(person, {})
        # for default behaviour
        ret_json[person] = papers_dict
        # get a person along with its currently-associated titles
        person_titles_dict = grouped_titles_dict[person]
        for platform in person_titles_dict:
            # print("Platform: ", platform)
            for titles in person_titles_dict[platform]:
                for title in titles:
                    # print("Paper: ", title)
                    paper_id = title
                    # add info for the specific paper
                    paper_dict = papers_dict.get(paper_id, {})
                    papers_dict[paper_id] = paper_dict
                    paper_dict["title"] = title
                    paper_dict[platform] = 1

    # add 0-count platforms to the returned JSON
    for person in ret_json:
        for paper in ret_json[person]:
            for platform_not_found in set.difference(set(platform_properties_dict.keys()), set(ret_json[person][paper].keys())):
                ret_json[person][paper][platform_not_found] = 0
    print("Returned JSON: ", ret_json)

    """
    Currently: 'title': '<paper1>' may be removed due to title being used as paper key - may change in future ;)
        return format: 
        { '<wd_person_id>': { '<paper1>': {   'title': '<paper1>', 
                                            '<platform1>': 0, 
                                            '<platform2>': 1, ...,
                             '<paper2>': {...} 
                            }
        }
        ...
    """
