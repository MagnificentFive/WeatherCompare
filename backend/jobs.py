import logging
from datetime import datetime, timedelta

from flask_apscheduler import APScheduler

from api_clients import news_client
from models import News, db

logger = logging.getLogger(__name__)


scheduler = APScheduler()


@scheduler.task('interval', id='update_news_from_api', seconds=24*60*60)  # every day
def update_news_from_api():
    logger.debug('Started cron task')

    with scheduler.app.app_context():
        News.query.delete()

        try:
            news = news_client.get_everything(
                q='',
                sources='bbc-news,the-verge',
                domains='bbc.co.uk,techcrunch.com',
                from_param=(datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d'),
                to=datetime.utcnow().strftime('%Y-%m-%d'),
                language='en',
                sort_by='relevancy',
                page=1
            )
            unique = set()
            for article in news['articles']:
                if article['title'] in unique:
                    continue
                else:
                    unique.add(article['title'])

                news = News(
                    dt=article['publishedAt'],
                    title=article['title'],
                    text=article['content'],
                    image_url=article['urlToImage'],
                )
                db.session.add(news)
            db.session.commit()
        except Exception as e:
            logger.error(f'Cannot get news. {e}')

    logger.debug('End cron task')
