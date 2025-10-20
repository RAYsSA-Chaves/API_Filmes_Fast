# Centralizando a criação e fechamento da sessão, para ser usada como dependência nas rotas/requisções

from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Session


# Função que fornece uma sessão do banco para as rotas
# Retorna um gerador (yield) de AsyncSession
async def get_session() -> Generator:
    # Cria uma sessão
    session: AsyncSession = Session()

    try:
        # Retorna a sessão para a rota que depende dela
        # pausa a função
        # o FastAPI injeta essa sessão automaticamente na rota
        yield session
    finally:
        # Fecha a sessão quando a rota termina ou se ocorrer algum erro
        await session.close()
