#################
# This script was used to collect articles from Aylien and send them
# to the Django REST API on the cluster. This was to support the evaluation
# as there was not enough articles from the past to test certain functionality.
#################

import json
import requests
import time
import sys

sys.path.insert(0, '../../../../')
from entity_extraction import extract_entities
from main_scraper import url_exists

url = 'http://django-l422finlayproject.ida.dcs.gla.ac.uk/articles'
asset_url = 'http://django-l422finlayproject.ida.dcs.gla.ac.uk/assets'

def main():
    cur_cursor = "*"
    data = api_call(cur_cursor)
    print(data)
    next_cursor = data['next_page_cursor']
    process_articles(data["stories"])
    while next_cursor != cur_cursor:
        data = api_call(next_cursor)
        cur_cursor = next_cursor
        next_cursor = data['next_page_cursor']
        new = process_articles(data["stories"])
        r = requests.post(url + '/', json={'articles': new})
        print(r.status_code)
        time.sleep(4)


def process_articles(articles):
    new_articles = []
    all_assets = fetch_assets()

    for a in articles:
        if url_exists(a['links']['permalink']):
            continue

        assets = extract_entities(a['body'], all_assets)
        body = json.dumps({"0": a['body']})

        new_articles.append(
            {
                'title': a['title'],
                'author': a['author']['name'],
                'source': a['source']['name'],
                'body': body,
                'url': a['links']['permalink'],
                'published': time.strftime("%Y-%m-%d", time.strptime(a['published_at'], '%Y-%m-%dT%H:%M:%SZ')),
                'assets': list(assets)
            }
        )
    print(new_articles)
    return new_articles

# makes call to API using the given URL and continues querying with a new
# cursor until there is no more articles to be processed.
def api_call(cursor):
    ay_url = 'https://api.aylien.com/news/stories?aql=language:(en) AND ' \
             'entities:({{id:Q312 AND overall_prominence:>=0.65}}) AND ' \
             'source.name.keyword:("The Washington Post" OR "CNBC" OR ' \
             '"Market Watch" OR "Wall Street Journal" OR "BBC" OR "Financial '\
             'Post" OR "Business Insider" OR "Bloomberg") AND ' \
             'sentiment.title.polarity:(negative neutral ' \
             'positive)&cursor=%s&published_at.end=2023-02-17T00:00:00Z' \
             '&published_at.start=2023-01-27T00:00:00Z' % cursor

    payload = {}
    headers = {
        'X-Application-ID': '6af931f4',
        'X-Application-Key': 'f936478ea019b835ba71a887c5565ebb'
    }

    response = requests.request("GET", ay_url, headers=headers, data=payload)
    return response.json()

def fetch_assets():
    r = requests.get(asset_url)
    assets = r.json()['assets']
    names = []
    for a in assets:
        names.append(a['name'])

    return names


if __name__ == "__main__":
    main()
