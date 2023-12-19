import os

DEBUG = os.getenv('DEBUG', '1') == '1'
OPEN_WEATHER_TOKEN = os.getenv('OPEN_WEATHER_TOKEN', '')
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN', '')
NEWS_TOKEN = os.getenv('NEWS_TOKEN', '')  # 'a128de079faa43e79575301d9c8a296d'
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///project.db' if DEBUG else '')
