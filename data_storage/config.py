"""
Configurações para armazenamento de dados.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class StorageConfig:
    """Configurações de armazenamento."""
    
    # PostgreSQL
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'airflow')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'airflow')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'airflow')
    
    # MongoDB
    MONGODB_HOST = os.getenv('MONGODB_HOST', 'localhost')
    MONGODB_PORT = int(os.getenv('MONGODB_PORT', 27017))
    MONGODB_USER = os.getenv('MONGODB_USER', 'admin')
    MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', 'admin')
    MONGODB_DB = os.getenv('MONGODB_DB', 'ml_database')
    
    # Redis
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
    
    # AWS S3
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', None)
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', None)
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET', None)
    
    # Azure Storage
    AZURE_STORAGE_ACCOUNT_NAME = os.getenv('AZURE_STORAGE_ACCOUNT_NAME', None)
    AZURE_STORAGE_ACCOUNT_KEY = os.getenv('AZURE_STORAGE_ACCOUNT_KEY', None)
    AZURE_STORAGE_CONTAINER = os.getenv('AZURE_STORAGE_CONTAINER', None)
    
    # Google Cloud Storage
    GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID', None)
    GCP_CREDENTIALS_PATH = os.getenv('GCP_CREDENTIALS_PATH', None)
    GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME', None)

