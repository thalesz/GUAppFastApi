from typing import ClassVar
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
import secrets  # Para geração segura de JWT_SECRET

class Settings(BaseSettings):
    # API endpoint
    API_V1_STR: str = '/api/v1'
    
    # Banco de dados
    DB_URL: str = 'postgresql+asyncpg://postgres:Pureheroine1%40@localhost:5432/Faculdade'
    
    # Declarando DBBaseModel como uma variável de classe com ClassVar
    DBBaseModel: ClassVar = declarative_base()

    # JWT Token
    JWT_SECRET: str = secrets.token_urlsafe(32)  # Gerando um segredo único e seguro
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 semana

    # Configurações Pydantic
    class Config:
        case_sensitive = True

# Instanciando a configuração
settings: Settings = Settings()
