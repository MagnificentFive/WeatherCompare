import unittest
import requests_mock
from backend.test_news import get_news

class TestNews(unittest.TestCase):

    def test_get_news(self):
        with requests_mock.mock() as m:
            
            mock_response = {
                'status': 'ok',
                'articles': [
                    {'title': 'Test Article 1'},
                    {'title': 'Test Article 2'}
                ]
            }
            m.get('https://newsapi.org/v2/top-headlines', json=mock_response)

            result = get_news()

            self.assertEqual(result, ['Test Article 1', 'Test Article 2'])

if __name__ == '__main__':
    unittest.main()
