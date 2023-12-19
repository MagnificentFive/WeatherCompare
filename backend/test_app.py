import pytest
from app import app, db, News

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()
        sample_news = News(
            dt='2022-01-01',
            title='Test News',
            text='This is a test news article.',
            image_url='https://example.com/image.jpg'
        )
        db.session.add(sample_news)
        db.session.commit()

    yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_news_endpoint(client):
    response = client.get('/news')

    assert response.status_code == 200

    expected_data = {
        'success': True,
        'result': [{
            'dt': '2022-01-01',
            'title': 'Test News',
            'text': 'This is a test news article.',
            'image_url': 'https://example.com/image.jpg'
        }]
    }
    assert response.json == expected_data
