import urllib.request
import json
import html


def paper_titles_for_id(person_id):

    url = f'https://app.dimensions.ai/discover/publication/results.json?and_facet_researcher=ur.{person_id}'
    output = json.load(urllib.request.urlopen(url))
    titles = [html.unescape(x['title']) for x in output['docs']]
    return titles

# print(paper_titles_for_id("010763216510.13"))

