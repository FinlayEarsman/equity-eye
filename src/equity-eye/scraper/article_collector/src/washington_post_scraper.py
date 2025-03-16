############
# Web scraper for Washington Post news articles
#
############

from newsapi import NewsApiClient


def get_washington_post_articles(api_key):
    newsapi = NewsApiClient(api_key=api_key)
    response = newsapi.get_everything(
                                      q='markets OR business OR technology',
                                      sources='the-washington-post',
                                      sort_by='publishedAt'
                                      )
    return response['articles']

def scrape_washington_post(soup):
    body = []
    for t in soup.findAll('div', attrs={'class': 'article-body'}):
        try:
            text=""
            if t.find("p"):
                text = t.find("p").getText()
            if len(text) > 0:
                body.append(text)
        except ValueError as e:
            print('error: ', e)
            pass

    if len(body) == 0:
        return None

    return body

# if __name__ == "__main__":
#     get_washington_post_articles()