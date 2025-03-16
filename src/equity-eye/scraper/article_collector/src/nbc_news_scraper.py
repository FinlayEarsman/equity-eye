############
# Web scraper for NBC news articles
#
############

from newsapi import NewsApiClient


def get_nbc_news_articles(api_key):
    newsapi = NewsApiClient(api_key=api_key)
    response = newsapi.get_everything(
                                      q='markets OR business OR technology',
                                      sources='nbc-news',
                                      sort_by='publishedAt'
                                      )
    return response['articles']

def scrape_nbc_news(soup):
    body = []
    content = soup.findAll('div', attrs={'class': 'article-body__content'})

    for div in content:
        paras = div.findAll('p')
        for p in paras:
            try:
                text = p.getText()
                if len(text) > 0:
                    body.append(text)
            except ValueError as e:
                print('error: ', e)
                pass

    if len(body) == 0:
        return None

    return body

# if __name__ == "__main__":
#     get_nbc_news_articles(api_key = '44b49f76413a44bf8a4d26d18336f5c6')