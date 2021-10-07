from refbee.platforms import platform_names
from refbee.platforms.wikidata import platform_ids_for_person
from refbee.disambiguation import disambiguate_titles
from refbee.fetching import get_titles_parallel as get_titles


def query(wd_person_id):
    
    # begin by fetching platform specific ids for person from wikidata entry
    persons_dict = platform_ids_for_person(wd_person_id)

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
            for title in person_titles_dict[platform]:
                print("Paper: ", title)
                paper_id = title
                # add info for the specific paper
                paper_dict = papers_dict.get(paper_id, {})
                papers_dict[paper_id] = paper_dict
                paper_dict["title"] = title
                paper_dict[platform] = 1
    # add 0-count platforms to the returned JSON
    for person in ret_json:
        for paper in ret_json[person]:
            for platform_not_found in set.difference(set(platform_names), set(ret_json[person][paper].keys())):
                ret_json[person][paper][platform_not_found] = 0
    
    # disambiguate titles
    for person in ret_json:
        ret_json[person] = disambiguate_titles(ret_json[person])
    print("Returned JSON: ", ret_json)
    return ret_json

