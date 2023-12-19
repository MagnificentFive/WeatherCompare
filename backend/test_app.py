import unittest
from flask_testing import TestCase
from app import app, db, News

class TestApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

        sample_news = News(
            dt='2022-01-01',
            title='Test News',
            text='This is a test news article.',
            image_url='https://example.com/image.jpg'
        )
        db.session.add(sample_news)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_news_endpoint(self):
        response = self.client.get('/news')

        self.assertEqual(response.status_code, 200)

        expected_data = {
            'success': True,
            'result': [{
                'dt': '2022-01-01',
                'title': 'Test News',
                'text': 'This is a test news article.',
                'image_url': 'https://example.com/image.jpg'
            }]
        }
        self.assertEqual(response.json, expected_data)

if __name__ == '__main__':
    unittest.main()
