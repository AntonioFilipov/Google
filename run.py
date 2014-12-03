from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from website import Website
from connect import Base
#import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

basic_websites = []
sub_domein_pages = []
visited_urls = []


def visited_url(page):
    visited_urls.append(page)


def page_crawer(session, domein, domein_length, page):
    websites = []
    sub_pages = []
    r = requests.get(page)
    html = r.text
    soup = BeautifulSoup(html)

    for link in soup.find_all('a'):
        if link.get('href') is not None and '#' not in link.get('href'):
            websites.append(link.get('href'))
    for item in websites:
        if item[:4] != 'http':
            a = urljoin(domein, item)
            sub_pages.append(a)
        if item[:domein_length] == domein:
            sub_pages.append(item)

    for pages in sub_pages:
        description = get_description(soup)
        title = get_title(soup)
        page_domein = get_domein(domein, pages)
        if pages not in visited_urls:
            print(pages)
            visited_urls.append(pages)
            push_to_database(session, pages, description, title, page_domein)
            page_crawer(session, domein, domein_length, pages)


def push_to_database(session, site, page_description, page_title, page_domein):
    my_site = Website(url=site, title=page_title, description=page_description, domain=page_domein, pages_count=3, html_version="")
    session.add(my_site)
    session.commit()


def get_description(soup):
    for link in soup.find_all('meta'):
        if link.get('name') == "description":
            if link.get('content') != "":
                return link.get('content')
        else:
            return "None"


def get_title(soup):
    if soup.find('title') is not None:
        for link in soup.find('title'):
            return link


def get_domein(domein, page):
    if page[:len(domein)] == domein:
        return domein







def main():
    domein = 'http://www.framar.bg/'
    domein_length = len(domein)
    r = requests.get(domein)
    html = r.text
    soup = BeautifulSoup(html)
    engine = create_engine("sqlite:///cinema.db")
    Base.metadata.create_all(engine)
    session = Session(bind=engine)

    for link in soup.find_all('a'):
        basic_websites.append(link.get('href'))

    for item in basic_websites:
        if item[:4] != 'http':
            a = urljoin(domein, item)
            sub_domein_pages.append(a)
        if item[:domein_length] == domein:
            sub_domein_pages.append(item)
    visited_urls.append(domein+'/')
    visited_urls.append(domein+'#')
    visited_urls.append(domein)
    # count = 0
    for sub_page in sub_domein_pages:
    #     count += 1
        #print (sub_page)
        if sub_page not in visited_urls:
            visited_url(sub_page)
            page_crawer(session, domein, domein_length, sub_page)


if __name__ == '__main__':
    main()