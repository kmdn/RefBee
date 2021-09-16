import urllib.request
import feedparser


def paper_titles_for_id(person_id):

    NewsFeed = feedparser.parse(f"feed:https://portal.dnb.de/opac.atom?currentResultId=auRef%3D{person_id}%26any&method=search")
    links = [x['link'] for x in NewsFeed.entries]

    titles = []
    for link in links:
        url = link + "/about/lds"
        titles.append(urllib.request.urlopen(url).read().decode('utf-8').split("dc:title \"")[1].split("\";")[0])
    titles = list(set(titles))

    return titles

# print(paper_titles_for_id(1137017686))
