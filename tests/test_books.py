import pytest
from app import create_app
from app.models.book import books
from app.utils.auth import generate_token

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_headers():
    token = generate_token(1)
    return {'Authorization': f'Bearer {token}'}

def test_create_book(client, auth_headers):
    # Clear any existing books
    books.clear()
    
    # Test successful book creation
    response = client.post('/books/', json={
        'title': 'Test Book',
        'author': 'Test Author',
        'isbn': '1234567890',
        'quantity': 5
    }, headers=auth_headers)
    assert response.status_code == 201
    assert response.json['title'] == 'Test Book'
    
    # Test missing fields
    response = client.post('/books/', json={
        'title': 'Test Book'
    }, headers=auth_headers)
    assert response.status_code == 400

def test_get_books(client, auth_headers):
    # Add a test book
    books.clear()
    client.post('/books/', json={
        'title': 'Test Book',
        'author': 'Test Author',
        'isbn': '1234567890',
        'quantity': 5
    }, headers=auth_headers)
    
    # Test get all books
    response = client.get('/books/', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json['books']) == 1
    
    # Test pagination
    response = client.get('/books/?page=1&per_page=10', headers=auth_headers)
    assert response.status_code == 200
    assert 'total_pages' in response.json

def test_search_books(client, auth_headers):
    # Add test books
    books.clear()
    client.post('/books/', json={
        'title': 'Python Programming',
        'author': 'John Doe',
        'isbn': '1234567890',
        'quantity': 5
    }, headers=auth_headers)
    client.post('/books/', json={
        'title': 'Java Programming',
        'author': 'Jane Smith',
        'isbn': '0987654321',
        'quantity': 3
    }, headers=auth_headers)
    
    # Test search by title
    response = client.get('/books/search?q=python', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json['results']) == 1
    
    # Test search by author
    response = client.get('/books/search?q=smith', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json['results']) == 1
