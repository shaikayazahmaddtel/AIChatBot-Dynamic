"""
Application Configuration Settings
"""
import os
from datetime import timedelta

class BaseConfig:
    """Base Configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///chatbot.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo-16k')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'text-embedding-ada-002')
    
    # Vector Store
    VECTOR_STORE_PATH = os.getenv('VECTOR_STORE_PATH', './data/vector_stores')
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Rate Limiting
    RATELIMIT_DEFAULT = "100/hour;1000/day"
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_POOL_SIZE = 20

class StagingConfig(BaseConfig):
    DEBUG = False
