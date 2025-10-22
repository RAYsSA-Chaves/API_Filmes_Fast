# Criar todas as tabelas do banco de dados usando os modelos definidos

import asyncio

from core.database import engine
from models import filme_model
from models import genero_model
from models import genero_filme_model
from models import table_registry


# Função é assíncrona porque usamos engine assíncrono (AsyncEngine)
async def create_tables() -> None:
    print('Criando as tabelas do banco!')

    # Conecta com o banco
    # async with garante que a conexão seja fechada automaticamente
    async with engine.begin() as conn:
        # Deleta todas as tabelas existentes
        # run_sync é necessário porque drop_all é uma função síncrona
        await conn.run_sync(table_registry.metadata.drop_all)

        # Cria todas as tabelas que estão registradas no registry
        await conn.run_sync(table_registry.metadata.create_all)

    print('☑️ Tabelas criadas com sucesso!')


asyncio.run(create_tables())  # funções async não rodam sozinhas, precisam de asyncio.run para executar

# Executar o script:npython criar_tabelas.py
