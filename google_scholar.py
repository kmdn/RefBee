# https://scholar.google.de/citations?hl=de&user=Tzu2z8UAAAAJ&cstart=100&pagesize=200

import requests
from pprint import pprint
from bs4 import BeautifulSoup

'''
Get publications as BeautifulSoup Python Objects.
'''
def get_pubs(user, cstart):
    uri = f'https://scholar.google.de/citations?hl=de&user={user}&cstart={cstart}&pagesize=100'
    page = requests.get(uri)
    soup = BeautifulSoup(page.content, 'html.parser')
    pubs = soup.find_all('tr', class_='gsc_a_tr')
    return pubs

'''
Get the publication information.

    @return (year, info as string array)
'''
def get_pub_info(pub):
    try:
        pub_title = pub.findChildren('td', class_='gsc_a_t')
        pub_title_infos = pub_title[0].findChildren()
        pub_year = pub.findChildren('td', class_='gsc_a_y')
        return pub_year[0].get_text(), [pub_title_info.get_text() for pub_title_info in pub_title_infos]
    except:
        return -1, []

'''
Get the publication information for the input user.

    @return (year, info as string array)
'''
def get_google_scholar_publications(user):
    # user = 'Tzu2z8UAAAAJ'
    # 'Tzu2z8UAAAAJ'
    # yL_3D4oAAAAJ
    cstart=0
    pub_infos = []
    while True:
        pubs = get_pubs(user, cstart)
        pub_infos.extend([ get_pub_info(pub) for pub in pubs])
        cstart+=100
        #pprint(pub_infos[-1])
        if pub_infos[-1][0] == -1:
            pub_infos = pub_infos[:-1]
            break
    return pub_infos
