import urllib.request
from lxml import etree


def retrieve_titles(input_xml=""):
   # print(str(input_xml.read()))
    root = etree.XML(input_xml.read())
    #print(dir(root))
    # print(root.getchildren())
    titles = set()
    for element in root.iter():
        #print("Element: %s %s" % (element.tag, ''.join(element.itertext())))
        if element.tag == "title":
            titles.add(''.join(element.itertext()))
    return list(titles)


def paper_titles_for_id(person_id):
    url = f'https://dblp.org/pid/{person_id}.xml'
    # print("URL:", url)
    titles = retrieve_titles(input_xml=urllib.request.urlopen(url))
    return titles

