"""Test configuration and fixtures"""
import pytest
import tempfile
import os
from app import create_app
from app.config import TestConfig
from app.database import init_db


@pytest.fixture
def client():
    """Create test client with isolated database"""
    db_fd, db_path = tempfile.mkstemp()
    
    class TestConfigLocal(TestConfig):
        DB_PATH = db_path
    
    app = create_app(TestConfigLocal)
    
    with app.test_client() as client:
        with app.app_context():
            init_db(db_path)
            yield client
    
    os.close(db_fd)
    os.unlink(db_path)