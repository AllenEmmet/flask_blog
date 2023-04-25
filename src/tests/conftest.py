import pytest
from flask import Flask
import src

@pytest.fixture
def app():
    app = src.main()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()
