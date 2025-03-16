##########
# Script that initalises the database with the S&P 500 assets and their price data
# Note: yuzu was deprecated recently so needs ammending
#
##########

import requests
import json
import datetime
from bs4 import BeautifulSoup
import re
import os


django_url = 'http://nginx:80/'


api_url = 'https://graph.yuzu.dev/graphql'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer VLcXXf6pzsfAZ8AQ'
}


def get_securities():
    # get the HTML content from the webpage
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # find the table containing the ticker symbols
    table = soup.find('table', {'class': 'wikitable sortable'})

    # extract the ticker symbols from the table
    securities = {}
    tickers = []
    for row in table.find_all('tr')[1:]:
        ticker = row.find_all('td')[0].text.strip('\n')
        name = row.find_all('td')[1].text.strip('\n')
        asset_url = row.find_all('td')[1].find('a')['href']
        securities[ticker] = (name, asset_url)
        tickers.append(ticker)
    return securities, tickers


def get_aggregates(date, tickers):
    response = send_graphql(variables={'symbols': tickers, 'date': date.isoformat()})

    data = json.loads(response.text)
    if data['data']:
        return data['data']['securities']
    else:
        return []


def send_graphql(variables={}):
    query = """
        query AssetInfo($symbols: [String!], $date: DateTime!) {
          securities(input: { symbols: $symbols }) {
            symbol
            aggregates(input: {limit: 365, after: $date }) {
              time
              open
              high
              low
              close
              volume
            }
          }
        }
    """
    data = json.dumps({
        'query': query,
        'variables': variables
    })
    return requests.post(api_url, headers=headers, data=data)


def make_assets(all_securities, tickers):
    new_assets = []
    for asset in tickers:
        url = f'https://en.wikipedia.org{all_securities[asset][1]}'
        print(url)
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        content = soup.find('table', attrs={'class': 'infobox'})
        summary = ''
        if content:
            tag = content.next_sibling
            while tag.name != 'p':
                tag = tag.next_sibling

            first_p = tag
            print(first_p.text)
            while not first_p.text.strip():
                first_p = first_p.find_next("p")
                if not first_p:
                    break
            summary = re.sub('\[.*?\]', '', first_p.text)
            # print(summary)

        new_assets.append({
            'name': all_securities[asset][0],
            'ticker': asset,
            'summary': summary,
        })

    r = requests.post(django_url + 'assets/', json={'assets': new_assets})


def process_aggregates(aggs):
    counter = 0
    new_aggregates = []
    for asset in aggs:
        new_aggregates.append({
            'ticker': asset['symbol'],
            'aggregates': asset['aggregates']
        })
        counter += 1
        if counter == 100:
            r = requests.post(django_url + 'prices/', json={'asset_aggregates': new_aggregates})
            counter = 0
            new_aggregates = []


def main():
    all_securities, tickers = get_securities()
    make_assets(all_securities, tickers)
    now = datetime.datetime.now()
    year_interval = datetime.timedelta(days=365)

    collect_from = now - year_interval
    agg1 = get_aggregates(collect_from, tickers)
    process_aggregates(agg1)

    # collect_from = collect_from - year_interval
    # agg2 = get_aggregates(collect_from, tickers)
    # process_aggregates(agg2)


if __name__ == '__main__':
    main()
