# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session
# from website import Website
#from connect import Base
import time
#import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

basic_websites = []
sub_domein_pages = []
visited_urls = []


def visited_url(page):
    visited_urls.append(page)


def page_crawer(domein, domein_length, page):
    websites = []
    sub_pages = []
    r = requests.get(page)
    html = r.text
    soup = BeautifulSoup(html)

    for link in soup.find_all('a'):
        if link.get('href') is not None:
            websites.append(link.get('href'))
    for item in websites:
        #print ('{}++', item)
        if item[:domein_length] != domein and item[:4] != 'http':
            a = urljoin(domein, item)
            sub_pages.append(a)

    for pages in sub_pages:
        if pages not in visited_urls:
            print(pages)
            visited_urls.append(pages)
            page_crawer(domein, domein_length, pages)

def main():
    domein = 'http://hackbulgaria.com'
    domein_length = len(domein)
    r = requests.get(domein)
    html = r.text
    soup = BeautifulSoup(html)

    for link in soup.find_all('a'):
        basic_websites.append(link.get('href'))

    for item in basic_websites:
        #print (item)
        if len(item) > 1:
            if item[:domein_length] != domein and item[:4] != 'http':
                sub_domein_pages.append(domein+item)
    visited_urls.append(domein+'/')
    visited_urls.append(domein+'#')
    visited_urls.append(domein)
    count = 0
    for sub_page in sub_domein_pages:
        print("=========================")
        print (sub_page)
        count += 1
        print("=========================")
        if sub_page not in visited_urls:
            visited_url(sub_page)
            page_crawer(domein, domein_length, sub_page)
        # if count == 3:
        #     break

    # # engine = create_engine("sqlite:///cinema.db")
    # # Base.metadata.create_all(engine)
    # # session = Session(bind=engine)
if __name__ == '__main__':
    main()