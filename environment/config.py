from dotenv import load_dotenv
from pathlib import Path
import os

"""Usando pathlib para garantir que o .env seja carregado corretamente independentemente do sistema operacional e do nível hierarquico das pastas do projeto."""
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

class Config:
    ORACLE_USER = os.getenv('ORACLE_USER')
    ORACLE_PASSWORD = os.getenv('ORACLE_PASSWORD')
    ORACLE_SERVICE = os.getenv('ORACLE_SERVICE')
    ORACLE_HOST = os.getenv('ORACLE_HOST')
    ORACLE_PORT = os.getenv('ORACLE_PORT')
    JDBC_PATH = os.getenv('JDBC_PATH')
    JDBC_DRIVER = os.getenv('JDBC_DRIVER')
    JDBC_URL = f'jdbc:oracle:thin:@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}'

class ConfigAuth:
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHM = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')