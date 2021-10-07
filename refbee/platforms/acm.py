from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def paper_titles_for_id(person_id, selenium_path=None#"/usr/local/bin/geckodriver"
                        ):

    options = Options()
    options.headless = True
    headers = {}
    url = f'https://dl.acm.org/profile/{person_id}/publications?Role=author&startPage=0&pageSize=999999'
    driver = webdriver.Firefox(options=options, executable_path=selenium_path)
    driver.get(url)
    html = driver.page_source
    driver.close()
    soup = BeautifulSoup(html, "html.parser")

    titles = []
    for li in soup.find_all('li', {'class' : 'search__item issue-item-container'}):
        titles.append(li.find_all('h5')[0].text.replace('\n                    ', ''))

    return titles
    
# print(paper_titles_for_id(81314486580))

