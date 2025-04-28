import pytest
import json
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_get_users_empty(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert json.loads(response.data) == []

def test_create_user(client):
    response = client.post('/users', 
                         json={'username': 'testuser', 'email': 'test@example.com'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['username'] == 'testuser'
    assert data['email'] == 'test@example.com'

def test_get_users(client):
    client.post('/users', json={'username': 'user1', 'email': 'user1@example.com'})
    client.post('/users', json={'username': 'user2', 'email': 'user2@example.com'})
    
    response = client.get('/users')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
