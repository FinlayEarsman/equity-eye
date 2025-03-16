############
# Web scraper for Business Insider articles
#
############

from newsapi import NewsApiClient


def get_business_insider_articles(api_key):
    newsapi = NewsApiClient(api_key=api_key)
    response = newsapi.get_everything(
                                      q='technology OR markets OR business',
                                      sources='business-insider',
                                      sort_by='publishedAt'
                                      )
    return response['articles']

def scrape_business_insider(soup):
    body = []
    content = soup.find('div', attrs={'class': 'content-lock-content'})

    if content:
        for t in content.findAll("p"):
            try:
                text = t.getText()
                if len(text) > 0:
                    body.append(text)
            except ValueError as e:
                print('error: ', e)
                pass

    if len(body) == 0:
        return None

    return body

# if __name__ == "__main__":
#     get_business_insider_articles()