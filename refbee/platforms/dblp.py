import urllib.request
from xml.etree.ElementTree import ElementTree

import re
from lxml import etree
import pprint


def retrieve_titles(input_xml=""):
   # print(str(input_xml.read()))
    root = etree.XML(input_xml.read())
    #print(dir(root))
    # print(root.getchildren())
    p = re.compile(r'<.*?>')
    titles = set()
    for element in root.iter():
        #print("Element: %s %s" % (element.tag, element.text))
        if element.tag == "title":
            # titles.add(element.text)
            titles.add(p.sub('', str(etree.tostring(element).decode("utf-8"))))
            # print("Element: %s %s %s %s" % (element.tag, element.text, p.sub('', str(etree.tostring(element).decode("utf-8"))), [e.text for e in element.iter()]))
    return list(titles)


def paper_titles_for_id(person_id):
    url = f'https://dblp.org/pid/{person_id}.xml'
    # print("URL:", url)
    titles = retrieve_titles(input_xml=urllib.request.urlopen(url))
    return titles

