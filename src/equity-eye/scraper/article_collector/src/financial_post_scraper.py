############
# Web scraper for Financial Post articles
#
############

from newsapi import NewsApiClient


def get_financial_post_articles(api_key):
    newsapi = NewsApiClient(api_key=api_key)
    response = newsapi.get_everything(
                                      q='markets OR business OR technology',
                                      sources='financial-post',
                                      sort_by='publishedAt'
                                      )
    return response['articles']

def scrape_financial_post(soup):
    body = []

    for s in soup.findAll('section', attrs={'class': 'article-content__content-group'}):
        for p in s.findAll('p'):
            try:
                text = p.getText().strip()
                if text:
                    body.append(text)
            except ValueError as e:
                print('error: ', e)
                pass

    if len(body) == 0:
        return None

    return body

# if __name__ == "__main__":
#     get_financial_post_articles()