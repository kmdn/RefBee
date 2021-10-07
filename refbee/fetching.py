from refbee.platforms import orcid_manual, viaf, acm, dimensions, dblp, dnb, google_scholar, semantic_scholar, microsoft_academic, wikidata
from multiprocessing import Process, Manager
import time


fetching_functions = {
    "VIAF": viaf.paper_titles_for_id,
    #"ACM Digital Library": acm.paper_titles_for_id,
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
    start = time.time()

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

    end = time.time()
    print(f"(Sequential) title fetching completed in: {end - start:.2f} seconds")
    return titles


def get_titles_parallel(persons_dict):
    start = time.time()

    titles = {}
    for person in persons_dict.keys():
        manager = Manager()
        titles[person] = manager.dict()

        job = [Process(target=fetch_from_database, args=(titles[person], i, persons_dict[person])) for i in persons_dict[person].keys()]
        _ = [p.start() for p in job]
        _ = [p.join() for p in job]
    end = time.time()
    print(f"(Parallel) title fetching completed in: {end - start:.2f} seconds")
    return titles

def fetch_from_database(write_to, database, databases_for_person):
    try:
        start = time.time()
        if database not in fetching_functions.keys():
            return None
        titles_for_database = []
        for database_id in databases_for_person[database]:
            fetched_titles = fetching_functions[database](database_id)
            if fetched_titles is None:
                continue
            titles_for_database.extend(fetched_titles)
        write_to[database] = list(set(titles_for_database))
        end = time.time()
        print(f"Fetch time {database}: {end - start:.2f} seconds")
    except:
        print(f"WARNING: Problems while fetching from {database}!")
