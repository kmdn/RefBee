from refbee.platforms import orcid_manual, viaf, acm, dimensions, dblp, dnb, google_scholar, semantic_scholar, microsoft_academic, wikidata

fetching_functions = {
    "VIAF": viaf.paper_titles_for_id,
    "ACM Digital Library": acm.paper_titles_for_id,
    "Dimensions": dimensions.paper_titles_for_id,
    "DBLP": dblp.paper_titles_for_id,
    "ORCID": orcid_manual.paper_titles_for_id,
    "Google Scholar": google_scholar.paper_titles_for_id,
    "Semantic Scholar": semantic_scholar.paper_titles_for_id,
    "DNB/GNB": dnb.paper_titles_for_id,
    "Microsoft Academic": microsoft_academic.paper_titles_for_id,
    "Wikidata": wikidata.paper_titles_for_id,
}


def get_titles(persons_dict):

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
                titles_for_database.extend(fetched_titles)
            titles[person][database] = list(set(titles_for_database))
    return titles
