import urllib.request
import json


def paper_titles_for_id(person_id):

    url = f'https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?expr=Composite(AA.AuId={person_id})&attributes=DN&subscription-key=a6f4e6b22dd9422cb40d0e8c2ef8eb3c&count=99999999'
    output = json.load(urllib.request.urlopen(url))
    titles = [x['DN'] for x in output['entities']]
    return titles

# print(paper_titles_for_id(2105886198))