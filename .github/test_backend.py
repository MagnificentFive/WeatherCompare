# tests/test_backend.py

import unittest
from unittest.mock import patch, MagicMock
from backend.test_news import get_news

class TestBackend(unittest.TestCase):

    @patch('requests.get')
    def test_get_news(self, mock_get):
        # Mock the response from the news API
        mock_response = {
            'status': 'ok',
            'articles': [
                {'title': 'Test Article 1'},
                {'title': 'Test Article 2'}
            ]
        }
        mock_get.return_value = MagicMock()
        mock_get.return_value.json.return_value = mock_response

        # Call the function that fetches news articles
        result = get_news()

        # Assert the result matches the expected data
        self.assertEqual(result, ['Test Article 1', 'Test Article 2'])

if __name__ == '__main__':
    unittest.main()
