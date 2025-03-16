##########
# Processing pipeline for extracting entities from articles and 
# linking them to the ones in the system
#
##########

import spacy
import requests
from fuzzywuzzy import fuzz

url = 'http://nginx:80/assets'


def extract_entities(text):
    text = ''.join(text)
    assets = fetch_assets()

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    tickers = []
    for e in doc.ents:
        if e.label_ == 'ORG':
            res = best_asset(e.text, assets)
            if res:
                tickers.append(res)
    return list(set(tickers))


def fetch_assets():
    r = requests.get(url)
    assets = r.json()['assets']
    names = []
    for a in assets:
        names.append(a['name'])

    return names


def best_asset(entity, asset_names):
    best = ""
    for a in asset_names:
        ratio = fuzz.token_set_ratio(entity.lower(), a.lower())
        if ratio == 100:
            return a
        elif ratio > 90:
            best = a
    return best
