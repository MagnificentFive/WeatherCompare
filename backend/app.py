import logging

from flask import Flask
from flask import jsonify
from flask_migrate import Migrate
from flask_caching import Cache

from jobs import scheduler
from models import db, News
from config import *
from api_clients import get_weather


logger = logging.getLogger(__name__)


# flask app
config = {
    'DEBUG': DEBUG,
    'SQLALCHEMY_DATABASE_URI': SQLALCHEMY_DATABASE_URI,
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
}


app = Flask(__name__)
app.config.from_mapping(config)

# db and migration
db.init_app(app)
migrate = Migrate(app, db)

# caching
cache = Cache(app)

# scheduler
scheduler.init_app(app)
scheduler.start()


@app.route('/news')
def news():
    try:
        result = []
        for news in News.query.order_by(News.dt.desc()).limit(10).all():
            result.append({
                'dt': news.dt,
                'title': news.title,
                'text': news.text,
                'image_url': news.image_url,
            })
        return jsonify(success=True, result=result)
    except Exception as e:
        logger.error(f'Не удалось получить новости. Ошибка: {e}')
        return jsonify(success=False)


@app.route('/weather/<string:city>', methods=('GET',))
def weather(city):
    try:
        result = get_weather(city)
        return jsonify(success=True, result=result)
    except Exception as e:
        logger.error(f'Не удалось получить погоду для города {city}. Ошибка: {e}')
        return jsonify(success=False)


if __name__ == '__main__':
    app.run()
