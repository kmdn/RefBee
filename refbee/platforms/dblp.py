import urllib.request
from xml.etree.ElementTree import ElementTree

from lxml import etree
import pprint


def retrieve_titles(input_xml=""):
    root = etree.XML(input_xml.read())
    #print(dir(root))
    print(root.getchildren())
    titles = set()
    for element in root.iter():
        if element.tag == "title":
            titles.add(element.text)
            #print("Element: %s %s " % (element.tag, element.text))
    return list(titles)


def paper_titles_for_id(person_id):
    url = f'https://dblp.org/pid/{person_id}.xml'
    print("URL:", url)
    titles = retrieve_titles(input_xml=urllib.request.urlopen(url))
    return titles

