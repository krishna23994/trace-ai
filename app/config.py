"""
Configuration settings for Trace-AI application
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    DB_PATH = os.getenv('DB_PATH', 'logs.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')


class TestConfig(Config):
    """Test configuration"""
    TESTING = True
    DB_PATH = ':memory:'