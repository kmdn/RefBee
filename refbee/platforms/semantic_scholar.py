import urllib.request
import json


def paper_titles_for_id(person_id):

    url = f'https://api.semanticscholar.org/graph/v1/author/{person_id}?fields=papers.title'
    output = json.load(urllib.request.urlopen(url))
    titles = [x['title'] for x in output['papers']]
    return titles

# print(paper_titles_for_id(1808632))
