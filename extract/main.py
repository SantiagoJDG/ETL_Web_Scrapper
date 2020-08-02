import argparse
import logging
import datetime
import csv
logging.basicConfig(level=logging.INFO)
import re

from requests.exceptions import HTTPError, ConnectionError
from urllib3.exceptions import MaxRetryError

import news_page_objects as news
from common import config


logger = logging.getLogger(__name__)
is_well_formed_url = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')

def _news_scraper(news_sites):
    host = config()['news_sites'][news_sites]['url']

    logging.info('Beginning scraper for {}'.format(host))
    logging.info('Finding links in homepage...')
    homepage = news.HomePage(news_sites, host)

    articles = []
    for link in homepage.article_links:
        article = _fetch_article(news_sites, host, link)

        if article:
            logger.info('Article fetched!')
            articles.append(article)
                
    _save_articles(news_sites, articles)

def _save_articles(news_sites, articles):
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name = '{news_sites}_{datetime}_articles.csv'.format(
        news_sites=news_sites,
        datetime=now
    ) 
    
    csv_headers = list(filter(lambda property: not property.startswith('_'), dir(articles[0])))
    
    with open (out_file_name, mode='w+') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

        for article in articles:
            row = [str(getattr(article, prop)) for prop in csv_headers]
            writer.writerow(row)
            

def _fetch_article(news_sites, host, link):
    logger.info('Start fetching article at {}'.format(link))
    article = None

    try:
        article = news.ArticlePage(news_sites, _build_link(host, link))
    except (HTTPError, MaxRetryError):
        logger.warning('Error while fetching the article', exc_info=False)
    except (ConnectionError):
        pass
    
    if article and not article.body:
        logger.warning('invalid article. Theres no body')
        return None
    
    return article

def _build_link(host, link):
    
    if is_well_formed_url.match(link):
        return link 
    elif is_root_path.match(link):
        return '{}{}'.format(host, link)
    else: 
        return '{host}{uri}'.format(host=host, uri=link)
    
     

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    news_site_choices = list(config()['news_sites'].keys())
    parser.add_argument('news_site',
                        help='The news site that you want to scrape',
                        type=str,
                        choices=news_site_choices)

    args = parser.parse_args()
    _news_scraper(args.news_site)