##########
# Script to import washington-post news article dump
#
##########

from datetime import datetime
from bs4 import BeautifulSoup
import requests
import json
import time
import urllib.parse
import sys
sys.path.insert(0, '../../../../')

from entity_extraction import extract_entities

# if os.environ.get('ENVIRONMENT') == 'local':
# if 1:
#     url = 'http://nginx:80/articles'
# else:
url = 'http://django-l422finlayproject.ida.dcs.gla.ac.uk/articles'


def crawl_articles():
    with open('./TREC_Washington_Post_collection.v2.jl.fix.json') as articles_file:
        articles = []
        counter = 0
        for line in articles_file:
            articles.append(json.loads(line))
            counter += 1
            if counter == 30:
                new_wp = loop_articles(articles, 'washington-post')
                r = requests.post(url + '/', json={'articles': new_wp})
                print(r.status_code)
                counter = 0
                articles = []


def loop_articles(articles, source):
    new_articles = []

    for a in articles:
        article_url = a['article_url']
        print(article_url)
        if not article_url or url_exists(article_url):
            continue

        body = parse_article(a['contents'])
        print(body)
        if not body:
            continue
        assets = extract_entities(str(body))

        while len(str(body)) > 15450:
            body = body[:-2]

        body = json.dumps(dict(enumerate(body)))
        print(body)
        new_articles.append(
            {
                'title': a['title'],
                'author': a['author'],
                'source': 'the-washington-post',
                'body': body,
                'url': article_url,
                'published': datetime.fromtimestamp(int(a['published_date'])/1000).strftime('%Y-%m-%d'),
                'assets': assets
            }
        )
    return new_articles


def parse_article(content):
    lines = []
    for line in content:
        if line['type'] == 'sanitized_html':
            soup = BeautifulSoup(line['content'], 'html.parser')
            lines.append(soup.text)
    return lines


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
