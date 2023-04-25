import src
import pytest

def test_index(client):
    response = client.get('/')
    assert response.status_code == 302

def test_login(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_register(client):
    response = client.get('/register')
    assert response.status_code == 200 # This is the status code for a successful request

def test_dashboard(client):
    response = client.get('/home')
    assert response.status_code == 200 # This is the status code for a redirect