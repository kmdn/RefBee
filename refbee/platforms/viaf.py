import urllib.request
import json


def paper_titles_for_id(person_id):

    url = f'https://viaf.org/viaf/{person_id}/viaf.json'
    output = json.load(urllib.request.urlopen(url))
    if "titles" not in output.keys():
        return None
    titles = [x['title'] for x in output['titles']['work']]
    return titles

# print(paper_titles_for_id(4412150085882215060005))
