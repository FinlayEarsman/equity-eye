############
# Main script for the article collection process
# Calls the subsequent sources to collect and scrape articles then passes
# them to be processed
# Sends articles to REST API
############

from bs4 import BeautifulSoup
import requests
import json
import time
import urllib.parse

from bbc_scraper import get_bbc_articles, scrape_bbc
from washington_post_scraper import get_washington_post_articles, \
    scrape_washington_post
from financial_post_scraper import get_financial_post_articles, \
    scrape_financial_post
from nbc_news_scraper import get_nbc_news_articles, scrape_nbc_news
from business_insider_scraper import get_business_insider_articles, \
    scrape_business_insider

from entity_extraction import extract_entities


url = 'http://nginx:80/articles'

api_key = '44b49f76413a44bf8a4d26d18336f5c6'


def crawl_articles():
    bbc_articles = get_bbc_articles(api_key)
    washington_articles = get_washington_post_articles(api_key)
    bus_insider_articles = get_business_insider_articles(api_key)
    nbc_articles = get_nbc_news_articles(api_key)
    financial_post_articles = get_financial_post_articles(api_key)

    new_bbc = loop_articles(bbc_articles, 'bbc')
    new_insider = loop_articles(bus_insider_articles, 'business-insider')
    new_nbc = loop_articles(nbc_articles, 'nbc')
    new_wp = loop_articles(washington_articles, 'washington-post')
    new_fp = loop_articles(financial_post_articles, 'financial-post')

    r = requests.post(url + '/', json={'articles': new_bbc})
    print(r.status_code)

    r = requests.post(url + '/', json={'articles': new_wp})
    print(r.status_code)

    r = requests.post(url + '/', json={'articles': new_insider})
    print(r.status_code)

    r = requests.post(url + '/', json={'articles': new_nbc})
    print(r.status_code)

    r = requests.post(url + '/', json={'articles': new_fp})
    print(r.status_code)


def loop_articles(articles, source):
    new_articles = []

    for a in articles:
        url = a['url']
        if not url or url_exists(url):
            continue

        print('fetching: %s' % url)
        body = scrape_article(url, source)
        if not body:
            continue
        assets = extract_entities(body)

        while len(str(body)) > 15450:
            body = body[:-2]

        body = json.dumps(dict(enumerate(body)))

        new_articles.append(
            {
                'title': a['title'],
                'author': a['author'],
                'source': a['source']['Id'],
                'body': body,
                'url': url,
                'published': time.strftime("%Y-%m-%d", time.strptime(a['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')),
                'assets': assets
            }
        )
    return new_articles


def scrape_article(article_url, source):
    try:
        request = requests.get(article_url,
                               headers={'User-agent': 'Mozilla/5.0'})
    except requests.exceptions.RequestException:
        print("failed: %s" % article_url)
        return None

    html = request.content
    soup = BeautifulSoup(html, 'html.parser')

    match source:
        case 'bbc':
            return scrape_bbc(soup)
        case 'business-insider':
            return scrape_business_insider(soup)
        case 'nbc':
            return scrape_nbc_news(soup)
        case 'washington-post':
            return scrape_washington_post(soup)
        case 'financial-post':
            return scrape_financial_post(soup)
        case _:
            return None


def url_exists(article_url):
    new_url = urllib.parse.quote(article_url)
    r = requests.get(url + '/' + new_url)
    if 'not-exists' in r.json().keys():
        print('not exists')
        return False
    print(article_url + ' exists')
    return True


if __name__ == '__main__':
    time.sleep(1)
    crawl_articles()
