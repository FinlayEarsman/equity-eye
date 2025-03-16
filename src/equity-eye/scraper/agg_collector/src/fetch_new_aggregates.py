##########
# Script to update the system with the most recent price data for the assets.
#
##########

import requests
import json


django_url = 'http://nginx:80/'


def get_securities():
    r = requests.get(django_url + 'assets')
    assets = r.json()
    tickers = []
    for a in assets:
        tickers.append(a['ticker'])

    return tickers

def send_graphql(query, variables = {}):
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer VLcXXf6pzsfAZ8AQ'
            }
    data = json.dumps({
        'query': query,
        'variables': variables
        })
    return requests.post('https://graph.yuzu.dev/graphql', headers=headers, data=data)

def main():
    query = """
        query AssetInfo($symbols: [String!], $date: DateTime!) {
          securities(input: { symbols: $symbols }) {
            symbol
            aggregates(input: { limit: 200, before: $date }) {
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

    # r = requests.get(django_url + 'prices/latest')
    # if not r.json()['latest']:
    #     return

    # get_aggregates_after = datetime.datetime.strptime(r.json()['latest'], '%Y-%m-%dT%H:%M:%SZ') + \
    #                        datetime.timedelta(days=1)
    # print(get_aggregates_after)
    tickers = get_securities()

    response = send_graphql(query, variables={ 'symbols': tickers, 'date': "2022-02-14"})
    json_data = json.loads(response.text)
    print(json_data)
    return
    if json_data['data']:
        asset_data = json_data['data']['securities']

        for asset in asset_data:
            new_aggregate = [{
                "ticker": asset['symbol'],
                "aggregates": asset['aggregates']
            }]

            r = requests.post(django_url + 'prices/', json={'asset_aggregates': new_aggregate})

if __name__ == "__main__":
    main()
