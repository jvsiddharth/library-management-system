import pytest
from app import create_app
from app.models.member import members

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register(client):
    # Clear any existing members
    members.clear()
    
    # Test successful registration
    response = client.post('/auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.json['member']['name'] == 'Test User'
    assert response.json['member']['email'] == 'test@example.com'
    
    # Test duplicate email
    response = client.post('/auth/register', json={
        'name': 'Another User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert 'already registered' in response.json['message']

def test_login(client):
    # Register a test user
    client.post('/auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    # Test successful login
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'token' in response.json
    
    # Test invalid credentials
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
