"""smile = "\U0001F600"
print(smile)"""

import requests
import json
from config import news_api


req = requests.get(url=f'https://newsapi.org/v2/top-headlines?country=ru&category=technology&apiKey={news_api}')

print(req)
req_json = req.json()
print(req_json)
for i in range (len(req_json['articles'])):
  print(req_json['articles'][int(i)]['title'])
  print()
'''with open(file='news.json', encoding='utf-8', mode='w') as file:
  json.dump(req, file, ensure_ascii=False)
'''
