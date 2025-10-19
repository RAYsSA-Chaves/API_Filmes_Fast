# Centralizando configurações do projeto

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'  # prefixo padrão para todas as rotas
    DB_URL: str = (
        'mysql+asyncmy://root:@127.0.0.1:3307/teste_filmes'  # se não existir arquivo .env, tenta conexão com esse
    )


class Config:
    env_file = '.env'  # indica de onde ler a variável DB_URL


settings = Settings()
