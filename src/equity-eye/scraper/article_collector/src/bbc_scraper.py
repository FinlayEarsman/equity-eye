############
# Web scraper for BBC articles
#
############

from newsapi import NewsApiClient

def get_bbc_articles(api_key):
    newsapi = NewsApiClient(api_key=api_key)
    response = newsapi.get_everything(
                                      q='markets OR business OR technology',
                                      sources='bbc-news',
                                      sort_by='publishedAt',
                                      )
    return response['articles']


def scrape_bbc(soup):
    body = []
    for t in soup.findAll('div', attrs={'data-component': 'text-block'}):
        try:
            text = t.find("p").getText()
            if len(text) > 0:
                body.append(text)
        except ValueError as e:
            print('error: ', e)
            pass

    if len(body) == 0:
        return None

    return body
